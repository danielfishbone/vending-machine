#!/usr/bin/python
import configparser
import sys
import paho.mqtt.client as mqtt
from pymediainfo import MediaInfo
from os.path import exists 
import datetime
import math
from time import sleep
import wget
import urllib.request
import os
from errno import ENOENT
import vlc
import pygame



config = configparser.ConfigParser()

#*********************************************MQTT SETTINGS********************************
url_top = "machine/url"
time_top = "machine/Interval1"
HH_time_top = "machine/Interval2"
HH_from__top = "machine/H_from"
HH_till__top = "machine/H_till"
shutdown_top = "machine/shutdown"
change_top = "machine/CO"
broker = "test.mosquitto.org"
port = 1883

#*********************************************************************************************
player = vlc.MediaPlayer()
pygame.init()
screen_size = pygame.display.Info()
screen_h = screen_size.current_h #hieght of current screen
screen_w = screen_size.current_w #width of current screen

#comment out the following lines to go full screen
# screen_h = 768
# screen_w = 1399

#comment out the following line and uncomment the next to remove frame 
screen = pygame.display.set_mode((screen_w,screen_h),pygame.RESIZABLE)
# screen = pygame.display.set_mode((screen_w,screen_h),pygame.NOFRAME)
win_id = pygame.display.get_wm_info()['window']
pygame.mixer.quit()

#************************************Pygame Settings ******************************************
video_duration = []
video_h_duration=[]

items = 10
Run =True
# flag = True


videonames_defaut  = ['1.mp4','2.mp4','3.mp4','4.mp4','5.mp4','6.mp4','7.mp4','8.mp4','9.mp4','10.mp4']
videonames_happy_defaut = ['h1.mp4','h2.mp4','h3.mp4','h4.mp4','h5.mp4','h6.mp4','h7.mp4','h8.mp4','h9.mp4','h10.mp4']
imagenames_defaut  = ['1.jpg','2.jpg','3.jpg','4.jpg','5.jpg','6.jpg','7.jpg','8.jpg','9.jpg','10.jpg']
imagenames_happy_defaut  = ['h1.jpg','h2.jpg','h3.jpg','h4.jpg','h5.jpg','h6.jpg','h7.jpg','h8.jpg','h9.jpg','h10.jpg']


videoPath =[]
videoPath_happy=[]
imagePath= []
imagePath_happy=[]

image = []
video_h = []
image_h = []
config_flag = False

#******************************************Defining all call back functions*****************************************



def get_seconds():
    now = datetime.datetime.now()
    midnight = now.replace(hour=0,minute=0,second=0)
    second = (now - midnight).seconds
    return second
begin_time = get_seconds()

def on_connect(client,userdata,flags,rc): 
    print("Connected - rc:",rc)    
    
def on_subscribe(client, userdata,mid,granted_qos):
    print("Subscribed:", str(mid),str(granted_qos))

def on_unsubscirbe(client,userdata,mid):
    print("Unsubscribed:",str(mid))

def on_disconnect(client,userdata,rc):
    if rc !=0:
        print("Unexpected Disconnection")
print("current time : ",get_seconds())

def compare_asset(_base_url,_base_dir,_imageNames,_videoNames,_imageHnames,_videoHnames):
    startup ='Startup.jpg'
    Format = "%a, %d %b %Y %H:%M:%S %Z"
    
    
    
    if exists('Assets'):
        pass
    else:
        os.mkdir('Assets')
    if exists(_base_dir+startup): # if a file called startup.jpg is in Assets folder
            try:
                file = urllib.request.urlopen(base_url + startup )
                date=file.headers['last-modified']
                datem = datetime.datetime.strptime(date, Format)
                remote_file_size = file.headers['Content-Length']
                remote_file_time = datetime.datetime(datem.year, datem.month, datem.day, datem.hour, datem.minute,datem.second).timestamp()
                local_file_time = os.path.getmtime(_base_dir+startup)
                local_file_size = int(os.path.getsize(_base_dir + startup))
                
                if float(remote_file_time) > float(local_file_time) or float(remote_file_size) != float(local_file_size):
                    print("Not matching")
                    print(float(remote_file_time) > float(local_file_time))
                    print(float(remote_file_size) == float(local_file_size))
                    try:
                        os.remove(_base_dir+startup)
                        url = _base_url + startup
                        print(url)
                        wget.download(url, (_base_dir + startup) )
                        sleep(.1)
                    except:
                        pass
                else:
                    print("matched: ",startup)
            except:        
                try:
                        os.remove(_base_dir+startup)
                        print("not in online folder deleting from local")
                except:
                        pass        
    else:
        try:
            url = _base_url + startup
            print(url)
            print("not in local folder downloading from online")
            wget.download(url, (_base_dir) + startup )
            sleep(.1)
        except:
            print("not in local folder not in online folder")  
    
    for _image in _imageNames:
        if exists(_base_dir+_image):
            try:
                file = urllib.request.urlopen(base_url + _image )
                date=file.headers['last-modified']
                datem = datetime.datetime.strptime(date, Format)
                remote_file_size = file.headers['Content-Length']
                remote_file_time = datetime.datetime(datem.year, datem.month, datem.day, datem.hour, datem.minute,datem.second).timestamp()
                local_file_time = os.path.getmtime(_base_dir+_image)
                local_file_size = int(os.path.getsize(_base_dir + _image))
                
                if float(remote_file_time) > float(local_file_time) or float(remote_file_size) != float(local_file_size):
                    print("Not matching")
                    print(float(remote_file_time) > float(local_file_time))
                    print(float(remote_file_size) == float(local_file_size))
                    try:
                        os.remove(_base_dir+_image)
                        url = _base_url + _image
                        print(url)
                        wget.download(url, (_base_dir) + _image )
                        sleep(.1)
                    except:
                        pass
                else:
                    print("matched: ",_image)
            except:
                try:
                        os.remove(_base_dir+_image)
                        print("not in online folder deleting from local")
                except:
                        pass
                        
                        
        else:
            try:
                url = _base_url + _image
                print(url)
                print("not in local folder downloading from online")
                wget.download(url, (_base_dir) + _image )
                sleep(.1)
            except:
                print("not in local folder not in online folder")

    for _video in _videoNames:
        if exists(_base_dir+_video):
            try:
                file = urllib.request.urlopen(base_url + _video )
                date=file.headers['last-modified']
                datem = datetime.datetime.strptime(date, Format)
                remote_file_size = file.headers['Content-Length']
                remote_file_time = datetime.datetime(datem.year, datem.month, datem.day, datem.hour, datem.minute,datem.second).timestamp()
                local_file_time = os.path.getmtime(_base_dir+_video)
                local_file_size = int(os.path.getsize(_base_dir + _video))
                
                if float(remote_file_time) > float(local_file_time) or float(remote_file_size) != float(local_file_size):
                    print("Not matching")
                    print(float(remote_file_time) > float(local_file_time))
                    print(float(remote_file_size) == float(local_file_size))
                    try:
                        os.remove(_base_dir+_video)
                        url = _base_url + _video
                        print(url)
                        wget.download(url, (_base_dir) + _video )
                        sleep(.1)
                    except:
                        pass
                else:
                    print("matched: ",_video)
            except:
                try:
                        os.remove(_base_dir+_video)
                        print("not in online folder deleting from local")
                except:
                        pass        
        else:
            try:
                url = _base_url + _video
                print(url)
                print("not in local folder downloading from online")
                wget.download(url, (_base_dir) + _video ) 
                sleep(.1)    
            except:
                print("not in local folder not in online folder")   

    for _image in _imageHnames:
        if exists(_base_dir+_image):
            try:
                file = urllib.request.urlopen(base_url + _image )
                date=file.headers['last-modified']
                datem = datetime.datetime.strptime(date, Format)
                remote_file_size = file.headers['Content-Length']
                remote_file_time = datetime.datetime(datem.year, datem.month, datem.day, datem.hour, datem.minute,datem.second).timestamp()
                local_file_time = os.path.getmtime(_base_dir+_image)
                local_file_size = int(os.path.getsize(_base_dir + _image))
                
                if float(remote_file_time) > float(local_file_time) or float(remote_file_size) != float(local_file_size):
                    print("Not matching")
                    try:
                        os.remove(_base_dir+_image)
                        url = _base_url + _image
                        print(url)
                        wget.download(url, (_base_dir) + _image )
                        sleep(.1)
                    except:
                        pass
                else:
                    print("matched: ",_image)

            except:
                try:
                        os.remove(_base_dir+_image)
                        print("not in online folder deleting from local")
                except:
                        pass
                        
                        
        else:
            try:
                url = _base_url + _image
                print(url)
                print("not in local folder downloading from online")
                wget.download(url, (_base_dir) + _image )
                sleep(.1)
            except:
                print("not in local folder not in online folder")
    for _video in _videoHnames:
        if exists(_base_dir+_video):
            try:
                file = urllib.request.urlopen(base_url + _video )
                date=file.headers['last-modified']
                datem = datetime.datetime.strptime(date, Format)
                remote_file_size = file.headers['Content-Length']
                remote_file_time = datetime.datetime(datem.year, datem.month, datem.day, datem.hour, datem.minute,datem.second).timestamp()
                local_file_time = os.path.getmtime(_base_dir+_video)
                local_file_size = int(os.path.getsize(_base_dir + _video))
                
                if float(remote_file_time) > float(local_file_time) or float(remote_file_size) != float(local_file_size):
                    print("Not matching")
                    print(float(remote_file_time) > float(local_file_time))
                    print(float(remote_file_size) == float(local_file_size))
                    try:
                        os.remove(_base_dir+_video)
                        url = _base_url + _video
                        print(url)
                        wget.download(url, (_base_dir) + _video )
                        sleep(.1)
                    except:
                        pass
                else:
                    print("matched: ",_video)
            except:
                try:
                        os.remove(_base_dir+_video)
                        print("not in online folder deleting from local")
                except:
                        pass        
        else:
            try:
                url = _base_url + _video
                print(url)
                print("not in local folder downloading from online")
                wget.download(url, (_base_dir) + _video ) 
                sleep(.1)    
            except:
                print("not in local folder not in online folder")      

def configure(flagP = False):
    global happy_hr_end
    global happy_hr_begin
    global base_url
    global base_dir 
    global image_display_time
    global image_h_display_time 
    global broker
    global config_flag
    if flagP:
        print('***********************************************************************')
        print('configuring')
        print("happy_hr_end",happy_hr_end)
        print("happy_hr_begin",happy_hr_begin)
        print("base_url",base_url)
        print("image_display_time",image_display_time)
        print("image_h_display_time",image_h_display_time)
        print('***********************************************************************')
    
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
    config_flag = False

def on_message(client,userdata,message):
    global happy_hr_end
    global happy_hr_begin
    global base_url
    global image_display_time
    global image_h_display_time 
    global Run
    print(("message recieved"))
    print(str(message.payload.decode("utf-8")))
    if str(message.topic)== url_top:
        base_url = str(message.payload.decode("utf-8"))
    if str(message.topic)== time_top:
        image_display_time = int(str(message.payload.decode("utf-8")))
    if str(message.topic)== HH_time_top:
        image_h_display_time = int(message.payload)
    if str(message.topic)== HH_from__top:
        happy_hr_begin = int(message.payload.decode())
    if str(message.topic)== HH_till__top:
        happy_hr_end = int(message.payload.decode())
    if str(message.topic)== change_top:
        transition = int(message.payload.decode())
    if str(message.topic)== shutdown_top:
        Run = False
                ##############################################################################
    configure() 

def get_configuration():
    global happy_hr_end
    global happy_hr_begin
    global base_url
    global base_dir 
    global image_display_time
    global image_h_display_time 
    global broker

    config.read('.config.ini')
    happy_hr_begin = config.getint('DEFAULT', 'happy_hr_begin',fallback =0 )
    happy_hr_end = config.getint('DEFAULT', 'happy_hr_end',fallback = 3600)
    image_display_time = config.getint('DEFAULT', 'interval_time',fallback =60 )
    image_h_display_time = config.getint('DEFAULT', 'interval_time_happy_hour',fallback =60 )
    base_url = config.get('DEFAULT', 'base_url',fallback ='none')
    base_dir = config.get('DEFAULT', 'base_dir',fallback = 'Assets')
    broker = config.get('DEFAULT', 'broker',fallback = 'test.mosquitto.org' )
    
def get_seek(timeT,_image,_image_display_time,_video,_video_duration): 
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

                return seek_time,_count,video_flag
        if i<len(_image):
             elapsed_time +=_image_display_time

             if elapsed_time >= timeT:
                _count = i
                video_flag = False
                remaining_time = elapsed_time -timeT

                return remaining_time,_count,video_flag

def playvid(path,start_time=0):
    
    _VideoFlag =False
    if int(start_time)>0:
        _VideoFlag=True
    # pygame.init()
    # screen_size = pygame.display.Info()
    # screen_h = screen_size.current_h #hieght of current screen
    # screen_w = screen_size.current_w #width of current screen

    # #comment out the following lines to go full screen
    # # screen_h = 768
    # # screen_w = 1399

    # #comment out the following line and uncomment the next to remove frame 
    # screen = pygame.display.set_mode((screen_w,screen_h),pygame.RESIZABLE)
    # # screen = pygame.display.set_mode((screen_w,screen_h),pygame.NOFRAME)
    # win_id = pygame.display.get_wm_info()['window']
    # pygame.mixer.quit()
    # vlcInstance = vlc.Instance()
    # media = vlcInstance.media_new(path)

    # player = vlcInstance.media_player_new()
    pygame.mouse.set_visible(False)
    media = vlc.Media(path)
    player.set_xwindow(win_id)
    player.set_media(media)
    
    player.play()
    start_time = int(start_time*1000)
    player.set_fullscreen(True)
    if _VideoFlag:
        player.pause()
        player.set_time(start_time)
        player.play()
    while player.get_state() != vlc.State.Ended:
            if Run == False:
                player.stop()
                player.release()  
                break  


def happy_hour():
    t0 = get_seconds()
    hflag = True
    if t0 >= happy_hr_begin and t0 <= happy_hr_end :
        hflag = True
    else :
        hflag = False
    return hflag        

def get_sync(_image_display_time,_video_duration,imagef,videof,flagP=False):
    global current 
    global imagePath
    global happy_hr_begin
    flag = True
    total_video_time=0
    t0 = get_seconds()
    for t in _video_duration:
        total_video_time += float(t)

    
    if happy_hour():
        total_time = total_video_time + (len(imagef)*_image_display_time)
        number_of_loops  = (t0-happy_hr_begin)/total_time   
        current_loop_time = (number_of_loops-math.floor(number_of_loops)) * total_time
        
    else:
        total_time = total_video_time + (len(imagef)*_image_display_time)
        number_of_loops  = t0/total_time   
        current_loop_time = (number_of_loops-math.floor(number_of_loops)) * total_time
  
    rtime,current,flag = get_seek(current_loop_time,imagef,_image_display_time,videof,_video_duration)
    if flagP:
        print('***********************************************************************')
        print("image time length :",(len(imagef)*_image_display_time))
        print("total_video_time: ", total_video_time)
        print('seek params: ',rtime,current,flag)
        print('num of loops: ',number_of_loops)
        print('floor of loops: ',math.floor(number_of_loops))
        print("Total length :",total_time)
        print("current loop time: ", current_loop_time)
        print('***********************************************************************')

    if flag :
        playvid(videof[current],rtime)
        flag = False
    else :

        playvid(imagef[current])  
        sleep(rtime)
        flag =True
        current += 1


if exists('Assets/Startup.jpg'):
    playvid("Assets/Startup.jpg")



get_configuration()
print ('*************************************')

print ('happy_hr_end',happy_hr_end)
print ('happy_hr_begin',happy_hr_begin)
print ('base_url',base_url)
print ('base_dir',base_dir) 
print ('image_display_time',image_display_time)
print ('image_h_display_time',image_h_display_time) 
print ('broker',broker)

sleep(1)
compare_asset(base_url,base_dir,imagenames_defaut,videonames_defaut,imagenames_happy_defaut,videonames_happy_defaut)


client = mqtt.Client("client4155")
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscirbe
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker,port)


for i in range(items):

    if exists(base_dir+videonames_defaut[i]):
        videoPath.append(base_dir+videonames_defaut[i])
        video_duration.append(None)
    if exists(base_dir + videonames_happy_defaut[i]):
        videoPath_happy.append(base_dir + videonames_happy_defaut[i])
        video_h_duration.append(None)
        
    if exists(base_dir + imagenames_defaut[i]):
        imagePath.append(base_dir + imagenames_defaut[i])
        image.append(None)
    if exists(base_dir + imagenames_happy_defaut[i]):
        imagePath_happy.append(base_dir + imagenames_happy_defaut[i])    
        image_h.append(None)      

current=0

for i in range (len(videoPath)): 
    info = MediaInfo.parse(videoPath[i]).video_tracks[0]
    video_duration[i] = info.duration/1000

for i in range (len(videoPath_happy)):
    info = MediaInfo.parse(videoPath_happy[i]).video_tracks[0]
    video_h_duration[i] = info.duration/1000

 
client.loop_start()
client.subscribe('machine/#')


wait_print_flag = True
while get_seconds() < (begin_time + 5):
    if wait_print_flag:
        print("waiting....")
        wait_print_flag = False
    



while Run:

    if happy_hour():
        get_sync(image_h_display_time,video_h_duration,imagePath_happy,videoPath_happy)
    else: 
        get_sync(image_display_time,video_duration,imagePath,videoPath)
            

