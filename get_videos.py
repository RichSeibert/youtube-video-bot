# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 13:50:29 2018

@author: Richie


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION:
Gets links of the top videos of the week from a specific reddit subreddit,
downloads videos from the links from any hosting site supported by the youtube_dl library,
and then uses moviepy to edit and concatinate the videos together
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""



from sys import argv
import youtube_dl
from random import shuffle
from os import listdir
from time import sleep
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip
import praw
from subprocess import Popen, check_output



###############################################################################
#Get the links from top posts of the week
def getlinks(subreddit):
    print("Getting links of tops videos...")
    
    
    links = []
    limit = int(60/len(subreddit)) #How many links to ATTEMPT to get, split bewtween subreddits in group
    
    reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='')

    for sub in subreddit:
        for submission in reddit.subreddit(sub).top(time_filter='week', limit=limit):
            #Do not get add urls onto the list if they are picutres, gifs, or NSFW
            if (submission.url[len(submission.url)-3:] not in ['jpg', 'png', 'gif', 'ifv']) and (not submission.over_18):
                #print(submission.url[len(submission.url)-3:])
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
    
    video_len = 0
    video_len_tot = 0
    
    for i in range(0, len(links)):
        try:
            #Options for video download, format is mp4, file name is video title, and make new folder named the current date
            #can also have %(title)s, videos saved into folder
            ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best','outtmpl': savedir+'/'+str(i)+'.%(ext)s'}
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    #Get duration of video from link and add to video length counter
                    video_len = ydl.extract_info(links[i], download=False)['duration']
                    #If the video is over 65 seconds do not download or add to counter
                    if (video_len > 65):
                        continue
                    
                    video_len_tot += video_len
                    
                except:
                    #If getting video duration doesn't work just add 30 seconds to total length counter as an approximation
                    video_len_tot += 30
                
                
                #Only download 15 minutes of video
                if (video_len_tot < 900):
                    ydl.download([links[i]])
                    #info = ydl.extract_info(str([links[i]])) #Future upgrade - have list of file names be titles of videos 
                
        except:
            print("Download failed, skipping video from link:", links[i])
        
###############################################################################


###############################################################################
#Chance height of video to 1080, combine all them and add a water mark to the final video
def combine_videos(savedir):
    print("Editing and combining videos...")
    
    tot_vid_dur = 0
    clips_sound = []
    #clips_nosound = []
    filenames = listdir(savedir)
    filenames.remove('resfix') #take out folder of list
    shuffle(filenames) #Mix up order videos are put together in video concatenate step
    #audio_chk = [1]*len(filenames) #List for keeping track of what videos have sound or not, 0=no sound 1=sound, assume all videos have sound
    
    '''
    #Check if videos have audio and put into audio_chk, don't check gifs
    for index, file in enumerate(filenames):
        if file[len(file)-3:] not in ['gif', 'ifv']:
            p = check_output(['ffprobe', '-loglevel', 'error', '-show_entries', 'stream=codec_type', '-of', 'csv=p=0', file])
            sleep(5)
            if 'audio' not in str(p):
                audio_chk[index]=0
    '''
    
    print("Resizing videos...")
    #Resize videos to have a height of 1080
    for file in filenames:
        try:
            Popen(['ffmpeg', '-i', savedir+'/'+file, '-vf', 'scale=-2:1080', savedir+'/resfix/'+file, '-hide_banner'])
            sleep(90)
            
        except:
            print("Failed to resize", file)
    
        
    
    #Include intro video
    clips_sound.append(VideoFileClip('intro1.mp4'))
    
    for file in filenames:
        #If the duration of all the videos that are going to be combined is over 10 minutes, stop adding
        if(tot_vid_dur>600):
            break
        
        for attempt in range(3): #Try 3 times to append
            try:
                clip = VideoFileClip(savedir+'/resfix/'+file)
                vid_dur = int(clip.duration)
                
                #If the video is over 70 seconds don't add it to the list of videos to combine
                if(vid_dur<70):
                    clips_sound.append(clip)
                    tot_vid_dur += vid_dur
                    
                break
            
            except:
                print("Video combine failed, skipping video:", file)
                sleep(5)
    
    
    #Concatinate videos and add watermark
    print("Concatenate and adding watermark...")
    final_clip = concatenate_videoclips(clips_sound, method="compose")
    logo = (ImageClip("logo.png")
          .set_start(7.5)
          .set_duration(final_clip.duration)
          .resize(height=50) # if you need to resize...
          .margin(right=0, top=0, opacity=0) # (optional) logo-border padding
          .set_pos(("right","bottom")))
    final_clip = CompositeVideoClip([final_clip, logo])
    final_clip.write_videofile(savedir+'/'+"combined.mp4")
    
###############################################################################    



def main(subreddit, savedir):
    links = getlinks(subreddit)
    download_videos(links, savedir)
    combine_videos(savedir)

if __name__ == "__main__":
    main(argv[1], argv[2])

