# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 13:50:29 2018

@author: Richie
"""

import sys
import youtube_dl
from random import shuffle
from os import listdir
from moviepy.editor import VideoFileClip, concatenate_videoclips
import praw



###############################################################################
#Get the links from top posts of the week
def getlinks(subreddit):
    print("Getting links of tops videos...")
    
    
    links = []
    client_id_sting = ''
    client_secret_string = ''
    user_agent_string = ''

    if client_id_sting == '' or client_secret_string == '' or user_agent_string == '':
        print("Need reddit praw credentials")
    reddit = praw.Reddit(client_id=client_id_sting,
                     client_secret=client_secret_string,
                     user_agent=user_agent_string)


    for submission in reddit.subreddit(subreddit).top(time_filter='week', limit=25):
        if submission.url[len(submission.url)-3:] != ('jpg' or 'png'):
            links.append(submission.url)

    
    return(links)
    
#OLD WAY OF GETTING LINKS FROM REDDIT, DID NOT USE API, JUST PARSED THROUGH HTML. HTTP GET REQUESTS BLOCKED
#NEED:
#import requests
#from time import sleep
    
#        #Attempt to get past reddit's bot block, the status code is 429 for bots
#        r = requests.get("https://old.reddit.com/r/"+subreddit+"/top/?sort=top&t=week")
#        while (r.status_code != 200):
#            print("Failed get request...trying again in 2 seconds")
#            r = requests.get("https://old.reddit.com/r/"+subreddit+"/top/?sort=top&t=week")
#            sleep(2)
#        
#        htmlstuff = r.text
#    
#    
#        #pick out the link address' from html
#        location = 0
#        searchword = "data-url="
#        while (location != -1):
#        
#            location = htmlstuff.find(searchword, location+len(searchword)) #look for "data-url" in html and return the location
#        
#            if (location != -1):
#                #usually it's data-url="www.blah.com"
#                startaddress_loc = location+len(searchword)+1 #everything after the start quote
#                endaddress_loc = htmlstuff.find('\"', startaddress_loc) #find location of the end quote
#                if htmlstuff[endaddress_loc-4:endaddress_loc] not in (".jpg", ".png"): #don't add pictures to the list
#                    if htmlstuff[endaddress_loc-5:endaddress_loc] == ".gifv":
#                        gifv_check = requests.get(htmlstuff[startaddress_loc:endaddress_loc])
#                        gifv_check_text = gifv_check.text
#                        if gifv_check_text[0:4] != "�PNG": #check if imgur link was removed
#                            links.append(htmlstuff[startaddress_loc:endaddress_loc]) #add link to links list
#                    else:
#                        links.append(htmlstuff[startaddress_loc:endaddress_loc]) #add link to links list
###############################################################################


###############################################################################
#Download the videos from links
def download_videos(links, savedir):
    print("Dowloading videos...")
    
    
    for i in range(0, len(links)):
        try:
            #Options for video download, format is mp4, file name is video title, and make new folder named the current date
            #can also have %(title)s, videos saved into folder
            ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best','outtmpl': savedir+'/'+str(i)+'.%(ext)s'}
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([links[i]])
                #info = ydl.extract_info(str([links[i]])) #Future upgrade - have list of file names be titles of videos 
                
        except:
            print("Download failed, skipping video from link: " + links[i])
            continue
        

    return()
###############################################################################


###############################################################################
def combine_videos(savedir):
    print("Combining videos...")
    
    clips = []
    filenames = listdir(savedir)
    shuffle(filenames) #Mix up order videos are put together in video concatenate step
    
    for i in range(0, len(filenames)):
        try:
            clips.append(VideoFileClip(savedir+'/'+filenames[i]))
        except:
            print("Video combine failed, skipping video:" + filenames[i])
            continue
        
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(savedir+'/'+"combined.mp4")
###############################################################################    



def main(subreddit, savedir):
    links = getlinks(subreddit)
    download_videos(links, savedir)
    combine_videos(savedir)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

