import configparser
config = configparser.ConfigParser()
config['DEFAULT'] = {
                      'happy_hr_begin': '47000',
                      'happy_hr_end': '50000',
                      'interval_time': '60',
                      'interval_time_happy_hour': '60',
                      'base_url': 'https//:',
                      'base_dir': 'Assets/',
                      'broker': 'test.mosquitto.org'
                      
                      }

with open('.config.ini', 'w') as configfile:
  config.write(configfile)

  # happy_hr_end=48500
# happy_hr_begin=47179
# base_url = 'https//:'
# base_dir = 'Assets/'
# broker = 'test.mosquitto.org'
                      
# image_display_time = 60
# image_h_display_time = 60
