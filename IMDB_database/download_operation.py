
import json
import re
import ast
from Retrieval import download

output = []
movie_dict = []

with open("movie_metadata", "rb") as input:
    lines = input.read().splitlines()
    for line in lines:
        line = ast.literal_eval(line)
        url = line[3]
        title = line[0]
        if not line[0] or not line[1] or not line[2] or not line[3]:
            continue
        grene_before = line[1]
        grenes = grene_before.split("|")
        grene = ""
        for item in grenes:
            grene = grene + "#" + item
        try:
            download(url, title, grene)
        except Exception, e:
            print "Error with url: %s" % url
            continue