import cv2
import numpy as np
import os
from statistics import mode
from QboSay import TextToSpeech
from QboListen import SpeechToText
from QBOTakePhoto import AdicionarImagesTrain
from Trainer import TrainingModel
import sys
#sys.path.insert(0, '/opt/qbo/')

#from controller.QboController3 import Controller
import serial

def WhoAmIRecognition():
    
    #port = '/dev/serial0'
    #ser = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, rtscts=False, dsrdtr=False, timeout=0)
    #controller = Controller(ser)
    
    faceDetet = True
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer.yml')
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml');
    id = 0
    
    ListaNomes = []
    print("A treinar")
    for nome in os.listdir('./Images/'):
        # Verifica se o item é uma pasta
        if os.path.isdir(os.path.join('./Images/', nome)):
            ListaNomes.append(nome)
    
    
    cam = cv2.VideoCapture(0)
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    
    NumAmostras = 1;
    NamesAmostList= [];
    TextToSpeech("A procurar por pessoa")
    while True:
        #controller.SetNoseColor(0)
        ret, img = cam.read()
        
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )
        for(x,y,w,h) in faces:
            
            if faceDetet == True:
                TextToSpeech("Face detetada! Por favor não se mexa")
                faceDetet = False 
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            # Check if confidence is less them 100 ==> "0" is perfect match
            if (confidence < 100):
                #controller.SetNoseColor(2)
                id = ListaNomes[id]
                NamesAmostList.append(id)
                NumAmostras += 1
                print("Recognized Face: {}, Confidence: {:.2f}".format(id, confidence))
            else:
                #controller.SetNoseColor(2)
                id = "desconhecido"
                NamesAmostList.append(id)
                NumAmostras += 1
                print("Recognized Face: {}, Confidence: {:.2f}".format(id, confidence))
        
        cv2.imshow("Camera Feed", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if NumAmostras == 20:
            break;
    
    cam.release()
    cv2.destroyAllWindows()
    
    Name = mode(NamesAmostList)
    
    if(Name == "desconhecido"):
        TextToSpeech("Não conheço esta pessoa. Deseja registá-la?")
        resposta = SpeechToText()
        if(resposta == "sim"):
            TextToSpeech("Okay, a começar o processo de registo")
            AdicionarImagesTrain()
            TrainingModel()
            TextToSpeech("Acabou de ser registado, Parabens")
        elif(resposta.lower() == "não"):
            TextToSpeech("Entendido")
    return Name