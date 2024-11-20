from chatInput import textModifier
from time import sleep
import threading
import hostChatServer
import os

import time

def chat():
    chemin = os.path.join(os.path.dirname(__file__), "chat.txt")

    while True:
        """
        sleep(0.5)
        command = textModifier(chemin, 'r')
        if command == "/host" :
            hostProcess = threading.Thread(target = hostChatServer.TCPConnect_Chat, daemon=True )
        if command == "/exit" :
            return
        if len(command) != 0 :
            print(command[command.find("§") + 1: -1])
            textModifier(chemin, 'w', "") #supprimer les données
        """
 
if __name__ == '__main__':
    chat()

