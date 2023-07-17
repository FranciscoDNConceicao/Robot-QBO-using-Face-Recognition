import speech_recognition as sr
import sys
import serial
sys.path.insert(0, '/opt/qbo/')
from controller.QboController3 import Controller

def SpeechToText():
    port = '/dev/serial0'
    ser = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, rtscts=False, dsrdtr=False, timeout=0)
    
    recognizer = sr.Recognizer()
    controller = Controller(ser)
    for i, mic_name in enumerate(sr.Microphone.list_microphone_names()):
            if mic_name == "dmicQBO_sv":
                mic = sr.Microphone(i)
                
    with mic as source:
        
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        controller.SetNoseColor(1) 
        audio = recognizer.listen(source)
        
    try:
        text = recognizer.recognize_google(audio, language="pt-PT")
        print("You said:", text)
        controller.SetNoseColor(0) 
        return text
    except sr.UnknownValueError:
        controller.SetNoseColor(0) 
        print("Unable to recognize speech")
    except sr.RequestError as e:
        controller.SetNoseColor(0) 
        print("Error occurred; {0}".format)
