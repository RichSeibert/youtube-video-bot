# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 21:53:47 2018

@author: Richie
"""

'''from random import shuffle
from os import listdir
from moviepy.editor import VideoFileClip, concatenate_videoclips
from os import chdir


def combine_videos():
    print("Combining videos...")
    
    clips = []
    filenames = listdir()
    shuffle(filenames) #Mix up order videos are put together in video concatenate step
    
    for i in range(0, len(filenames)):
        clips.append(VideoFileClip(filenames[i]))
        
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile("combined.mp4")
    
    
chdir('2018-11-03WTF' + '/')    
combine_videos()'''

from oauth2client.tools import argparser
print("g")
argparser.add_argument("--file", required=True, help="Video file to upload")

args = argparser.parse_args()

print(args)
print("Done")