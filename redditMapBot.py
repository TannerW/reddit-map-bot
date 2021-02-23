#!/bin/python3
import praw
import pandas as pd
import datetime as dt #only if you want to analyze the date created feature
import requests
import os
from dotenv import load_dotenv


def downloadImageFromUrl(url, dirName):
    file_name = url.split("/")
    if len(file_name) == 0:
        file_name = re.findall("/(.*?)", url)
    file_name = file_name[-1]
    if "." not in file_name:
        file_name += ".jpg"
    if dirName != "":
        file_name = dirName+"/"+file_name
    print(file_name)
    r = requests.get(url)
    with open(file_name,"wb") as f:
        f.write(r.content)

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')

# I assigned reddit as the variable name, you can call it whatever you want to.
reddit = praw.Reddit(client_id=CLIENT_ID, 
                     client_secret=CLIENT_SECRET, 
                     user_agent=USER_AGENT)
# IF YOU HAVE ANY SPACES BETWEEN THE CHARACTERS AND THE QUOTES, YOU WILL RECEIVE AN ERROR.
# GOOD: '14_CHARS_IDENTIFIER'
# BAD: ' 14_CHARS_IDENTIFIER '

imgDirName = "images"

if not os.path.exists(imgDirName):
    os.makedirs(imgDirName)

no_subreddit = reddit.subreddit('dndmaps')
hot = no_subreddit.hot(limit=30)
for post in hot:
    url = (post.url)
    print(url)
    if "/gallery/" in url:
        print("HELLO!!!")
        submission = reddit.submission(url=url)
        #r = requests.get(url)
        #print(r.content)
        print(submission)
        for i in range(len(submission.mod.thing.gallery_data['items'])):
            media_id = submission.mod.thing.gallery_data['items'][i]['media_id']
            currGalleryImgUrl = "https://i.redd.it/"+media_id+".jpg"
            print(currGalleryImgUrl)
            dirName = imgDirName+"/"+submission.id
            if not os.path.exists(dirName):
                os.makedirs(dirName)
            downloadImageFromUrl(currGalleryImgUrl, dirName)
    else:
        downloadImageFromUrl(url, imgDirName)