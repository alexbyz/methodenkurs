import pandas as pd
from sklearn.feature_extraction.text import (CountVectorizer, TfidfTransformer)
from sklearn.metrics.pairwise import cosine_similarity

import os, yaml, json, re, sys
import datetime
import loadReg

settingsFile = "./settings.yml"
settings = yaml.load(open(settingsFile))
min_Df_S = settings["min_df"]
max_Df_S = settings["max_df"]

dataPath = settings["path_to_data"]

def loadFile(dataPath):

     data = json.load(open(dataPath + "regesten.json", encoding="utf8"))

     return data

def filterDic(dic, thold): 

    retDic = {}    #empty Dictonary to copy filterd values into

    for k,v in dic.items():     #loop through outer first dic, containig the titles
        retDic[k]={}            #create a subDic for each title

        for key,val in v.items():   #loop through the entries of each title
            if val > thold:         #check threshold                            
                if k != key:        #check to not match the publication with itself
                    retDic[k][key] = val    #add value

    return(retDic)

def generatetfidfvalues():

    #ocrFiles = functions.dicOfRelevantFiles(memexPath, ".json")
    ocrFiles = loadReg.loadData(dataPath)
    citeKeys = list(ocrFiles.keys())

    docList   = []
    docIdList = []

    with open("_misc/stopwords.txt", "r", encoding="utf8") as f1:
        stopW = f1.read().split("\n")     

    for key, val in data.items():
        if "cont" in val:
            docList.append(val["cont"])
            docIdList.append(key)

    #convert data
    vectorizer = CountVectorizer(ngram_range=(1,1), min_df=min_Df_S, max_df=max_Df_S, stop_words=stopW)
    countVectorized = vectorizer.fit_transform(docList)
    tfidfTransformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    vectorized = tfidfTransformer.fit_transform(countVectorized) # https://en.wikipedia.org/wiki/Sparse_matrix
    cosineMatrix = cosine_similarity(vectorized)

    #converting results
    tfidfTable = pd.DataFrame(vectorized.toarray(), index=docIdList, columns=vectorizer.get_feature_names())
    print("tfidfTable Shape: ", tfidfTable.shape) # optional
    tfidfTable = tfidfTable.transpose()
    tfidfTableDic = tfidfTable.to_dict()

    cosineTable = pd.DataFrame(cosineMatrix)
    print("cosineTable Shape: ", cosineTable.shape) # optional
    cosineTable.columns = docIdList
    cosineTable.index = docIdList
    cosineTableDic = cosineTable.to_dict()

    filteredDic = {}
    filteredDic = filterDic(tfidfTableDic, 0.02)
    saveTo = os.path.join(dataPath, "tfidf", "tfidfTableDic_filtered.txt")
    with open(saveTo, 'w', encoding='utf8') as f9:
        json.dump(filteredDic, f9, sort_keys=True, indent=4, ensure_ascii=False)

    filteredDic = {}
    filteredDic = filterDic(cosineTableDic, 0.2)

    saveTo = os.path.join(dataPath, "tfidf", "cosineTableDic_filtered.txt")
    with open(saveTo, 'w', encoding='utf8') as f9:
        json.dump(filteredDic, f9, sort_keys=True, indent=4, ensure_ascii=False)

data = loadFile(dataPath)
generatetfidfvalues()