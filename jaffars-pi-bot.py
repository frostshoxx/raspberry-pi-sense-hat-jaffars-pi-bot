import tweepy
import json
import os
import random
import time
import threading
from colorzero import Color
from datetime import datetime
from espeak import espeak
from sense_hat import SenseHat

# Set up background thread to flip image
def flip_image_horizontally():
    while 1:
        sense.flip_h()
        time.sleep(random.randint(1,5))
    
# Get device core temperature
def get_device_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return (temp.replace("temp=","").replace('\'C\n',''))

# Convert celsius to fahrenheit
def get_fahrenheit(celsius):
    return round((celsius * 9/5) + 32,2)

# Use text to speech with sense hat LED animation
def speak(text_to_speech):
    sense.load_image("jaffar3.png")
    jaff_open_mouth = True
    espeak.synth(text_to_speech)    
    while espeak.is_playing():
        time.sleep(0.3)
        jaff_open_mouth = not jaff_open_mouth
        sense.load_image("jaffar3.png" if jaff_open_mouth else "jaffar.png")        
    sense.load_image("jaffar.png")

# configuration
enable_cheerlights = True

# print('Initiate Sense Hat')
sense = SenseHat()
sense.low_light = False
sense.load_image("jaffar.png")

# add a backgroudn thread to flip image horizonally
thread1 = threading.Thread(target = flip_image_horizontally)
thread1.start()

# print('Initiate TTS')
#espeak.set_voice("en-us+f5") # female's voice
espeak.set_voice("en-us+m3") # male's voice
speak("Initiate Jaffar's Pi Bot!")

# print('Set up tweepy')
with open('twitter_auth.json') as file:
    secrets = json.load(file)

# print('Authenticate the access token')
auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
auth.set_access_token(secrets['access_token'], secrets['access_token_secret'])
twitter = tweepy.API(auth)

# Start the program loop
command = ''
while command != 'e':
    # print('Setting up greeters')
    status_greet_words = ['Hello','Hi','Hey', 'Heya']
    status_readers = ['friends','pals','earthlings','dawgs','homies']
    status_greeting = random.choice(status_greet_words) + ', ' + random.choice(status_readers) + '! '
    
    # Prompt menu option
    print('\n\n\n\n\n\n\n\n\n\n') # Throw a bunch of new line to move the menu down from previous texts
    print('[c] to set LED color and broadcast #cheerlights on twitter')
    print('[t] text to speech')
    print('[g] gyroscope (press ctrl + c to stop)')
    print('[cp] compass (press ctrl + c to stop)')
    print('[a] accelerometer (press ctrl + c to stop)')
    print('[o] orientation (press ctrl + c to stop)')
    print('[e] to exit')
    print('[other keys] to send a system tweet')
    command = input('Select the command: ')    
    
    # Setting up date time
    status_date_time = 'It is ' + datetime.today().strftime('%a %b %d %Y %I:%M %p') + '. '
    
    # change LED color
    if command == 'c':
        speak("Please enter a color")
        color_input = ''
        while color_input != 'e':
            print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
            color_input = input("Please enter a color or [e] to main menu: ")
            if color_input != 'e':
                try:
                    color = Color(color_input)
                    speak("Here is " + color_input)
                    sense.clear(color.rgb_bytes)
                    if enable_cheerlights == True:                        
                        message = status_greeting + status_date_time + "Please set #cheerlights to " + color_input
                        print(message)
                        twitter.update_status(message)
                    else:
                        print("Cheerlights tweet is disabled")
                except:
                    error_message = color_input + ' is not a valid color. Try again!'
                    print(error_message)
                    speak(error_message)
            else:
                speak("Back to main menu")
    
    # text to speech
    elif command == 't':
        speak("Please enter what you want me to say")
        text_input = ''
        while text_input != 'e':
            print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
            text_input = input("Please enter the texts or [e] to exit: ")
            if text_input != 'e':
                print(text_input)
                speak(text_input)
            else:
                speak("Back to main menu")
    elif command == 'g':
        speak("gyroscope")
        sense.clear()
        continue_gyro = True
        while continue_gyro:
            try:
                sense.set_imu_config(False, True, False)
                gyro_only = sense.get_gyroscope()
                print("p: {pitch}, r: {roll}, y: {yaw}".format(**gyro_only))
                time.sleep(0.05)
            except:
                speak("Back to main menu")
                continue_gyro = False
    elif command == 'cp':
        speak("compass")
        sense.clear()
        continue_compass = True
        while continue_compass:
            try:
                sense.set_imu_config(True, False, False)
                north = sense.get_compass()
                print("North: %s" % north)
                time.sleep(0.05)
            except:
                speak("Back to main menu")
                continue_compass = False
    elif command == 'a':
        speak("accelerometer")
        sense.clear()
        continue_acc = True
        while continue_acc:
            try:
                sense.set_imu_config(False, False, True)
                accel_only = sense.get_accelerometer()
                print("p: {pitch}, r: {roll}, y: {yaw}".format(**accel_only))
                time.sleep(0.05)
            except:
                speak("Back to main menu")
                continue_acc = False
    elif command == 'o':
        speak("orientation")
        sense.clear()
        continue_sensor = True
        while continue_sensor:
            try:
                sense.set_imu_config(True, True, True)
                orientation = sense.get_orientation()
                print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))
                time.sleep(0.05)
            except:
                speak("Back to main menu")
                continue_sensor = False                  
    # Jaffar Pi Bot tweeting sensor data        
    elif command != 'e':
        sense.load_image("jaffar2.png")
        espeak.synth("Constructing tweeter message")                
        while espeak.is_playing():
            time.sleep(1)                   
        
        espeak.synth("Collecting data from the sensors")
        while espeak.is_playing():
            time.sleep(1)
            
        # print('Add dynamic temperature-based comment on Pi temp')
        cTemp = float(get_device_temp())
        fTemp = get_fahrenheit(cTemp)
        status_pi_temp = 'My core temp is ' + str(fTemp) +'\'F. '
    
        if cTemp < 60:
            status_pi_temp = status_pi_temp + 'I feel very comfortable right now. '
        elif cTemp > 60 and cTemp < 75:
            status_pi_temp = status_pi_temp + 'It\'s getting hot in here, but I\'m still doing OK. '
        elif cTemp >= 75:
            status_pi_temp = status_pi_temp + 'It\'s getting too hot in here, so I need to cool down a bit. '

        sense.set_imu_config(True, False, False)
        
        # Pull the data from sense sensors
        status_humidity = sense.humidity
        
        # Call twice to ensure that the pressure is being read correctly
        status_pressure = sense.get_pressure()
        status_pressure = sense.get_pressure()
        
        status_room_temp = get_fahrenheit(sense.get_temperature_from_humidity())                
        status_room = '\n\nRoom Sensors\nHumidity: ' + str(round(status_humidity,2)) + ' %RH\nPressure: ' + str(round(status_pressure,2)) + ' Millibars'
        status_room += '\nTemperature: ' + str(status_room_temp) + '\'F'
        status_footer = '\n\nPowered by #jaffarspibot. '

        espeak.synth("Tweet the message")
        while espeak.is_playing():
            time.sleep(1)

        #message = status_greeting + status_date_time + status_pi_temp + status_room + status_orientation_rad + status_footer
        message = status_greeting + status_date_time + status_pi_temp + status_room + status_footer
        print(message)
        twitter.update_status(message)        
        speak("Tasks completed!")

# Terminate the program loop
speak("Good bye!")
sense.clear()

