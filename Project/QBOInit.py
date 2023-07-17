from QboSay import TextToSpeech
from QboListen import SpeechToText
from QBOMain import Init
import os

os.system('sudo pkill chromium')
os.system('mpg123 -g 10 -a convertQBO AudioStartup.mp3')

print("hi")
TextToSpeech("Olá eu sou a EVA. Estou pronta para ajudar. Quando o meu nariz estiver azul pode falar")

while True:
    text = SpeechToText()

    if text == "Eva":
        TextToSpeech("Sim, no que posso ajudar?")
        Init()
    elif text == "desligar":
        TextToSpeech("A desligar...")
        os.system('mpg123 -a convertQBO AudioEnd.mp3')
        break;
    else:
        TextToSpeech("Não conheço nenhuma ordem chamada " + str(text))