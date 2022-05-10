import pygame
import configparser
from pyvidplayer import Video
from os.path import exists 
import datetime
import math
from time import sleep
import configparser
import wget
import urllib.request
import os


pygame.init()
config = configparser.ConfigParser()


video_duration = []
video_h_duration=[]

items = 10

flag = True


videonames_defaut  = ['1.mp4','2.mp4','3.mp4','4.mp4','5.mp4','6.mp4','7.mp4','8.mp4','9.mp4','10.mp4']
videonames_happy_defaut = ['1h.mp4','2h.mp4','3h.mp4','4h.mp4','5h.mp4','6h.mp4','7h.mp4','8h.mp4','9h.mp4','10h.mp4']
imagenames_defaut  = ['1.png','2.png','3.png','4.png','5.png','6.png','7.png','8.png','9.png','10.png']
imagenames_happy_defaut  = ['1h.png','2h.png','3h.png','4h.png','5h.png','6h.png','7h.png','8h.png','9h.png','10h.png']


videoPath =[]
videoPath_happy=[]
imagePath= []
imagePath_happy=[]

video = []
image = []
video_h = []
image_h = []




def get_seconds():
    now = datetime.datetime.now()
    midnight = now.replace(hour=0,minute=0,second=0)
    second = (now - midnight).seconds
    return second

print(get_seconds())

def download_resources(_base_url,_base_dir,_imagenames_defaut,_videonames_defaut,_imagenames_happy_defaut,_videonames_happy_defaut):
    for i in range():
        url = _base_url + _videonames_defaut[i]
        wget.download(url, (_base_dir) + _videonames_defaut[i] )
        url = _base_url + _videonames_happy_defaut[i]
        wget.download(url, (_base_dir) + _videonames_happy_defaut[i] )
        url = _base_url + _imagenames_defaut[i]
        wget.download(url, (_base_dir) + _imagenames_defaut[i] )
        url = _base_url + _imagenames_happy_defaut[i]
        wget.download(url, (_base_dir) + _imagenames_happy_defaut[i] )

def compare_asset(_imageNames,_videoNames,_imageHnames,_videoHnames):
    for _image in _imageNames:
        if exists(base_dir+_image):
            file = urllib.request.urlopen(base_url + _image )
            local_file = os.path.getsize(base_dir + _image)
            if local_file != file.length():
                return False
    for _video in _videoNames:
        if exists(base_dir+_video):
            file = urllib.request.urlopen(base_url + _video )
            local_file = os.path.getsize(base_dir + _video)
            if local_file != file.length():
                return False
    for _image in _imageHnames:
        if exists(base_dir+_image):
            file = urllib.request.urlopen(base_url + _image )
            local_file = os.path.getsize(base_dir + _image)
            if local_file != file.length():
                return False
    for _video in _videoHnames:
        if exists(base_dir+_video):
            file = urllib.request.urlopen(base_url + _video )
            local_file = os.path.getsize(base_dir + _video)
            if local_file != file.length():
                return False            




def configure():
    global happy_hr_end
    global happy_hr_begin
    global base_url
    global base_dir 
    global image_display_time
    global image_h_display_time 
    global broker
    config['DEFAULT'] = {
                      'happy_hr_begin': happy_hr_begin,
                      'happy_hr_end': happy_hr_end,
                      'interval_time': image_display_time,
                      'interval_time_happy_hour': image_h_display_time,
                      'base_url': base_url,
                      'base_dir': base_dir,
                      'broker': broker
                      
                      }

    with open('.config.ini', 'w') as configfile:
        config.write(configfile)

def get_configuration():
    global happy_hr_end
    global happy_hr_begin
    global base_url
    global base_dir 
    global image_display_time
    global image_h_display_time 
    global broker

    config.read('.config.ini')
    happy_hr_begin = config.getint('DEFAULT', 'happy_hr_begin',fallback =50000 )
    happy_hr_end = config.getint('DEFAULT', 'happy_hr_end',fallback = 50000)
    image_display_time = config.getint('DEFAULT', 'interval_time',fallback =60 )
    image_h_display_time = config.getint('DEFAULT', 'interval_time_happy_hour',fallback =60 )
    base_url = config.get('DEFAULT', 'base_url',fallback ='none')
    base_dir = config.get('DEFAULT', 'base_dir',fallback = 'Assets')
    broker = config.get('DEFAULT', 'broker',fallback = 'test.mosquitto.org' )
    


def get_seek(timeT,_image,_image_display_time,_video,_video_duration): # this takes the time spent in the loop, total images and total videos and the point the loop should be in at a particular time
    elapsed_time = 0
    video_flag = True
    _count = 0
    if len(_video) >= len(_image):
        num = len(_video)
    else:
        num = len(_image)  
    for i in range(num):
        if i<len(_video):
            elapsed_time += _video_duration[i]
            if elapsed_time >= timeT:
                _count = i
                video_flag = True
                remaining_time = elapsed_time -timeT
                seek_time = _video_duration[i] -remaining_time
                for i in range(len(_video)):
                    _video[i].close()
                return seek_time,_count,video_flag
        if i<len(_image):
             elapsed_time +=_image_display_time
             if elapsed_time >= timeT:
                _count = i
                video_flag = False
                remaining_time = elapsed_time -timeT
                for i in range(len(_video)):
                    _video[i].close()

                return remaining_time,_count,video_flag

def playvid(path,time):
    global screensize
    vid = Video(path)
    vid.set_size(screensize)
    vid.seek(time)
    play =True
    while play:
        vid.draw(screen, (0, 0))
        pygame.display.update()
        if vid.get_playback_data()["time"] >= (vid.get_file_data()["duration"]-1):
            vid.close()
            play = False
 
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()
                play = False

def happy_hour():
    t0 = get_seconds()
    hflag = True
    if t0 >= happy_hr_begin and t0 <= happy_hr_end :
        hflag = True
    else :
        hflag = False
    return hflag        

def get_sync(image_display_time,_video_duration,imagef,videof):
    sleep(1)
    global current 
    global flag
    total_video_time=0
    t0 = get_seconds()
    for i in range(len(_video_duration)):
        total_video_time += _video_duration[i]

    
    if happy_hour():
        total_time = total_video_time + (len(imagef)*image_display_time)
        number_of_loops  = (t0-happy_hr_begin)/total_time   
        current_loop_time = (number_of_loops-math.floor(number_of_loops)) * total_time
        
    else:
        total_time = total_video_time + (len(imagef)*image_display_time)
        number_of_loops  = t0/total_time   
        current_loop_time = (number_of_loops-math.floor(number_of_loops)) * total_time
    
    rtime,current,flag = get_seek(current_loop_time,imagef,image_display_time,videof,_video_duration)


    print('seek params: ',rtime,current,flag)
    print('num of loops: ',number_of_loops)
    print('floor of loops: ',math.floor(number_of_loops))
    print("Total length :",total_time)
    print("current loop time: ", current_loop_time)

    if flag :
        playvid(videoPath[current],rtime)
        flag = False
    else :
        screen.blit(image[current],(0,0))  
        pygame.display.update()     
        sleep(rtime)
        flag =True
        current += 1
            
get_configuration()



for i in range(items):

    if exists(base_dir+videonames_defaut[i]):
        videoPath.append(base_dir+videonames_defaut[i])
        video.append(None)
        video_duration.append(None)
    if exists(base_dir + videonames_happy_defaut[i]):
        videoPath_happy.append(base_dir + videonames_happy_defaut[i])
        video_h.append(None)
        video_h_duration.append(None)
        
    if exists(base_dir + imagenames_defaut[i]):
        imagePath.append(base_dir + imagenames_defaut[i])
        image.append(None)
    if exists(base_dir + imagenames_happy_defaut[i]):
        imagePath_happy.append(base_dir + imagenames_happy_defaut[i])    
        image_h.append(None)      

current=0
wininfo = pygame.display.Info()
screensize = (wininfo.current_w, wininfo.current_h)
width, height = 900, 900
 
screen = pygame.display.set_mode((width, height),pygame.NOFRAME)

for i in range (len(video)):
    video[i] = Video(videoPath[i])
    video[i].toggle_pause() 
    video_duration[i] = video[i].get_file_data()["duration"] 
    video[i].close()
for i in range (len(image)):
    image[i] = pygame.image.load(imagePath[i])
    image[i] = pygame.transform.scale(image[i], (screensize))

for i in range (len(video_h)):
    video_h[i] = Video(videoPath_happy[i])
    video_h[i].toggle_pause() 
    video_h_duration[i] = video_h[i].get_file_data()["duration"] 
    video_h[i].close()
for i in range (len(image_h)):
    image_h[i] = pygame.image.load(imagePath_happy[i])
    image_h[i] = pygame.transform.scale(image_h[i], (screensize))
 



if happy_hour():
    print("happy begining")
    get_sync(image_h_display_time,video_h_duration,image_h,video_h)
    print ("happy")
else: 
    get_sync(image_display_time,video_duration,image,video)
    print ("not happy")

Run =True

while Run:

    if happy_hour():
        get_sync(image_h_display_time,video_h_duration,image_h,video_h)
    else: 
        get_sync(image_display_time,video_duration,image,video)
            

