import pandas as pd
from sklearn.feature_extraction.text import (CountVectorizer, TfidfTransformer)
from sklearn.metrics.pairwise import cosine_similarity

import os, yaml, json, re, sys
import datetime

settingsFile = "./settings.yml"
settings = yaml.load(open(settingsFile))

dataPath = settings["path_to_data"]

import xml.etree.ElementTree as ElementTree

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

    regDict = {}    #empty dict for data

    for subdir, dirs, files in os.walk(path):   #go through all the datastructure in _data/xml/
        for file in files:
            if ".xml" in file:                  #choose only xml files

                p = os.path.join(subdir, file)  #re create the paths of the files

                tree = ElementTree.parse(p)     #get the tree
                root = tree.getroot()           #root

                ####
                #get number
                cont = root.findall("./{http://www.w3.org/2005/Atom}content//{http://www.monasterium.net/NS/cei}idno")  #gets the idno of the regest
                
                for c in cont:  #goes through all the elements in in 
                    key = "".join(c.itertext()) #joins up all the texts within
                    regDict[key]={}             #entry in the dict, subdict with the regId al key
                ####
                
                ####
                #get content
                cont = root.findall("./{http://www.w3.org/2005/Atom}content//{http://www.monasterium.net/NS/cei}abstract")  #gets the abstract text

                for c in cont:
                    text = "".join(c.itertext())
                
                text = text.replace("\n", "")       #removes newlines
                text = " ".join(re.split("\s+", text, flags=re.UNICODE))    #removes spaces within

                regDict[key]["cont"] = text         #stores it in the dict
                ####
                #get date
                cont = root.findall("./{http://www.w3.org/2005/Atom}content//{http://www.monasterium.net/NS/cei}date")  #gets the date of the regest

                for c in cont:
                    dateString = "".join(c.itertext())

                date = dateString.split(" ")    #date is in a string, formate year, month(roman), day
                date[1] = convRomanNumb(date[1])  #converts the month into arab number
                dateX = datetime.datetime(int(date[0]), int(date[1]), int(date[2])) #proper python date format

                regDict[key]["date"] = dateX.strftime('%b/%d/%Y')                #store into the dict
                ####
                #get link
                cont = root.findall("./{http://www.w3.org/2005/Atom}id")        #gets the id monasterium adds to the regest

                for c in cont:
                    link = "".join(c.itertext())
                regDict[key]["id"] = link.replace("tag:", "")
                ####
                #get orig dateing
                cont = root.findall("./{http://www.w3.org/2005/Atom}content//{http://www.monasterium.net/NS/cei}quoteOriginaldatierung")

                for c in cont:
                    orig = "".join(c.itertext())

                orig = orig.replace("\n", "")   #removes newlines
                orig = " ".join(re.split("\s+", orig, flags=re.UNICODE))    #removes spaces within

                regDict[key]["orig"] = orig         #stores the citation of the original dating
                ####                

    with open(path + "regesten.json", 'w', encoding='utf8') as f9:      #saves the dict into a json file
        json.dump(regDict, f9, sort_keys=True, indent=4, ensure_ascii=False)          
    
loadData(dataPath)