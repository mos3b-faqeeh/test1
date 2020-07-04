from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from sklearn.feature_extraction.text import CountVectorizer


import requests
import json
import pandas as pd
import numpy as np

import pdb;





def extract_hash_tags(s):
  return [i  for i in s.split() if i.startswith("#") ]


def video_count(posts):
    count=0
    img=0

    for post in posts:
        if post["node"]["is_video"]:
            count = count + 1
        else:
            img=img+1
    return count,img


def likes_count(posts):
    count=0
    for post in posts:
        count = count + post["node"]["edge_liked_by"]["count"]

    return count

def hashtagTracker(request):

    if request.GET.get('num1'):
        hashtag = request.GET['num1']
        # print("\033[1m" + "Scraping/analyzing posts for " + hashtag + "..." + "\033[0m")
        page = requests.get("https://www.instagram.com/explore/tags/" + hashtag[1:])
        posts = json.loads(page.text[page.text.find("window._sharedData") + 21: page.text.find("};</script>") + 1])
        postCount = posts["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["count"]
        minTopLikes = 0
        meanTopLikes = 0
        medianRecentTime = 0
        percentRecentVids = 0

        if postCount != 0:
            i = 0
            totalTop = 0
            for post in posts["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_top_posts"][
                "edges"]:
                if post["node"]["edge_liked_by"]["count"] < minTopLikes or i == 0:
                    minTopLikes = post["node"]["edge_liked_by"]["count"]
                totalTop += post["node"]["edge_liked_by"]["count"]
                i += 1
            meanTopLikes = totalTop / i
            print("Looked at " + str(i) + " top posts...")

            j = 0
            totalTimeList = []
            totalRecentVids = 0
            for post in posts["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]:
                totalTimeList.append(post["node"]["taken_at_timestamp"])
                if post["node"]["is_video"]:
                    totalRecentVids += 1

                j += 1
                if j == 100:
                    break
            if j != 1:
                medianRecentTime = np.median(np.diff(sorted(totalTimeList)))
            percentRecentVids = (totalRecentVids / j) * 100
            print("Looked at " + str(j) + " recent posts...")
            tags = []

            for post in posts["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_related_tags"][
                "edges"]:
                tags.append(post["node"]["name"])

            ExtraTags = []
            for post in posts["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_top_posts"][
                "edges"]:
                ExtraTags.append((post["node"]["edge_media_to_caption"]["edges"][0]["node"]))
            print((ExtraTags))

            caption = []
            for sentance in ExtraTags:
                caption.append(sentance['text'])
            # print(caption)

            arrayOfHashs = []
            for hash in caption:
                hash1 = ''.join(hash)
                arrayOfHashs.append(extract_hash_tags(hash1))

            print(arrayOfHashs)

            ListOfHashs = [y for x in arrayOfHashs for y in x]
            print(ListOfHashs)

            count_model = CountVectorizer(ngram_range=(1, 1))  # default unigram model
            # count_model.min_df=2
            count_model.max_features = 15
            count_model.stop_words = ['01', '05', '2layersprotection']
            X = count_model.fit_transform(ListOfHashs)
            AIRec = count_model.get_feature_names()

            ListOfHashsText = ' '.join(ListOfHashs)
            print(AIRec)

            count_list = X.toarray().sum(axis=0)
            count_list = dict(zip(count_model.get_feature_names(), count_list))
            hashRankValues = list(count_list.values())
            hashRankWords = list(count_list.keys())

            videoCount, ImgCount = video_count(
                posts["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"])
            LikesCount = likes_count(
                posts["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"])

            hashRankWords = str(hashRankWords).replace("\'", "\"")






        else:
            print("\033[93m" + "No posts exist for this hashtag" + "\033[0m")

        # outputFile.write(hashtag + "," + str(postCount) + "," + str(minTopLikes) + "," + str(meanTopLikes) + "," + str(
        # medianRecentTime) + "," + str(percentRecentVids) + "\n")

        return render(request, "dashboard.html",
                      {'hashtag': hashtag, 'postCount': postCount, 'minTopLikes': minTopLikes,
                       'meanTopLikes': meanTopLikes,
                       'medianRecentTime': medianRecentTime,
                       'percentRecentVids': percentRecentVids, 'tags': tags, 'AIRec': AIRec, 'videoCount': videoCount,
                       'LikesCount': LikesCount, 'totalTop': totalTop, 'ImgCount': ImgCount,
                       'ListOfHashsText': ListOfHashsText, 'hashRankWords': hashRankWords,
                       'hashRankValues': hashRankValues})
        res=0
    else :

        return render(request, "dashboard.html",
                      {'hashtag': 0, 'postCount': 0, 'minTopLikes': 0,
                       'meanTopLikes': 0,
                       'medianRecentTime': 0,
                       'percentRecentVids': 0, 'tags': 0, 'AIRec': 0, 'videoCount': 0,
                       'LikesCount': 0, 'totalTop': 0, 'ImgCount': 0,
                       'ListOfHashsText': 0, 'hashRankWords': 0,
                       'hashRankValues': 0})







