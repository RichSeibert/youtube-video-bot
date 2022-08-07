# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 17:27:18 2018

@author: Richie
"""


import get_videos
import upload_video


import datetime
from os import mkdir
from random import randint


title_beginning = ["Most Savage", "The Best", "Best", ""]
preposition = ["for", "of", "in"]
subreddit_list = ["WTF"]#, "Funny", "aww", "ChildrenFallingOver", "HoldMyBeer", "HoldMyCosmo", "ContagiousLaughter", "DamnThatsInteresting"] #List of subreddits to makes videos out of



for i in range(0, len(subreddit_list)):
    
        
    savedir = str(datetime.date.today()) + '/' + subreddit_list[i]
    
    try:
        mkdir(savedir)
    except:
        print("Folder with duplicate name exists")

    
    try:
        print("***Making video***")
        get_videos.main(subreddit_list[i], savedir)
    except:
        print("Critical error while making video for " + subreddit_list[i])
        continue
        
    
    try:
        print("***Uploading video***")
        #Copy client secret file into video folder because it needs to be in the cwd
        #copy2(getcwd() + '/../../' + 'client_secrets.json', getcwd())
        #Upload parameters for youtube api, [file, title, decription, category, keywords, privacy]
        upload_video.main(savedir+'/'+"combined.mp4",
                          title_beginning[randint(0, len(title_beginning))]+' '+subreddit_list[i]+' Videos '+preposition[randint(0, len(preposition))]+' '+str(datetime.datetime.now().strftime("%B")), 
                          "", 
                          "24", 
                          "funny,funny videos,funny fails,aww,cool,coolio,wow,compilation,wtf,lol,savage,dope,hot,fails", 
                          "private")
    except:
        print("Critical error while uploading video for " + subreddit_list[i])
        continue


    