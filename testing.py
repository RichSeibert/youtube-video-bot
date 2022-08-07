# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 21:53:47 2018

@author: Richie
"""

# from shutil import copy2
# import datetime
# from os import mkdir, getcwd, chdir, system, listdir
# from time import sleep
# from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip
# import praw
# import youtube_dl
from gtts import gTTS
import os


tts = gTTS(text='Ocean Sunfish are the heaviest bony fish! They can weigh up to 1,000 kg (2,204 lbs). They are very curious and frequently approach divers and boats. ', lang='en')
tts.save("good.mp3")
#os.system("mpg321 good.mp3")



# rc = call(['ffmpeg', '-i', 'intro1.mp4', '-vcodec', 'libx264', '-acodec', 'libvo_aacenc', '-vf', 'scale=-2:1080', '-r', '30', '-b:v', '10M', '-b:a', '128K', 'out.mp4', '-hide_banner'])



#call(['ffprobe', '-i', '<file>', '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv="p=0"'])





'''
w = "hello"
r = call(['ffmpeg', '-i', "intro2.mp4", '-vf', 'scale=-2:1080', "22.mp4", '-hide_banner'])
print("Failed", r, w, "\n", r)



p = check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', '0.mp4'])
print(p)




list1 = [0,1,1,1]
list1 = list1 * 2
list1.remove('a')
list1[1]='1'
for index, w in enumerate(list1):
    print(index, w)
'''
'''
p = check_output(['ffprobe', '-loglevel', 'error', '-show_entries', 'stream=codec_type', '-of', 'csv=p=0', '4.mp4'])
if 'audio' in str(p):
    print(p)




i = {'wtf':['wtf','gross'],
     'funny':['funny','aww']}

limit = int(61/len(i))
print(limit)


reddit = praw.Reddit(client_id='z8G9VkdKwTSqgw',
                     client_secret='u0rILJoBozB57UW-lszZ_CCaBYQ',
                     user_agent='peanutchickenbot')


for submission in reddit.subreddit('wtf').top(time_filter='week', limit=50):
    #print(submission.over_18)
    if (submission.url[len(submission.url)-3:] not in ['jpg', 'png', 'gif', 'ifv']) and (not submission.over_18):
        print(submission.over_18)
        print(submission.url[len(submission.url)-3:])







savedir = '2018-12-22/WTF/'


Popen(['ffmpeg', '-i', '2018-12-22/WTF/0.mp4', '-vf', 'scale=-2:1080', '2018-12-22/WTF/0n.mp4', '-hide_banner'])
Popen(['ffmpeg', '-i', '2018-12-22/WTF/2.mp4', '-vf', 'scale=-2:1080', '2018-12-22/WTF/1n.mp4', '-hide_banner'])



clips = []




files = ['0n.mp4', '1n.mp4']

for i in range(2):
    clips.append(VideoFileClip(savedir+files[i]))

print(clips)
print("Concatenate...")
final_clip = concatenate_videoclips(clips, method="compose")
final_clip.write_videofile(savedir+"combined.mp4")



Popen(['ffmpeg','-i', '0.mp4', '-i', '1.mp4', '-filter_complex', '[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[outv][outa]', '-map', '[outv]', '-map', '[outa]', 'merged.mp4'])






ffmpeg -i input1.mp4 -i input2.webm -i input3.mov \
-filter_complex "[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[outv][outa]" \
-map "[outv]" -map "[outa]" output.mkv

Popen(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', 'input.mp4'])

Popen(['ffmpeg', '-i', '0.mp4', '-i', '1.mp4', '-i', '-filter complex', '[0:v:0] [0:a:0] [1:v:0] [1:a:0] concat=n=2:v=1:a=1 [v] [a]', '-map [v]', '-map [a]', 'output_video.mp4'])

'''
