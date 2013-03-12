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

def getSi(prefs, p1, p2):
    #get shared items
    getSi = lambda x, y : {item : 1 for item in prefs[x] if item in prefs[y]} 
    si = getSi(p1, p2) if len(p1) >= len(p2) else getSi(p2, p1)
    return si

def sim_distance(prefs, p1, p2):
    
    si = getSi(prefs, p1, p2)
    
    if len(si) == 0: return 0
    
    sumSq = sum([pow(prefs[p1][item] - prefs[p2][item], 2) for item in si])
    return 1/(1+sqrt(sumSq))

def sim_pearson(prefs, p1, p2):
    
    si = getSi(prefs, p1, p2)
    n = len(si)
    
    if n == 0: return 0
    
    sum1 = sum([prefs[p1][item] for item in si])
    sum2 = sum([prefs[p2][item] for item in si])
    
    sumSq1 = sum( [ pow(prefs[p1][item], 2) for item in si ] )
    sumSq2 = sum( [ pow(prefs[p2][item], 2) for item in si ] )
    
    sumMul = sum( [ prefs[p1][item]*prefs[p2][item] for item in si ] )
    
    num = sumMul - sum1*sum2/n
    den = sqrt( (sumSq1 - pow(sum1, 2)/n) * (sumSq2 - pow(sum2, 2)/n) )
    if den == 0: return 0;
    return num/den

def topMatches(prefs, person, n = 5, similarity = sim_pearson):
    scores = [ (similarity(prefs, person, other), other) for other in prefs if other != person ]
    scores.sort(reverse = True)
    index = n if n < len(scores) else len(scores)
    return scores[0:index]

def getRecommendations(prefs, person, similarity = sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        if other == person: continue
        sim = similarity(prefs, person, other)
        
        if sim < 0: continue
        for item in prefs[other]:
            if item not in prefs[person]  or  prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item]*sim
                
                simSums.setdefault(item, 0)
                simSums[item] += sim
    rankings = [ (total/simSums[item], item) 
                for item, total in totals.items() if simSums[item] != 0 ]
    rankings.sort(reverse=True)
    return rankings

def transform(prefs):
    for person, movieLst in prefs.item():
        for 


