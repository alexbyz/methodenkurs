import pandas as pd
from sklearn.feature_extraction.text import (CountVectorizer, TfidfTransformer)
from sklearn.metrics.pairwise import cosine_similarity

import os, yaml, json, re, sys
from datetime import datetime


settingsFile = "./settings.yml"
settings = yaml.load(open(settingsFile))

dataPath = settings["path_to_data"]

########################
#searchTerm = r"\b(((w|W)ein)|((b|B)aum))garten\b"
#searchTerm = r"\b(s|S)tephan\b"
#searchTerm = r"(frau|(v|V)ro(n|w))"
#searchTerm = r"(\bver|)kauf"
#searchTerm = r"(\bge|)schaff"
#searchTerm = r"\b(h|H)aus"
#searchTerm = r"\b(m|M)esse"
#searchTerm = r"spital"
#searchTerm = r"\b(s|S)un\b"
#searchTerm = r"\b(t|T)ochter\b"
#searchTerm = r"purger"
#searchTerm = r"\b(h|H)erz(o|\u00f6)"
searchTerm = r"\b([A-Z])\w+\b (der|des|dem) \b\w+\b"
########################

def loadFile(dataPath):

     data = json.load(open(dataPath + "regesten.json", encoding="utf8"))

     return data

def searchReg(regDict):

    resultsDict = {}
    count = 0
    regList = []

    for key, val in regDict.items():

        resultsDict["searchTerm"] = searchTerm
        
        if "cont" in val:
            if re.search(r"%s" % searchTerm, val["cont"], flags=re.IGNORECASE):           
                resultsDict[key] = {}
                resultsDict[key]["cont"] = val["cont"]
                resultsDict[key]["link"] = val["link"]
                count +=1
                regList.append(key)

        resultsDict["count"] = count  

        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        resultsDict["timestamp"] = currentTime 

    resultsDict["list"] =  regList              
               
    return resultsDict

def saveResults(resultsDict):

    saveWith = re.sub("\W+", "", searchTerm)
    saveTo = os.path.join(dataPath, "searches", "%s.searchResults" % saveWith)

    with open(saveTo, 'w', encoding='utf8') as f9:
        json.dump(resultsDict, f9, sort_keys=True, indent=4, ensure_ascii=False)


regDict = loadFile(dataPath)
results = searchReg(regDict)
saveResults(results)

print("*"*80)
print("%s %d mal gefunden" %(searchTerm, results["count"]))
print("*"*80)


