import graph
import json
import numpy as np

#load movie explicit and implicit files
with open("movie_explicit_tags", "r") as input1:
    movie_explicit_tags_dict = json.load(input1)
input1.close()

with open("movie_implicit_tags", "r") as input2:
    movie_implicit_tags_dict = json.load(input2)
input2.close()

#user rating database -> user_id, movie_id, rating
with open("user_ratedmovies.dat") as input:
    user_ratings = input.read().splitlines()
    del user_ratings[0]
input.close()

#operate on user tags -> {user_id:{5:{}, 4.5:{}, 4:{}}}
user_explicit_tags_dict = {}
user_implicit_tags_dict = {}

index = 0

for line in user_ratings:
    line = line.split("\t")
    user_id = line[0]
    movie_id = line[1]
    rating_result = line[2]

    if user_id not in user_explicit_tags_dict:
        user_explicit_tags_dict[user_id] = {}
        for i in np.arange(0, 5.5, 0.5):
            user_explicit_tags_dict[user_id][i] = []
    if user_id not in user_implicit_tags_dict:
        user_implicit_tags_dict[user_id] = {}
        for i in np.arange(0, 5.5, 0.5):
            user_implicit_tags_dict[user_id][i] = []

    #print "length: %s\n" % len(user_explicit_tags_dict)

    #if len(user_explicit_tags_dict) >= 3:
    #    with open("user_explicit_tags_" + str(index), "w") as output1:
    #        json.dump(user_explicit_tags_dict, output1)
    #    output1.close()
    #    with open("user_implicit_tags_" + str(index), "w") as output2:
    #        json.dump(user_implicit_tags_dict, output2)
    #    output2.close()
#
    #    user_explicit_tags_dict = {}
    #    user_implicit_tags_dict = {}
    #    index += 1
    #    continue

    try:
        #generate user features list
        explicit_tags_list = movie_explicit_tags_dict[movie_id]
        implicit_tags_list = movie_implicit_tags_dict[movie_id]
        for item in explicit_tags_list:
            if item not in user_explicit_tags_dict[user_id][float(rating_result)]:
                user_explicit_tags_dict[user_id][float(rating_result)].append(item)

        for item in implicit_tags_list:
            if item not in user_implicit_tags_dict[user_id][float(rating_result)]:
                user_implicit_tags_dict[user_id][float(rating_result)].append(item)

        #user_explicit_tags_dict[user_id][float(rating_result)].extend(explicit_tags_list)
        #user_implicit_tags_dict[user_id][float(rating_result)].extend(implicit_tags_list)
    except:
        continue

with open("user_explicit_tags", "w") as output1:
    json.dump(user_explicit_tags_dict, output1)
output1.close()

with open("user_implicit_tags", "w") as output2:
    json.dump(user_implicit_tags_dict, output2)
output2.close()