# data will be a data frame
# w is the weights list
# i is the impact list
# returns a list of the ranks of the alternatives
import numpy as np
import pandas as pd
import copy

#todo : add conditions

def Normalize(dataset, nCol, weights):
    # print(weights)
    for j in range(0, nCol):
        temp = 0
        # Calculating Root of Sum of squares of a particular column
        for i in range(len(dataset)):
            temp = temp + dataset.iloc[i, j]**2
        temp = temp**0.5
        # Weighted Normalizing a element
        for i in range(len(dataset)):
            dataset.iat[i, j] = (dataset.iloc[i, j] / temp)*weights[j]
    return dataset

def Calc_Values(dataset, nCol, impact):
    p_sln = (dataset.max().values)
    n_sln = (dataset.min().values)
    # print(p_sln)
    # print(n_sln)
    for i in range(0, nCol):
        if impact[i] == '-':
            p_sln[i], n_sln[i] = n_sln[i], p_sln[i]
    return p_sln, n_sln

def topsis(dtemp, w, i):
    nCol = dtemp.shape[1]
    if(nCol!=len(w)):
        print("Weights length does not match data length")
        return
    if(nCol!=len(i)):
        print("Impacts length does not match data length")
        return
    if(len(w)!=len(i)):
        print("Impact length does not match weight length")
    data = copy.deepcopy(dtemp);
    data = Normalize(data, nCol, w)    #weighted normalized matrix
    # print("Normalized data")
    # print(data)
    p_sln, n_sln = Calc_Values(data, nCol, i)
    score = []
    #iterating through rows
    for i in range(len(data)):
        temp_p, temp_n = 0, 0
        for j in range(data.shape[1]):
            temp_p = temp_p + (p_sln[j] - data.iloc[i, j])**2
            temp_n = temp_n + (n_sln[j] - data.iloc[i, j])**2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        score.append(temp_n/(temp_p + temp_n))
        
    # print(score)
    return score



def rerank(data, score, inplace = True):
    if inplace:
        data['Score'] = score
        data['Rank'] = data['Score'].rank(method='max', ascending = False)
        data.sort_values(by = ['Rank'], inplace = True)
    else:
        new_data = copy.deepcopy(data)
        new_data['Score'] = score
        new_data['Rank'] = new_data['Score'].rank(method='max', ascending = False)
        new_data.sort_values(by = ['Rank'], inplace = True)
        return new_data
    