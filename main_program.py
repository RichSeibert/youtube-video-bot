# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 17:27:18 2018

@author: Richie


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION:
Downloads videos from top weekly videos on certain subreddits, compiles them into
one video and uploads to youtube    
    
This program runs through a loop and calls the get_videos and upload_video programs passing
needed parameters:
    title_beginning - array of phrases for the beginning of youtube video's title
    preposition - array of prepositions to use in the youtube video's title
    subreddit_list - what subreddits to make videos of
    
This program needs the following files to be in the same directory as the main program:
    logo.png - logo in the bottom left of all videos
    intro1.mp4 - Intro video
    get_videos.py
    upload_videos.py
    main_program.py-oauth2.json
    client_secrets.json
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""



import get_videos
import upload_video

import datetime
from os import makedirs
from random import randint
from time import sleep
#from shutil import rmtree



#Variables
###############################################################################
title_beginning = ["Chicken Peanut:"]

preposition = ["||"]

#Has to match index of subreddit list
title_noun = [
             "WTF", 
             "Funny",
             "Cute", 
             "Fast Worker",
             "Live Stream Fail"
             ]

#List of subreddits to makes videos out of
subreddit_list = [
                 ["WTF"],
                 ["Funny", "HoldMyBeer", "HoldMyCosmo", "ContagiousLaughter"],
                 ["aww", "ChildrenFallingOver"],
                 ["FastWorkers"],
                 ["LivestreamFail"]
                 ]
                 
#Slideshow? Slideshow option will take images and gifs from the subreddit(s) and overlay audio of a TTS reading of the submition title
slideshow = [
            False,
            False,
            False,
            False,
            False,
            True
            ]
###############################################################################






#Pick subreddit that matches the day of week
i = datetime.datetime.today().weekday() % len(title_noun)

date_folder = str(datetime.date.today())
savedir = date_folder + '/' + title_noun[i]
resfixfolder = savedir+'/'+'resfix'







#Make new folder(s) for videos, copy intro video into temp files
try:
    makedirs(resfixfolder)
except:
    print("Folder with duplicate name exists")



#Get videos and compile
try:
    print("***Making video***")
    get_videos.main(subreddit_list[i], savedir, slideshow[i])
except:
    print("Critical error while making video for " + str(subreddit_list[i]))

    

  
#Upload
for attempt in range(3): #If the video fails to upload, it will try to upload 2 more times with 5 second breaks inbetween
    try:
        print("***Uploading video***")
        #Upload parameters for youtube api, [file, title, decription, category, keywords, privacy]
        #For the description 'PHP_EOL' is for a newline
        upload_video.main(
                      #File dir
                      savedir+'/'+"combined.mp4",
                      #Title
                      title_beginning[randint(0, len(title_beginning))]+' '+title_noun[i]+' Videos '+preposition[randint(0, len(preposition))]+' '+str(datetime.datetime.now().strftime("%B")),
                      #Description
                      "Like, comment, subscribe" + 
                      '                                                                                                                              ' +
                      "Intro music:" + 
                      '                                                                                                                                                      ' + 
                      "Road Trip by Joakim Karud https://soundcloud.com/joakimkarud" + 
                      '                                                                                                                              ' + 
                      "Music promoted by Audio Library https://youtu.be/vpssnpH_H4c",
                      #Category
                      "24",
                      #Keywords
                      "funny,funny videos,funny fails,aww,cool,coolio,wow,compilation,wtf,lol,savage,dope,hot,fails",
                      #Privacy
                      "public"
                      )
        
        break #video uploaded sucessfully, don't attempt to upload again
    
    except:
        print("Critical error while uploading video for " + str(subreddit_list[i]) + ". Attempt " + str(attempt))
        sleep(5) #Wait 5 seconds before trying to upload again



#Write to log file feature
sleep(10)
#Delete folder
#rmtree(date_folder)
exit()
