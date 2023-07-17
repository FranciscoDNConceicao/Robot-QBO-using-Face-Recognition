import pyttsx3
import subprocess
import pygame
import os
import time
from gtts import gTTS

def TextToSpeech(text):
    if (text == ""):
        text = "No message"
    tts = gTTS(text=text, lang='pt')
    tts.save('output.mp3')
    os.system('mpg123 -a convertQBO output.mp3')
