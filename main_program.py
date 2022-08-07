# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 17:27:18 2018

@author: Richie
"""


import get_videos
import upload_video

import datetime
from os import chdir, mkdir

flag = 0

subreddit_list = ["wtf"] #List of subreddits to makes videos out of
savedir = str(datetime.date.today()) + subreddit_list[0] + '/'
try:
    mkdir(savedir)
except:
    flag = 1
chdir(savedir)

if flag == 0:
    get_videos.main(subreddit_list)
upload_video.main("combined.mp4", "Test Title", "Test", "24", "funny,cool,wow,compilation,wtf,reddit,lol", "public")
