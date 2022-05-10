import pygame, sys
from pyvidplayer import Video
from os.path import exists 
import datetime
import math
from time import sleep
import configparser
import wget
pygame.init()

def get_seconds():
    now = datetime.datetime.now()
    midnight = now.replace(hour=0,minute=0,second=0)
    second = (now - midnight).seconds
    return second

print(get_seconds())



happy_hr_end=48500
happy_hr_begin=47179
base_url = 'https//:'
base_dir = 'Assets/'
image_display_time = 60
image_h_display_time = 60

video_duration = []
video_h_duration=[]

show_video = False

items = 10

flag = True

# videoPath_defaut  = ['Assets/1.mp4','Assets/2.mp4','Assets/3.mp4','Assets/4.mp4','Assets/5.mp4','Assets/6.mp4','Assets/7.mp4','Assets/8.mp4','Assets/9.mp4','Assets/10.mp4']
# videoPath_happy_defaut = ['Assets/1h.mp4','Assets/2h.mp4','Assets/3h.mp4','Assets/4h.mp4','Assets/5h.mp4','Assets/6h.mp4','Assets/7h.mp4','Assets/8h.mp4','Assets/9h.mp4','Assets/10h.mp4']
# imagePath_defaut  = ['Assets/1.png','Assets/2.png','Assets/3.png','Assets/4.png','Assets/5.png','Assets/6.png','Assets/7.png','Assets/8.png','Assets/9.png','Assets/10.png']
# imagePath_happy_defaut  = ['Assets/1h.png','Assets/2h.png','Assets/3h.png','Assets/4h.png','Assets/5h.png','Assets/6h.png','Assets/7h.png','Assets/8h.png','Assets/9h.png','Assets/10h.png']

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

def download_resources(path):
    for i in range():
        url = base_url + videonames_defaut[i]
        wget.download(url, (base_dir) + videonames_defaut[i] )
        url = base_url + videonames_happy_defaut[i]
        wget.download(url, (base_dir) + videonames_happy_defaut[i] )
        url = base_url + imagenames_defaut[i]
        wget.download(url, (base_dir) + imagenames_defaut[i] )
        url = base_url + imagenames_happy_defaut[i]
        wget.download(url, (base_dir) + imagenames_happy_defaut[i] )

def get_seek(timeT,_image,_image_display_time,_video,_video_duration): # this takes the time spent in the loop, total images and total videos and the point the loop should be in at a particular time
    elapsed_time = 0
    video_flag = True
    _count = 0
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
            print('closing')
            play = False
 
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()
                print('closing')
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
 
screen = pygame.display.set_mode(screensize,pygame.NOFRAME)

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
    print ("loop")

    if happy_hour():
        get_sync(image_h_display_time,video_h_duration,image_h,video_h)
    else: 
        get_sync(image_display_time,video_duration,image,video)
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:# if you close the window
                Run = False #exit game 
