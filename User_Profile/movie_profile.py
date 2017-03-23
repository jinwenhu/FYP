import graph
import json

#tags database
with open("tags.dat") as input:
    tags = input.read().splitlines()
    del tags[0]
input.close()

#operate on tags
tags_dict = {}
for line in tags:
    line = line.split("\t")
    tags_dict[line[0]] = line[1]

#movies tag database
with open("movie_tags.dat") as input:
    movie_tags = input.read().splitlines()
    del movie_tags[0]
input.close()

#operate on movie tags
movie_tags_dict = {}
for line in movie_tags:
    line = line.split("\t")
    #add movie id to movie_tags_dict
    if line[0] not in movie_tags_dict:
        movie_tags_dict[line[0]] = []
    #add tags to movie list
    temp_tag = tags_dict[line[1]]
    movie_tags_dict[line[0]].append(temp_tag)

#load graph instance
gp = graph.graph()

#generate implicit tags from explicit
movie_tags_implicit_dict = {}
for movie_id in movie_tags_dict:
    if movie_id not in movie_tags_implicit_dict:
        movie_tags_implicit_dict[movie_id] = []
    movie_tags_num = len(movie_tags_dict[movie_id])
    for i in range(movie_tags_num):
        head_list = movie_tags_dict[movie_id][i].split(" ")
        for j in range(i+1, movie_tags_num):
            tail_list = movie_tags_dict[movie_id][j].split(" ")

            #find path and insert into movies_tags_implicit_dict
            for start in head_list:
                for end in tail_list:
                    implicit_list = gp.query(start, end)
                    if implicit_list and len(implicit_list) < 5:
                        movie_tags_implicit_dict[movie_id].extend(implicit_list[1:-1])


#write into file explicit and implicit movie tag lists
with open("movie_explicit_tags", "w") as output1:
    json.dump(movie_tags_dict, output1)
output1.close()

with open("movie_implicit_tags", "w") as output2:
    json.dump(movie_tags_implicit_dict, output2)
output2.close()