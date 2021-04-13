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
#searchTerm = r"\b([A-Z])\w+\b (der|des|dem) \b\w+\b"
#searchTerm = r"(swester|) Kathrein"
#searchTerm = r"Chunra(d|t)"
#searchTerm = r"Mergart"
#searchTerm = r"Jansen"
searchTerm = r"\bpurgermaister\b"
########################

def loadFile(dataPath):

     data = json.load(open(dataPath + "regesten.json", encoding="utf8"))

     return data

def searchReg(regDict):

    resultsDict = {}    #empty dict for the results
    count = 0           #counts the regests where the search term is found
    regList = []        #list with all the reg-numbers

    for key, val in regDict.items():    #loops through the json file of the regests

        resultsDict["searchTerm"] = searchTerm  #adds the search term to the dict
        
        if "cont" in val:       #does the current regest have content?
            if re.search(r"%s" % searchTerm, val["cont"], flags=re.IGNORECASE): #searches the term in the content           
                resultsDict[key] = {}       #creates empty dict with the key if the term is found
                resultsDict[key]["cont"] = val["cont"]  #saves the content
                resultsDict[key]["id"] = val["id"]      #saves over the id
                count +=1                               #counter
                regList.append(key)                     #add id tho the list

        resultsDict["count"] = count                    #add counter

        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  #adds timestamp
        resultsDict["timestamp"] = currentTime 

    resultsDict["list"] =  regList           #adds list   
               
    return resultsDict

def saveResults(resultsDict):               #saves results into a json file

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


