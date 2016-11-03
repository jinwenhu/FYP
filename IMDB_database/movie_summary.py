import os
import ast

movie_list = []
movie_index = {}

for dirpath, dirs, files in os.walk('movie_image\\'):
    for file in files:
        file_name = os.path.splitext(file)[0]
        movie_list.append(file_name)

with open("movie_list", "wb") as output:
    with open("movie_metadata", "rb") as input:
        lines = input.read().splitlines()
        for i in range(0, len(lines)):
            lines[i] = ast.literal_eval(lines[i])
            movie_index[lines[i][0]] = i;
            #line = ast.literal_eval(line)
        for movie in movie_list:
            try:
                index = movie_index[movie]
                output.write("%s\n"%lines[index])
            except Exception, e:
                print movie
                continue

