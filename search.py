# NEW LIBRARIES
import pandas as pd
from sklearn.feature_extraction.text import (CountVectorizer, TfidfTransformer)
from sklearn.metrics.pairwise import cosine_similarity

import os, yaml, json, re, sys
import datetime

settingsFile = "./settings.yml"
settings = yaml.load(open(settingsFile))

dataPath = settings["path_to_data"]

########################
searchTerm = "Herzog"
########################

def loadFile(dataPath):

     data = json.load(open(dataPath + "regesten.json", encoding="utf8"))

     return data

def searchReg(searchTerm, regDict):

    resultsDict = {}

    for key, val in regDict.items():
        
        if "cont" in val:
            if searchTerm in val["cont"]:            
                resultsDict[key] = {}
                resultsDict[key]["cont"] = val["cont"]                                
               
    return resultsDict

def saveResults(resultsDict):
    with open(dataPath + searchTerm +".search", 'w', encoding='utf8') as f9:
        json.dump(resultsDict, f9, sort_keys=True, indent=4, ensure_ascii=False)


regDict = loadFile(dataPath)
results = searchReg(searchTerm, regDict)
saveResults(results)




