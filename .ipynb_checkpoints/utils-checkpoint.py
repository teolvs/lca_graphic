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


def lca_comparison(fu, methods, method_ref=('Impact Potential', 'GCC'), ):
    '''
    Compare several activities for several impact categories and return a DataFrame with the impact score for each categories and each activities.
    ----------
    fu : dicitonnary of the activity/activities to compare associated with its/their associated reference flow/s
    methods : tuple of several/single methods
    method_ref : method used for normalization
    '''
    scores=[]
    names=[]
    try: #for multi impact categories
        for act, q in zip(fu.keys(),fu.values()):
            lca=bc.LCA({act:q},methods[0])
            lca.lci()
            lca.lcia()
            res=[]
            for m in methods:
                lca.switch_method(m)
                lca.lcia()
                res.append(lca.score)
            scores.append(res)
            names.append(act['name'])
    except : #if only one method
        for act, q in zip(fu.keys(),fu.values()):
            lca=bc.LCA({act:q},methods[0])
            lca.lci()
            lca.lcia()
            scores.append(lca.score)
            names.append(act['name'])
    return pd.DataFrame(index=names,data=scores,columns=methods).sort_values(by=[method_ref],ascending=False)



def act_topscore(fu, method_ref=('Impact Potential', 'GCC')):
    '''
    Give the activity which has the highest score the reference method
    ----------
    fu : dicitonnary of the activity/activities to compare associated with its/their associated reference flow/s
    method_ref : method used for normalization (by default, GCC)
    '''
    activities=list(fu.keys())
    scores=[]
    
    for act, q in zip(activities,fu.values()):
        lca=bc.LCA({act:q},method_ref)
        lca.lci()
        lca.lcia()
        scores.append(lca.score)

    # Récupération de l'index de l'activité ayant le score d'impact le plus élevé
    max_index = scores.index(max(scores))
        
    return activities[max_index]

def contributions_df(activity,method,limit=0.01,limit_type='percent',group_by_other=True, norm=False):
    '''
    Gather in a dataframe the main contributors of the lca score 
    ----------    
    activity : activity to be analyzed
    method : impact category method
    limit: relative threshold of the total lca score from which contributors are displayed : (0.01 by default)
    limit_type : percentage or number for the threshold ('percent' by default)
    group_by_other : group the other contributors into an 'other' category (True by default)
    norm : norm the contributions (False by default)
    '''
    
    ca = ba.ContributionAnalysis()    
    #we compute the top contributors for the impact category
    lca=bc.LCA({activity:1},method)
    lca.lci()
    lca.lcia()
    contrib=(ca.annotated_top_processes(lca, limit=limit, limit_type=limit_type)) #returns a list of tuples: (lca score, supply amount, activity name)

    names=[i[2]['name'] for i in contrib] #for each impact category we concatenate all names
    scores=[i[0] for i in contrib]#for each impact category we add a new tuple for the scores
    
    if group_by_other:
        names.append('Others')
        scores.append(lca.score-np.sum(scores))
    
    if norm:
        scores=[s/lca.score*100 for s in scores]

    return pd.DataFrame(index=names, data=scores, columns=[method]).sort_values(by=[method],ascending=True)
