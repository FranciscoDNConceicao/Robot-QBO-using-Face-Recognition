from QboSay import TextToSpeech
from QboListen import SpeechToText
from datetime import datetime
from WhoAmI import WhoAmIRecognition
from QBOTakePhoto import AdicionarImagesTrain
from Trainer import TrainingModel
from FollowFace import PiFace

def TimeClock():
    DateNow = datetime.now()
    formattedDateNow = DateNow.strftime("São %H horas e %M minutos")
    TextToSpeech(formattedDateNow)

def MacaquinhoImit():
    while True:
        text = SpeechToText()
        if text == "Podes parar":
            break
        TextToSpeech(text)

def WhoAmI():
    TextToSpeech("Ok, a identificar face")
    name = WhoAmIRecognition() 
    TextToSpeech("Olá " + name)

def DontUnderstand():
    TextToSpeech("Não entendi o que disse, por favor repita novamente")

def Exit():
    TextToSpeech("Adeus, até uma próxima")

def AddPersonModel():
    TextToSpeech("Entendido, a adicionar pessoa ao meu modelo")
    AdicionarImagesTrain()

def TrainModel():
    TextToSpeech("Entendido, a treinar modelo")
    TrainingModel()

def FollowFace():
    PiFace()
    
TasksDict = {
        "imita-me": MacaquinhoImit,
        "Que horas são": TimeClock,
        "horas": TimeClock,
        "quem sou eu": WhoAmI,
        "quem eu sou": WhoAmI,
        "adeus": Exit,
        "adicionar pessoa": AddPersonModel,
        "treinar modelo":  TrainModel,
        "segue-me": FollowFace,
        }
def Init():
    while True:
        task = SpeechToText()
        action = TasksDict.get(task, DontUnderstand)
        action()
        print(action)
        if(task== "adeus"):
            break
    