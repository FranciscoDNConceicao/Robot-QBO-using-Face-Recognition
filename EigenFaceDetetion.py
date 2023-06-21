import os
import cv2
import time
import numpy as np


ListaNomes = []
ListaImages = []
ListId = []
IdNames = 0

for nome in os.listdir('./Images/'):
    # Verifica se o item é uma pasta
    if os.path.isdir(os.path.join('./Images/', nome)):
        for i in range(1, 20):
            ListaImages.append(cv2.resize(cv2.imread('./Images/' + nome + '/' + str(i) + '.jpg', cv2.IMREAD_GRAYSCALE), (100, 100)))
            ListId.append(IdNames)
        ListaNomes.append(nome)
        IdNames += 1

num_components = 80  
height, width = ListaImages[0].shape

imagesFlat = np.array([image.flatten() for image in ListaImages], dtype='float32')
#mean, eigenvectors = cv2.PCACompute(imagesFlat, mean=None, maxComponents=num_components)

recognizer = cv2.face.EigenFaceRecognizer_create(num_components)
print(ListId)

ListId = np.array(ListId)
recognizer.train(imagesFlat, ListId)

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        faces = gray[y:y + h, x:x + w]
        image = cv2.resize(faces, (width, height))
        Imageflat = image.flatten().astype('float32')
        #projection = cv2.pcaPOroject(Imageflat.reshape(1, -1), mean, eigenvectors)
        id, confidence = recognizer.predict(image)
        name = ListaNomes[id]
        print("Recognized Face: {}, Confidence: {:.2f}".format(name, confidence))
        break
        
    cv2.imshow('Face Detection', frame)       
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

    

