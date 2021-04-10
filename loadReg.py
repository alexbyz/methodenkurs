import pandas as pd
from sklearn.feature_extraction.text import (CountVectorizer, TfidfTransformer)
from sklearn.metrics.pairwise import cosine_similarity

import os, yaml, json, re, sys
import datetime

settingsFile = "./settings.yml"
settings = yaml.load(open(settingsFile))

dataPath = settings["path_to_data"]

#loads the regesten from a file and saves them to a json file, returns a dictionary
#Data Structure for the Regesten: 
# Urkunde:
# Datum:
# Abstract:
# Original Dating clause:

def convRomanNumb(s):
    roman = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000,'IV':4,'IX':9,'XL':40,'XC':90,'CD':400,'CM':900}
    i = 0
    num = 0
    while i < len(s):
        if i+1<len(s) and s[i:i+2] in roman:
            num+=roman[s[i:i+2]]
            i+=2
        else:
            #print(i)
            num+=roman[s[i]]
            i+=1
    return num

def loadData(path):

    regDict = {}

    with open(path + "Regesten.txt", "r", encoding="utf8") as f1:
        regesten = f1.read().split("\n:")       

        for r in regesten:            
          
            lines = r.split("\n")
            for line in lines:

                content = ""

                if "Urkunde:" in line:
                    #print(re.findall(r'\b\d+\b', line))
                    num =  re.findall(r'\b\d+\b', line)
                    regDict[num[0]] = {}                    
                    number = num[0]                    

                if "Datum:" in line:
                    dateString = line.strip("Datum:")
                    dateString = dateString.lstrip()
                    d = dateString.split(" ")
                    d[1] = convRomanNumb(d[1])  
                    dateX = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))

                    regDict[number]["date"] = dateX.strftime('%b/%d/%Y')                       

                if "Original dating clause:" in line:                    
                    line = line.strip("Original dating clause")
                    regDict[number]["orig"] = line.strip(":")

                if "Abstract:" in line:                                                 
                    regDict[number]["cont"] = line.strip("Abstract:")

                if "Link:" in line:                                                 
                    regDict[number]["link"] = line.strip("Link:")

    with open(path + "regesten.json", 'w', encoding='utf8') as f9:
        json.dump(regDict, f9, sort_keys=True, indent=4, ensure_ascii=False)
    
    print("*"*80)
    print("%d Regesten geladen" %len(regDict))
    print("*"*80)
    
    return regDict

loadData(dataPath)   