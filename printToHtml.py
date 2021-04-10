import pandas as pd
from sklearn.feature_extraction.text import (CountVectorizer, TfidfTransformer)
from sklearn.metrics.pairwise import cosine_similarity

import os, yaml, json, re, sys
import datetime

settingsFile = "./settings.yml"
settings = yaml.load(open(settingsFile, encoding="utf8"))

dataPath = settings["path_to_data"]

searchesTemplate = """
<button class="collapsible">SAVED SEARCHES</button>
<div class="content">
<table id="" class="display" width="100%">
<thead>
    <tr>
        <th><i>link</i></th>
        <th>search string</th>
        <th># of publications with matches</th>
        <th>time stamp</th>
    </tr>
</thead>
<tbody>
@TABLECONTENTS@
</tbody>
</table>
</div>
"""

def loadTemplate(path):

    with open(path, encoding="utf8") as f1:
        template = f1.read()

    return template

def loadSearches(pathToSaves):

    path = os.path.join("_misc", "template.html")
    template = loadTemplate(path)   

    for subdir, dirs, files in os.walk(pathToSaves):
        for file in files:
            
            searchFilePath = os.path.join(dataPath, "searches", file)
            data = json.load(open(searchFilePath, encoding="utf8"))

            singleItemTemplate = '<tr><td>%s</td><td>%s</td></tr>' % (data["key"], data["cont"])


path = os.path.join(dataPath, "searches")
loadSearches(path)        