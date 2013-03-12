# -*- utf-8 -*-
'''
Created on 2013-3-12

@author: wayne
'''
from math import sqrt

pathMovieLens = r'E:\learning\CollectiveIntelligence\ch02\ml-100k'

def loadMovieLens(path = pathMovieLens):
    
    #get movie title
    movies = {}
    for line in open(path + '/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title
    
    prefs = {}
    for line in open(path + '/u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)
    return prefs    


def sim_distance(prefs, p1, p2):
    
    #get shared items
    getSi = lambda x, y : {item : 1 for item in prefs[x] if item in prefs[y]} 
    si = getSi(p1, p2) if len(p1) >= len(p2) else getSi(p2, p1)
    
    if len(si) == 0: return 0
    
    sumSq = sum([pow(prefs[p1][item] - prefs[p2][item], 2) for item in si])
    return 1/(1+sqrt(sumSq))

def sim_pearson(prefs, p1, p2):
    