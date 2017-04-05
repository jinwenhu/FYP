import graph
import json
import numpy as np

#load movie explicit and implicit files
with open("data/movie_explicit_tags", "r") as input1:
    movie_explicit_tags_dict = json.load(input1)
input1.close()

with open("data/movie_implicit_tags", "r") as input2:
    movie_implicit_tags_dict = json.load(input2)
input2.close()

#user rating database -> user_id, movie_id, rating
with open("data/user_ratedmovies.dat") as input:
    user_ratings = input.read().splitlines()
    del user_ratings[0]
input.close()

#operate on user tags -> {user_id:{feature:score}}
user_explicit_tags_dict = {}
user_implicit_tags_dict = {}

index = 0

for line in user_ratings:
    line = line.split("\t")
    user_id = int(line[0])
    movie_id = int(line[1])
    rating_result = float(line[2]) - 2.5

    if user_id not in user_explicit_tags_dict:
        user_explicit_tags_dict[user_id] = {}
    if user_id not in user_implicit_tags_dict:
        user_implicit_tags_dict[user_id] = {}
    try:

        print "%s" % len(user_explicit_tags_dict)

        #generate user features list
        explicit_tags_list = movie_explicit_tags_dict[movie_id]
        implicit_tags_list = movie_implicit_tags_dict[movie_id]

        for item in explicit_tags_list:
            if item not in user_explicit_tags_dict[user_id]:
                user_explicit_tags_dict[user_id][item] = rating_result
            else:
                user_explicit_tags_dict[user_id][item] = np.mean([float(user_explicit_tags_dict[user_id][item]), rating_result])

        for item in implicit_tags_list:
            if item not in user_implicit_tags_dict[user_id]:
                user_implicit_tags_dict[user_id][item] = rating_result
            else:
                user_implicit_tags_dict[user_id][item] = np.mean([float(user_implicit_tags_dict[user_id][item]), rating_result])
        #user_explicit_tags_dict[user_id][float(rating_result)].extend(explicit_tags_list)
        #user_implicit_tags_dict[user_id][float(rating_result)].extend(implicit_tags_list)

    except:
        continue

with open("data/user_explicit_tags", "w") as output1:
    json.dump(user_explicit_tags_dict, output1)
output1.close()

with open("data/user_implicit_tags", "w") as output2:
    json.dump(user_implicit_tags_dict, output2)
output2.close()