import graph
import json
import numpy as np

#tags database
with open("data/tags.dat") as input:
    tags = input.read().splitlines()
    del tags[0]
input.close()

#operate on tags
tags_dict = {}
reverse_tags_dict = {}
for line in tags:
    line = line.split("\t")
    tags_dict[int(line[0])] = line[1]
    reverse_tags_dict[line[1]] = int(line[0])

num_features = max(tags_dict.keys())
#movies tag database
with open("data/movie_tags.dat") as input:
    movie_tags = input.read().splitlines()
    del movie_tags[0]
input.close()

#operate on movie tags
movie_tags_dict = {}
for line in movie_tags:
    movie_id, tag_id, tag_weight = map(int, line.split("\t"))
    #add movie id to movie_tags_dict
    if movie_id not in movie_tags_dict:
        movie_tags_dict[movie_id] = [0] * num_features
    #add tags to movie list
    movie_tags_dict[movie_id][tag_id] += tag_weight

#load graph instance
gp = graph.graph()

#generate implicit tags from explicit
movie_tags_implicit_dict = {}
for movie_id in movie_tags_dict:
    movie_id = int(movie_id)
    if movie_id not in movie_tags_implicit_dict:
        movie_tags_implicit_dict[movie_id] = [0] * num_features
    movie_tags_num = np.count_nonzero(movie_tags_dict[movie_id])
    explicit_id_list = [tag_id for tag_id in range(num_features) if movie_tags_dict[movie_id][tag_id]]
    for i in range(movie_tags_num):
        tag1 = tags_dict[explicit_id_list[i]]
        #head_list = movie_tags_dict[movie_id][i].split(" ")
        for j in range(i+1, movie_tags_num):
            tag2 = tags_dict[explicit_id_list[j]]
            implicit_tag_list = gp.query(tag1, tag2)
            if implicit_tag_list and len(implicit_tag_list) < 7:
                implicit_id_list = [reverse_tags_dict[tag] for tag in implicit_tag_list[1:-1] if tag in tags_dict]
                for tag_id in implicit_id_list:
                    movie_tags_implicit_dict[movie_id][tag_id] += 1
                #movie_tags_implicit_dict[movie_id]
            #tail_list = movie_tags_dict[movie_id][j]
            
            #find path and insert into movies_tags_implicit_dict
            """
            for start in head_list:
                for end in tail_list:
                    implicit_list = gp.query(start, end)
                    if implicit_list and len(implicit_list) < 7:
                        movie_tags_implicit_dict[movie_id].extend(implicit_list[1:-1])
            """

#write into file explicit and implicit movie tag lists
with open("data/movie_explicit_tags", "w") as output1:
    json.dump(movie_tags_dict, output1)
output1.close()

with open("data/movie_implicit_tags", "w") as output2:
    json.dump(movie_tags_implicit_dict, output2)
output2.close()