import vlc
from time import sleep

path1 = "Assets/1.mp4"
path2 = "Assets/4.mp4"


media_player = vlc.MediaPlayer()


def playvid(path,_VideoFlag =True,start_time=0.1 ):
    start_time = start_time*1000
    media = vlc.Media(path)
    media_player.set_media(media)
    media_player.set_fullscreen(True)
    media_player.play()
   

    sleep(.1)
    if _VideoFlag:
        media_player.set_time(start_time)

        while media_player.get_state() != vlc.State.Ended:
            
            media_player.set_fullscreen(True)
            
            
            
        



while True:
    playvid("Assets/1.jpg",False)
    sleep(3)
    playvid(path2,True,15.4)
