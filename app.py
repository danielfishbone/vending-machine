import configparser
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


config = configparser.ConfigParser()
black = (0,0,0)

#*********************************************MQTT SETTINGS********************************
url_top = "machine/url"
time_top = "machine/interval1"
HH_time_top = "machine/interval2"
HH_from__top = "machine/HH_from"
HH_till__top = "machine/HH_till"
change_top = "machine/CO"
broker = "test.mosquitto.org"
port = 1883

#*********************************************************************************************
media_player = vlc.MediaPlayer()
#************************************Pygame Settings ******************************************
video_duration = []
video_h_duration=[]

items = 10

flag = True


videonames_defaut  = ['1.mp4','2.mp4','3.mp4','4.mp4','5.mp4','6.mp4','7.mp4','8.mp4','9.mp4','10.mp4']
videonames_happy_defaut = ['h1.mp4','h2.mp4','h3.mp4','h4.mp4','h5.mp4','h6.mp4','h7.mp4','h8.mp4','h9.mp4','h10.mp4']
imagenames_defaut  = ['1.jpg','2.jpg','3.jpg','4.jpg','5.jpg','6.jpg','7.jpg','8.jpg','9.jpg','10.jpg']
imagenames_happy_defaut  = ['h1.jpg','h2.jpg','h3.jpg','h4.jpg','h5.jpg','h6.jpg','h7.jpg','h8.jpg','h9.jpg','h10.jpg']


videoPath =[]
videoPath_happy=[]
imagePath= []
imagePath_happy=[]

# video = []
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

def compare_asset(_base_url,base_dir,_imageNames,_videoNames,_imageHnames,_videoHnames):
    if exists('Assets'):
        pass
    else:
        os.mkdir('Assets')
    startup ='Startup.jpg'
    if exists(base_dir+startup):
            try:
                file = urllib.request.urlopen(base_url + startup )
                local_file = os.path.getsize(base_dir + startup)
                if local_file != file.length():
                    try:
                        os.remove(base_dir+startup)
                        url = _base_url + startup
                        print(url)
                        wget.download(url, (base_dir) + startup )
                        sleep(.1)
                    except:
                        pass
            except:        
                pass        
    else:
        try:
            url = _base_url + startup
            print(url)
            wget.download(url, (base_dir) + startup )
            sleep(.1)
        except:
                pass  
    if exists(base_dir+startup):  
        # Startup = pygame.image.load('Assets/Startup.jpg')
        # Startup = pygame.transform.scale(Startup, (screensize))
        # screen.blit(Startup,(0,0))  
        # pygame.display.update()   
        playvid('Assets/Startup.jpg',False)            
    for _image in _imageNames:
        if exists(base_dir+_image):
            try:
                file = urllib.request.urlopen(base_url + _image )
                local_file = os.path.getsize(base_dir + _image)
                if local_file != file.length():
                    try:
                        os.remove(base_dir+_image)
                        url = _base_url + _image
                        print(url)
                        wget.download(url, (base_dir) + _image )
                        sleep(.1)
                    except:
                        pass
            except:        
                pass        
        else:
            try:
                url = _base_url + _image
                print(url)
                wget.download(url, (base_dir) + _image )
                sleep(.1)
            except:
                    pass

    for _video in _videoNames:
        if exists(base_dir+_video):
            try:
                file = urllib.request.urlopen(base_url + _video )
                local_file = os.path.getsize(base_dir + _video)
            
                if local_file != file.length():
                    try:
                        os.remove(base_dir+_video)
                        url = _base_url + _video
                        print(url)
                        wget.download(url, (base_dir) + _video )
                        sleep(.1)
                    except:
                        pass
            except:
                pass        
        else:
            try:
                url = _base_url + _video
                print(url)
                wget.download(url, (base_dir) + _video ) 
                sleep(.1)    
            except:
                pass   

    for _image in _imageHnames:
        if exists(base_dir+_image):
            try:
                file = urllib.request.urlopen(base_url + _image )
                local_file = os.path.getsize(base_dir + _image)
            
                if local_file != file.length():
                    try:
                        os.remove(base_dir+_image)
                        url = _base_url + _image
                        print(url)
                        wget.download(url, (base_dir) + _image )
                        sleep(.1)
                    except:
                        pass
            except:
                pass       
        else:
            try:
                url = _base_url + _image
                print(url)
                wget.download(url, (base_dir) + _image )
                sleep(.1)
            except:
                pass
    for _video in _videoHnames:
        if exists(base_dir+_video):
            try:
                file = urllib.request.urlopen(base_url + _video )
                local_file = os.path.getsize(base_dir + _video)
                if local_file != file.length():
                    try:
                        os.remove(base_dir+_video)
                        url = _base_url + _video
                        print(url)
                        wget.download(url, (base_dir) + _video )
                        sleep(.1)
                    except:
                        pass
            except:
                pass        
        else:
            try:

                url = _base_url + _video
                print(url)
                wget.download(url, (base_dir) + _video )   
                sleep(.1)  
            except:
                pass       

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
    happy_hr_begin = config.getint('DEFAULT', 'happy_hr_begin',fallback =50000 )
    happy_hr_end = config.getint('DEFAULT', 'happy_hr_end',fallback = 50000)
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


##########################################





def playvid(path,_VideoFlag =True,start_time=0.1 ):
    start_time = start_time*1000
    media = vlc.Media(path)
    media_player.set_media(media)
    media_player.set_fullscreen(True)
    media_player.play()
   

    sleep(.1)
    if _VideoFlag:
        media_player.set_time(int(start_time))

        while media_player.get_state() != vlc.State.Ended:
            
            media_player.set_fullscreen(True)

# def playvid(path,surf = screen, seek_time =0):
    
#     if exists(path):
#         info = MediaInfo.parse(path).video_tracks[0]
#         _video = MediaPlayer(path)
        
#         active = True 
#         duration = info.duration
#         frames = 0
#         frame_delay = 1 / float(info.frame_rate)
#         image = pygame.Surface((0, 0))
#         _video.set_size(900, 650)
#         sleep(0.2)
#         vid_time = _video.get_pts()
#         if (vid_time + seek_time) < duration and active:
#             _video.seek(seek_time)
#             if seek_time < 0:
#                 while (vid_time + seek_time < frames * frame_delay):
#                     frames -= 1
#         while _video.get_pts() > frames * frame_delay:
#             frame, val = _video.get_frame()
#             frames += 1
#         while active:
#             frame, val = _video.get_frame()
#             if val == "eof":
#                 active = False
#                 _video.close_player()
#             elif frame != None:
#                 image = pygame.image.frombuffer(frame[0].to_bytearray()[0], frame[0].get_size(), "RGB")       
#                 surf.blit(image, (0,0))       
#                 pygame.display.update()
#                 sleep(val)
#                 # pygame.time.wait(int(val))
                
#     else:
#         pass
##################################################################
def happy_hour():
    t0 = get_seconds()
    hflag = True
    if t0 >= happy_hr_begin and t0 <= happy_hr_end :
        hflag = True
    else :
        hflag = False
    return hflag        

def get_sync(image_display_time,_video_duration,imagef,videof,flagP=False):
    global current 
    global flag
    global imagePath
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
    if flagP:
        print('***********************************************************************')
        print("image time length :",(len(imagef)*image_display_time))
        print("total_video_time: ", total_video_time)
        print('seek params: ',rtime,current,flag)
        print('num of loops: ',number_of_loops)
        print('floor of loops: ',math.floor(number_of_loops))
        print("Total length :",total_time)
        print("current loop time: ", current_loop_time)
        print('***********************************************************************')

    if flag :
        playvid(videoPath[current],True,rtime)
        flag = False
    else :
        playvid(imagePath[current],False)
        # pic = pygame.image.load(imagePath[current]).convert()
        # pic = pygame.transform.scale(pic, (screensize))
        # screen.blit(pic,(0,0))  
        # pygame.display.update()     
        sleep(rtime)
        flag =True
        current += 1

# pygame.mouse.set_visible(False)
if exists('Assets/Startup.jpg'):
    playvid("Assets/Startup.jpg",False)
    # Startup = pygame.image.load('Assets/Startup.jpg')
    # Startup = pygame.transform.scale(Startup, (screensize))
    # screen.blit(Startup,(0,0))  

    # pygame.display.update()   


get_configuration()
sleep(1)
compare_asset(base_url,base_dir,imagenames_defaut,videonames_defaut,imagenames_happy_defaut,videonames_happy_defaut)


client = mqtt.Client("pythonq")
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
# for i in range (len(image)):
#     image[i] = pygame.image.load(imagePath[i])
#     image[i] = pygame.transform.scale(image[i], (screensize))

for i in range (len(videoPath_happy)):
    info = MediaInfo.parse(videoPath_happy[i]).video_tracks[0]
    video_h_duration[i] = info.duration/1000
# for i in range (len(image_h)):
#     image_h[i] = pygame.image.load(imagePath_happy[i])
#     image_h[i] = pygame.transform.scale(image_h[i], (screensize))
 
client.loop_start()
client.subscribe(url_top)
client.subscribe(time_top)
client.subscribe(HH_time_top)
client.subscribe(HH_from__top)
client.subscribe(HH_till__top)
client.subscribe(change_top)
wait_print_flag = True
while get_seconds() < (begin_time + 30):
    if wait_print_flag:
        print("waiting....")
        wait_print_flag = False
    pass
# if happy_hour():
#     get_sync(image_h_display_time,video_h_duration,imagePath_happy,videoPath_happy)
# else: 
#     get_sync(image_display_time,video_duration,imagePath,videoPath)

Run =True

while Run:
    if config_flag:
        configure()
    if happy_hour():
        get_sync(image_h_display_time,video_h_duration,imagePath_happy,videoPath_happy)
    else: 
        get_sync(image_display_time,video_duration,imagePath,videoPath)
            

