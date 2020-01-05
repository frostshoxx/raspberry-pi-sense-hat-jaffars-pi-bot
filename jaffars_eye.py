import tweepy
import json
import os
import random
import time
import threading
from datetime import datetime
from picamera import PiCamera

print('Set up tweepy')
with open('twitter_auth.json') as file:
    secrets = json.load(file)

print('Authenticate the access token')
auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
auth.set_access_token(secrets['access_token'], secrets['access_token_secret'])
twitter = tweepy.API(auth)
workDir = "/home/pi/Documents/Projects/TweeterBot"
path = workDir + "/jaffareye.JPG"    
camera = PiCamera()

def take_picture():   
    camera.capture(path)
    
def send_reply():    
    status_greet_words = ['Hello','Hi','Hey', 'Heya', 'Greetings']
    status_readers = ['friends','pals','earthlings','dawgs','homies', 'folks']    
    status_greeting = random.choice(status_greet_words) + ', ' + random.choice(status_readers) + '! '
    print('Setting up date time')
    status_date_time = 'It is ' + datetime.today().strftime('%a %b %d %Y %I:%M %p') + '. '
    status_eye = '\nHere is what I can see right now.'
    status_footer = '\nSeeing through #jaffareye, powered by #jaffarspibot'
    message = status_greeting + status_date_time + status_eye + status_footer
    print(message)
    twitter.update_with_media(path, message)      

# Start the program loop
while 1:
    try:
        take_picture()
        send_reply()
    except:
        print("There was some issue with Jaffar's Eye")
    time.sleep(1800)


