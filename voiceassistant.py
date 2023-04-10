import os 
import time
import speech_recognition as sr
import playsound
from gtts import gTTS
from weather import getDate, userDate 
from homeworkbot import getAssignments
import datetime
import threading



def speak(text):
    try:
        tts = gTTS(text= text, lang = "en", tld= "ie", slow= False) #create an object of gTTs which is a module that converts text into speech
        filename = "voice.mp3" 
        tts.save(filename) #create a file named "voice.mp3"
        playsound.playsound(filename) #play the file
    except AssertionError: #this will ignore the errors when there is no text because there are new lines in the txt files, so we can skip those
        pass


def getaudio():
    r = sr.Recognizer() #sr is a nickname and abbreviation for the speech recognition library, .Recognizer calls the class
    with sr.Microphone(chunk_size = 512) as source: 
        audio = r.listen(source) #check for audio
        said = ""
        try:
            said = r.recognize_google(audio) #get the dialogue through the speech recognizer using Google's API
            print(said)
        except Exception as e:
            print("Exception as ", str(e)) 
    return said

def speakAssignment():
    with open("missingAssignments.txt", "r", buffering= 20000000) as f: #open the list of missing assignments in small chunks
        for line in f:    #speak one line at a time
            speak(line)

WAKE = "hey andrew" 
print("Start")

while True:
    text = getaudio().lower()
    if text.count(WAKE) > 0:
        speak("What can I do for you?")
        text = getaudio().lower()
        
        #list of possible commands for the voice assistant
        POEM_STR = ["poem", "let me hear a poem", "do you have a poem"] 
        WEATHER_STR = ["weather", "what is the weather"]
        HOMEWORK_STR = ["homework"]

        #checks to see if any of these commands are used
        word_in_text = [word for word in text.split() if word in POEM_STR or word in WEATHER_STR or word in HOMEWORK_STR]
        
        
        if not len(word_in_text) > 0:  #if there aren't any commands used... 
            speak("I don't understand you.")
        
        for phrase in POEM_STR:
            if phrase in text:
                speak("what poem would you like to hear?")
                text = getaudio().lower()
              
                GENRE_STR = {"father": "/Users/andrew/Desktop/LearningC++/LearningPython/VoiceAssistantPython/fatherpoem.txt", 
                             "mother": "/Users/andrew/Desktop/LearningC++/LearningPython/VoiceAssistantPython/motherpoem.txt",
                              "brother":"/Users/andrew/Desktop/LearningC++/LearningPython/VoiceAssistantPython/brotherpoem.txt"}
                
                #checks to see if user specifies a poem that exists
                for genre in GENRE_STR: 
                    if genre in text: #if the poem does exist...
                        speak("Okay")
                        #read the file in small chunks which allows the program not have to load the entire poem at once
                        with open(GENRE_STR[genre],"r",buffering= 20000000) as f:  
                            for line in f:
                                speak(line)                       
                                            
                if not text in GENRE_STR:    
                    speak("I don't understand you.")
        
        
        for phrase in WEATHER_STR:
            if phrase in text:  #check to see if the weather command is used
                date = userDate(text) #get the date that the user is refering to
                speak(getDate(date))  #get the weather on that date
            
        for phrase in HOMEWORK_STR:
            if phrase in text:  #check if homework command is used
                getAssignmentThread = threading.Thread(target= getAssignments) # start a thread to get a list of missing assignments
                getAssignmentThread.start()
                
                speakAssignmentThread = threading.Thread(target= speakAssignment) #start a thread that speaks the assignment by small chunks until the entire missing list is loaded
                speakAssignmentThread.start()

                speakAssignmentThread.join()
                speak("That is all.")
                
         
       
