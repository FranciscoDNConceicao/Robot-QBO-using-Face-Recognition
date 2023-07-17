import os
import cv2

def AdicionarImagesTrain(name):
    cap = cv2.VideoCapture(0)
    i = 1
    os.mkdir('Images/' + name)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

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
            if(i % 10 == 0):
                cv2.imwrite('Images/' + name + '/' + str(int(i/10)) + '.jpg', faces) 
                print('Images/' + name + '/' + str(int(i/10)) + '.jpg')            
            i += 1    
            
        cv2.imshow('Face Detection', frame)


    cap.release()
    cv2.destroyAllWindows()


name = str(input("Nome: "))
AdicionarImagesTrain(name)

