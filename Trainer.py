import cv2
import numpy as np
from PIL import Image
import os
from QboSay import TextToSpeech
def getImagesAndLabels(detector):
    faceSamples=[]
    ids = []
    id = 0
    for nome in os.listdir('./Images/'):
        for i in range(1, 100):
            print('./Images/' + nome + '/' + str(i) + '.jpg')
            PIL_img = Image.open('./Images/' + nome + '/' + str(i) + '.jpg').convert('L') # convert it to grayscale
            img_numpy = np.array(PIL_img,'uint8')

            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])   
                ids.append(id)
        TextToSpeech("Registei " + str(id + 1) + " pessoas")
        print("Registei " + str(id + 1) + " pessoas")
        print(len(ids))
        print(len(faceSamples))
        id += 1
    print(ids)
    return faceSamples,ids

def TrainingModel():
    path = 'Images'
    TextToSpeech("Estou a treinar para reconhecer mais pessoas!")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml');

    print ("\nTraining faces. It will take few seconds. Wait ...")
    faces, ids = getImagesAndLabels(detector)
    recognizer.train(faces, np.array(ids))
    recognizer.write('trainer.yml')
    TextToSpeech("Finalizei o treinamento")
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))

