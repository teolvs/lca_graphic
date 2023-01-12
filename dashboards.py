import bw2data as bd
import bw2calc as bc
import bw2io as bi
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import json
import os
import matrix_utils as mu
import bw_processing as bp
import math
import warnings
import ipywidgets as widgets
from ipywidgets import interact
import bw2analyzer as ba
import seaborn as sns
import textwrap

from utils import *

#define standard color palette:
colors = ["#F08C2E", "#7f6000", "#72AF42", "#A32683"]

#create longer color list for complex figures
color_div_YlBr=sns.color_palette('YlOrBr',6)
color_seq_green=sns.color_palette('Greens',6)
color_seq_RdPu=sns.color_palette('RdPu',6)
color_seq_org=sns.color_palette('Oranges',5)

colors.extend(colors)


#the 2 following methods come from the library lca_algebraic from stats.py : 
# https://github.com/oie-mines-paristech/lca_algebraic/blob/master/lca_algebraic/stats.py
def _display_tabs(titlesAndContentF):
    """Generate tabs"""
    tabs = []
    titles = []
    for title, content_f in titlesAndContentF:
        titles.append(title)

        tab = widgets.Output()
        with tab:
            content_f()
        tabs.append(tab)

    res = widgets.Tab(children=tabs)
    for i, title in enumerate(titles):
        res.set_title(i, title)
    display(res)
    
def displayWithExportButton(df):
    '''Display dataframe with option to export'''

    button = widgets.Button(description="Export data")
    button.style.button_color = "lightgray"
    def click(e) :
        df.to_csv("out.csv")
        button.description = "exported as 'out.csv'"
    dfout = widgets.Output()
    with dfout :
        display(df)

    button.on_click(click)

    display(widgets.VBox([button, dfout]))


def compare(fu, methods, reference_category =('Impact Potential', 'GCC'), sharex=True, cols=1, func_unit="kg"):
    '''
    Compare several activities for several impact categories
    ----------
    fu : dicitonnary of the activity/activities to compare associated with its/their associated reference flow/s
    methods : set of methods,
    act_transfert : activity for which the impact transfers compared to the top activity are computed 
    method_ref : method used for normalization    
    sharex: Shared X axes ? True by default
    cols: number of columns to plot
    func_unit : functionnal unit (kg by default)
    '''
    
    act=list(fu.keys())
    df=lca_comparison(fu, methods, method_ref=reference_category)
    act_ref=act_topscore(fu)
    
    def table():
        displayWithExportButton(df)
        
    def graph_method_ref():
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fig, axes = plt.subplots(figsize=(20,10))
            sns.set_style("white")
            df[reference_category ].plot(
                ax=axes, sharex=sharex,
                legend=None,
                rot=0,
                kind='bar',
                alpha=0.8,
                fontsize=20,
                color=colors)

            axes.set_yticklabels(["0"]) #to remove all the graduations and keep only the zero
            axes.set_ylabel(reference_category[0], fontsize=20)

            #add each score of components
            # the text color is white if the figure is dark and vice versa 
            r, g, b, _ = fig.get_facecolor()
            if r + g + b > 1:
                c = 'black'
            else:
                c = 'white'
                
            # Hide edges of the frame
            for spine in axes.spines.values():
                if spine.spine_type == 'bottom':
                    spine.set_visible(True)
                else:
                    spine.set_visible(False)
                    
            for bar in axes.patches:
                axes.text(
                        # Put the text in the middle of each bar. get_x returns the start
                        # so we add half the width to get to the middle.
                        bar.get_x() + bar.get_width() / 2,
                        # Vertically, add the height of the bar to the start of the bar,
                        # along with the offset.
                        bar.get_height() + bar.get_y(),
                        # This is actual value we'll show.
                        str('{:.2e}'.format(bar.get_height())) + '\n' + reference_category[1],
                        # Center the labels and style them a bit.
                        ha='center',
                        color=c,
                        alpha=0.8,
                        size=15,
                    )
            
            plt.xticks(range(len(df)), ['\n'.join(textwrap.wrap(label, 20)) for label in df.index])
            
            #add a suptitle
            fig.suptitle("Comparison of different LCA on " + reference_category[0], fontsize=30, fontweight='bold', ha='center') #centered title in bold
            # add a subtitle
            axes.set_title("for 1 " + func_unit,fontsize=17, ha='center',y=1.1, color='gray')
            plt.tight_layout()
            plt.show(fig)

    def graph_multi():
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            nb_rows = int(np.ceil(len(methods) / cols))
            fig, axes = plt.subplots(figsize=(20,15))
            sns.set_style("white")
            plt.subplots_adjust(None, None, None, None, 0.5, 0.5)

            axes = df.plot(
                ax=axes, sharex=sharex, subplots=True,
                layout=(nb_rows, cols),
                legend=None,
                rot=0,
                kind='bar',
                alpha=0.8,
                fontsize=15,
                color=colors)
            axes = axes.flatten()
            for ax, m in zip(axes, methods):
                ax.set_yticklabels(["0"]) #to remove all the graduations and keep only the zero
                ax.set_ylabel(m[0], fontsize=15)
                ax.set_xticks(range(len(df)), ['\n'.join(textwrap.wrap(label, 20)) for label in df.index])
                ax.set_title('')
                
                # Hide edges of the frame
                for spine in ax.spines.values():
                    if spine.spine_type == 'bottom':
                        spine.set_visible(True)
                    else:
                        spine.set_visible(False)

                #add each score of components
                # the color is white if the figure is dark and vice versa 
                r, g, b, _ = fig.get_facecolor()
                if r + g + b > 1:
                    c = 'black'
                else:
                    c = 'white'  
                for bar in ax.patches:
                    ax.text(
                        # Put the text in the middle of each bar. get_x returns the start
                        # so we add half the width to get to the middle.
                        bar.get_x() + bar.get_width() / 2,
                        # Vertically, add the height of the bar to the start of the bar,
                        # along with the offset.
                        bar.get_height() + bar.get_y(),
                        # This is actual value we'll show.
                        str('{:.1e}'.format(bar.get_height())) + '\n' + m[1],
                        # Center the labels and style them a bit.
                        ha='center',
                        color=c,
                        alpha=0.7,
                        size=12,
                        )
            
            fig.suptitle("Comparison of different LCA on several impact categories", fontsize=30, fontweight='bold', ha='center', y=1.03) #centered title in bold
            fig.text(0.5, 0.99, "for 1 " + func_unit, fontsize=17, ha='center', color='gray')            
            plt.tight_layout()
            plt.show(fig)
            
            displayWithExportButton(df)
        
    _display_tabs([
        ("Reference indicator", graph_method_ref),
        ("All indicators",graph_multi),       
    ])

def hotspots(fu, methods, reference_category=('Impact Potential', 'GCC'),limit=0.05, func_unit="kg"):
    '''
    Plot the contribution analysis of an activity for several impact categories and display the associated DataFrame ready to export. If the number of activities is too large, the figure is not displayed.
    ----------
    fu : dicitonnary of the single activity with its associated amount
    methods : set of impact category methods
    method_ref : method used for normalization ('Impact Potential', 'GCC') by default
    limit: relative threshold of the total lca score from which contributors are displayed : (0.05 by default)
    func_unit : functionnal unit (kg by default)
    '''
    df=lca_comparison(fu, methods, method_ref=reference_category)
    
    #to have one color by method, we define a dataframe:
    df_color=pd.DataFrame(index=methods,data=[colors[c] for c in range(len(methods))]).T
    
    def contributions(act, method):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  
            fig, axes = plt.subplots(figsize=(20,10))
            sns.set_style("white")
            plt.subplots_adjust(None, None, None, None, 0.5, 0.5)
            df_contrib=contributions_df(act,method,limit=limit)
            plt.barh(df_contrib.index,df_contrib[method],alpha=0.8,color=df_color[method])
            axes.set_title('Contribution analysis of  LCA on {}'
                          .format(method[0]),fontsize=20)
            axes.set_xlabel(method[0], fontsize=20)
            axes.set_xticks([])
            axes.set_yticks(range(len(df_contrib)), ['\n'.join(textwrap.wrap(label, 40)) for label in df_contrib.index],fontsize=20)

            #add each score of components
            for bar in axes.patches:
                y_offset = bar.get_width()/100
                
                # the color is white if the bar is dark and vice versa 
                r, g, b, _ = bar.get_facecolor()
                if r + g + b > 1.8:
                    c = 'black'
                else:
                    c = 'white'
                    
                axes.text(
                    bar.get_x() + y_offset,
                    bar.get_y() + bar.get_height()/2,
                    str('{:.2e}'.format(bar.get_width())) + ' '+ method[1], 
                    ha='left',
                    color=c,
                    alpha=0.8,
                    size=15,
                )
                
            # Hide edges of the frame
            for spine in axes.spines.values():
                if spine.spine_type == 'left':
                    spine.set_visible(True)
                else:
                    spine.set_visible(False)
        
            fig.suptitle("Contribution analysis of " + act['name'] +"\n", fontsize=30, fontweight='bold', ha='center',x=axes.get_position().x0+0.5, y=1.02) #centered title in bold
            plt.tight_layout()
            plt.show()
            displayWithExportButton(df_contrib)
    
    if len(fu)>7:
        print('The number of activities is too large to plot the contributions for each of them')
    else :
        for act in list(fu.keys()):
            _display_tabs([("on " + str(i[0]+' ['+i[1]+']'), lambda i=i: contributions(act,i)) for i in methods])


def impact_transfer(fu, methods, reference_category=('Impact Potential', 'GCC'),limit=5, cols=3, func_unit="kg"):
    '''
    Plot the variations of the contribution of the top processes (for the reference method) for each impact category 

    ----------
    fu : dicitonnary of activities with the associated amount
    methods : set of impact category methods
    method_ref : method used for normalization ('Impact Potential', 'GCC') by default
    limit: relative threshold of the total lca score from which contributors are displayed : (0.05 by default)
    '''
    
    act=list(fu.keys())
    df=lca_comparison(fu, methods, method_ref=reference_category)
    act_ref=act_topscore(fu)
    df_norm=df.T.apply(lambda x: x/x.max(), axis=1) #to normalize the results for each impact category
    
    def heatmap():
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fig, axes = plt.subplots(figsize=(20,10))
            sns.set_style("white")
            sns.heatmap(df_norm,annot = True, cbar = True, ax=axes, cmap='YlOrBr', alpha=0.8, linewidth=0.5, xticklabels=True)
            axes.set_yticklabels([m[0] for m in methods], rotation=0, fontsize=20)
            axes.set_xticks(range(len(df_norm.columns)), ['\n'.join(textwrap.wrap(label, 30)) for label in df_norm.columns],rotation=0,fontsize=20,ha="left")
            fig.suptitle("Comparison of different LCA", fontsize=30, fontweight='bold',x=0.44, y=1.02) #centered title in bold
            axes.set_title("for 1 " + func_unit,fontsize=17, ha='center',y=1.1, color='gray')
            plt.show()
            displayWithExportButton(df_norm)

            
    def transfer_impact():            
        
        act_transfert=[act for act in fu.keys() if act!=act_ref][0]
        df_transfer=df_norm[act_transfert['name'] ]*100-df_norm[act_ref['name']]*100 #%
        df_transfer=df_transfer.sort_values()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sns.set_style("white")
            fig, axes = plt.subplots(figsize=(20,10))
            plt.bar(range(len(df_transfer)),df_transfer,alpha=0.8, color=colors)
            plt.xticks(range(len(df_transfer)),[m[0] + ' ' + m[1] for m in methods], fontsize=20)

            #To remove the frame but keep a horizontal line on 0
            axes.spines['top'].set_visible(False)
            axes.spines['right'].set_visible(False)
            axes.spines['bottom'].set_visible(False)
            axes.spines['left'].set_visible(False)
            axes.axhline(y=0, color='gray', linewidth=1)

            #add each score of components
            for bar in axes.patches:
                if bar.get_height()>=0:
                    y_offset=-4
                    axes.set_ylabel('Impact Transfer', fontsize=20)
                    fig.suptitle('Impact transfer of {} \n compared to {}'.format(act_transfert['name'],act_ref['name']),
                                 fontsize=30, fontweight='bold', ha='center')
                else :
                    y_offset=1
                    axes.set_ylabel('Impact Reduction', fontsize=20)
                    fig.suptitle('Impact Reduction of {} \n compared to {}'.format(act_transfert['name'],act_ref['name']),
                                 fontsize=25, fontweight='bold', ha='center')

                # the color is white if the bar is dark and vice versa 
                r, g, b, _ = bar.get_facecolor()
                if r + g + b > 1.8:
                    c = 'black'
                else:
                    c = 'white'
                axes.text(
                      # Put the text in the middle of each bar. get_x returns the start
                      # so we add half the width to get to the middle.
                      bar.get_x() + bar.get_width() / 2,
                      # Vertically, add the height of the bar to the start of the bar,
                      # along with the offset.
                      bar.get_height() + bar.get_y() + y_offset,
                      # This is actual value we'll show.
                      str(round(bar.get_height())) + ' %',
                      # Center the labels and style them a bit.
                      ha='center',
                      color=c,
                      alpha=0.9,
                      size=20,
                  )
            axes.set_yticks([0]) #to remove all the graduations and keep only the zero
            plt.show()
    
    def reference_contributions(act):
        #Get the top contributors for the reference impact category
        df = contributions_df(act,reference_category,limit=limit,limit_type='number',group_by_other=False,norm=True)
        top_contributors_reference = [a for a in df.index]

        #Compute the contributors for the other impact categories and gather it into a dictionnary
        contributions_by_category = {}
        for m in methods:
            contributions_by_category[m] = contributions_df(act, m, limit=0.000001,norm=True) #  very small threshold to get almost every contributors

        # Create an empty dataframe with the top reference contributors as indexes and the impact categories as columns
        result_df = pd.DataFrame(columns=methods, index=top_contributors_reference)

        # For each reference top contributor, check if it appears in the contributions dataframes stored in the dictionary
        for c in top_contributors_reference:
            for m in methods:
                if c in contributions_by_category[m].index:
                    result_df.at[c, m] = contributions_by_category[m].at[c, m]
                else:
                    result_df.at[c, m] = pd.np.nan
        
        #Add a row for the other contributors
        result_df.loc['Others'] = [100 - result_df[c].sum() for c in result_df.columns]

        #Plot the dataframe in a horizontal bar chart
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  
            fig, axes = plt.subplots(figsize=(20,10))
            nb_rows = int(np.ceil(len(methods) / cols))      

            sns.set_style("white")
            plt.subplots_adjust(None, None, None, None, 0.5, 0.5)
            axes = result_df.plot(
                ax=axes, sharey=True, subplots=True,
                layout=(nb_rows, cols),
                legend=None,
                rot=0,
                kind='barh',
                alpha=0.8,
                fontsize=20,
                color=colors)         
            axes=axes.flatten()

            for ax, m in zip(axes, methods):
                ax.set_title(m[0], fontsize=15)
                ax.set_xticks([])
                ax.set_yticks(range(len(result_df)), ['\n'.join(textwrap.wrap(label, 40)) for label in result_df.index],fontsize=20)
                #add each score of components
                for bar in ax.patches:
                    y_offset = 1
                    ax.text(
                        bar.get_x() + + bar.get_width()+ y_offset,
                        bar.get_y() + bar.get_height()/3,
                        str('{:.0f}'.format(bar.get_width())) + ' %', 
                        ha='left',
                        color='black',
                        alpha=0.8,
                        size=12)

                # Hide edges of the frame
                for spine in ax.spines.values():
                    if spine.spine_type == 'left':
                        spine.set_visible(True)
                    else:
                        spine.set_visible(False)
                    
            fig.suptitle("Contribution analysis of " + act['name'] +"\n", fontsize=30, fontweight='bold', ha='center', y=1.02) #centered title in bold
            plt.tight_layout()
            plt.show()

    if len(fu)==2:
        _display_tabs([
            ("Impact transfer", transfer_impact),
            ("Heatmap", heatmap)] +
            [(j['name'], lambda k=j: reference_contributions(k)) for j in list(fu.keys())]
        )    
    else :
        _display_tabs([
        ("Heatmap", heatmap)] +
        [(j['name'], lambda k=j: reference_contributions(k)) for j in list(fu.keys())]
        )



def lca_graphic(fu,methods, reference_category=('Impact Potential', 'GCC'), func_unit="kg"):
    '''
    Generic function that calls the other methods to plot :
        - one dashboard that compare the impacts of serveral activites in different impact categories
        - one dashboard for each activity to plot the main contributors for each impact categories
        - one dashboard to plot the variations of the contribution of the top processes (for the reference method) for each impact category 
    ----------
    fu : dicitonnary of the activity/activities to compare associated with its/their associated reference flow/s
    methods : set of methods,
    method_ref : method used for normalization    
    act_transfert : activity for which the impact transfers compared to the top activity are computed
    func_unit : functionnal unit (kg by default)    
    '''
    
    compare(fu, methods, func_unit=func_unit)
    impact_transfer(fu, methods,reference_category=reference_category,limit=5,func_unit=func_unit,cols=2)
    hotspots(fu, methods, limit=0.02)
