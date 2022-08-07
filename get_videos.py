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
import praw
from subprocess import call, check_output
from shutil import copy2


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
            if (submission.url[len(submission.url)-3:] not in ['jpg', 'png', 'ifv']) and (not submission.over_18):
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
    
    intro_vid_name = "intro1.mp4"
    copy2(intro_vid_name, savedir+'/'+intro_vid_name)
    
    
    
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
    
    
    
    
    
    #Resize videos to have a height of 1080
    print("Resizing videos...")
    for file in filenames:
        try:
            #rc = call(['ffmpeg', '-i', savedir+'/'+file, '-vcodec', 'libx264', '-acodec', 'aac', '-vf', 'scale=-2:1080', '-r', '30', '-b:v', '10M', '-b:a', '128K', savedir+'/resfix/'+file[:len(file)-4]+'.mkv'])
            rc = call(['ffmpeg', '-i', savedir+'/'+file, '-vcodec', 'libx264', '-acodec', 'aac', '-vf', 'scale=-2:1080', '-ac', '2', '-r', '30', '-b:v', '10M', '-b:a', '128K', savedir+'/resfix/'+file[:len(file)-4]+'.mkv'])
        except:
            pass
        
        if(rc!=0):
            print("Failed to resize video", file, "\nError code", rc)
        
    
    
    
    
    
    
    
    
    
    #Add videos to list of videos that should be put into final video
    
    resfix_filenames = listdir(savedir+'/resfix')
    
    #Need txt file for ffmpeg concat command input
    #Format of txt file is "file file_name.mp4, new line, file file_name2.mp4"
    
    #clips_sound.append('file '+'resfix/'+'intro1.mp4') #Include intro video at beggining
    
    
    for file in resfix_filenames:
        #If the duration of all the videos that are going to be combined is over 10 minutes, stop adding
        if(tot_vid_dur>600):
            break
        

        try:
            #Check duration
            print("Attempt to add:", file)
            output = check_output(['ffprobe', '-i', savedir+'/resfix/'+file, '-show_entries', 'format=duration', '-v', 'quiet']).decode()
            vid_dur = int(float((output[19:26])))
            #If the video is over 70 seconds don't add it to the list of videos to combine
            if(vid_dur<70 or file!=intro_vid_name):
                clips_sound.append('\n'+'file '+'resfix/'+file)
                tot_vid_dur += vid_dur
                print("Video duration is now:", tot_vid_dur)
                    
            
        except:
            print("Failed get", file, "duration")

    
    
    
    
    
    #Create txt file
    text_file = open(savedir+'/'+"clips_sound.txt", "w")
    text_file.write('file '+'resfix/'+intro_vid_name[:len(intro_vid_name)-4]+'.mkv')
    text_file.write(''.join(clips_sound))
    text_file.close()
    
	
	#Combine Videos
    try:
        rc = call(['ffmpeg', '-safe', '0', '-f', 'concat', '-i', savedir+'/'+'clips_sound.txt', '-c', 'copy', savedir+'/'+'combined.mp4'])
    except:
        pass
    if(rc!=0):
        print("Failed combine videos", file, "\nError code", rc)
    
    
	
    # # using these ffmpeg calls:

    # # ffmpeg -i 1.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate1.ts
    # # ffmpeg -i 2.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate2.ts
    # # ffmpeg -i "concat:intermediate1.ts|intermediate2.ts" -c copy -bsf:a aac_adtstoasc combined.mp4

    # dir2 = savedir+'/resfix/'
    # concat_command = "concat:"
	
    # print("Concatenate...")
    # for file in clips_sound:
        # try:
            # rc = call(['ffmpeg', '-i', dir2+file, '-c', 'copy', '-bsf:v', 'h264_mp4toannexb', '-f', 'mpegts', savedir+'/'+'intermediate'+file[:file.index('.')]+'.ts'])
            # if(rc==0):
                # concat_command += savedir+'/'+'intermediate'+file[:file.index('.')]+'.ts'
        # except:
            # continue
        
        # if(rc!=0):
            # print("Failed to make ts file", file, "\nError code", rc)
            # continue
	
        # if(clips_sound.index(file)!=len(clips_sound)-1):
            # concat_command += '|'

    # print(concat_command)
    # try:
        # rc = call(['ffmpeg', '-i', concat_command, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', savedir+'/'+'combined.mp4'])
        # #rc = call(['ffmpeg', '-i', concat_command, '-c', 'copy', savedir+'/'+'combined.mp4']) #Possibly able to combine videos without temp files, all files must have same metadata though
    # except:
        # pass

    # if(rc!=0):
        # print("Failed combine videos", file, "\nError code", rc)
        
            
###############################################################################    



def main(subreddit, savedir, slideshow):
    links = getlinks(subreddit)
    download_videos(links, savedir)
    combine_videos(savedir)

if __name__ == "__main__":
    main(argv[1], argv[2], argc[3])
