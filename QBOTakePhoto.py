import os
import cv2
from QboSay import TextToSpeech
from QboListen import SpeechToText
def AdicionarImagesTrain():
    
    TextToSpeech("Qual é o nome do utilizador?")
    while True:
        name = SpeechToText()
        TextToSpeech("O nome do utilizador é " + str(name) + " ?")
        ConfName = SpeechToText()
        if ConfName == "sim":
            break
        elif ConfName == "Não":
            TextToSpeech("Por favor, informe o seu nome")
        else:
            TextToSpeech("Não entendi a confirmação, por favor informe o seu nome")
    
    cap = cv2.VideoCapture(0)
    i = 1
    os.mkdir('Images/' + name)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    TextToSpeech("A iniciar o processo, por favor mantenha-se posicionado e olhe para mim")
    while True:
        if(i == 200):
            break
        print(i)
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            faces = frame[y:y + h, x:x + w]
            if(i % 2 == 0):
                cv2.imwrite('Images/' + name + '/' + str(int(i/2)) + '.jpg', faces) 
                print('Images/' + name + '/' + str(int(i/2)) + '.jpg')            
            i += 1    
            
        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    
    TextToSpeech("Processo Finalizado")
    cap.release()
    cv2.destroyAllWindows()


