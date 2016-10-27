import json
import re
import operator
import random

num_random = 2
limit = 1;

movie_user = {} # movie_id, number of raters
movie_popularity = {}
num_user = 0
output = {}

num_relevance = 0 # all movies, e per user
num_unexpectedness = 0
num_serendipity = 0

relevent = False
unexpect = False

#read in the rating database
with open("rating_database_test.txt", "rb") as input1:
    lines = json.loads(input1.read())
input1.close()

#generate number of rater for each movie -> if it is unexpecteded or not
for user_id in lines:
    num_user += 1
    for movie_id in lines[user_id]:
        if movie_id not in movie_user:
            movie_user[movie_id] = 1
        else:
            movie_user[movie_id] += 1

#generate average popularity rate
sorted_movie_user = sorted(movie_user.items(), key=operator.itemgetter(1))
average_popularity = sorted_movie_user[5055][1]

#genenrate popularity for each movie
for movie_id in movie_user:
    if float(movie_user[movie_id]) > average_popularity:
        movie_popularity[movie_id] = 1
    else:
        movie_popularity[movie_id] = 0

#random pick
for user_id in lines:
    length = len(lines[user_id])
    relevance = 0.0
    if length > limit:
        sum = 0.0
        for index in lines[user_id]:
            sum = sum + float(lines[user_id][index])
        #average rating for that user
        average = float(sum) / length
        rates = []
        for key, rate in lines[user_id].iteritems():
            temp = [key, rate]
            rates.append(temp)
        randoms = random.sample(range(0, length), num_random)
        for index_selected in randoms:
            rate_temp = float(rates[index_selected][1])
            popular_temp = int(float(movie_popularity[rates[index_selected][0]]))
            if rate_temp > average:
                num_relevance = num_relevance + 1
                relevent = True
            if popular_temp == 0:
                num_unexpectedness = num_unexpectedness + 1
                unexpect = True
            if relevent and unexpect:
                num_serendipity = num_serendipity + 1
            relevent = False
            unexpect = False

rate_relevance = float(num_relevance) / (num_random * num_user)
rate_unexpectedness = float(num_unexpectedness) / (num_random * num_user)
rate_serendipitous = float(num_serendipity) / (num_random * num_user)
result = [rate_relevance, rate_unexpectedness, rate_serendipitous]

with open("rating_result.txt", "wb") as output1:
    json.dump(result, output1)
output1.close()
