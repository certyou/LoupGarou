from chatInput import textModifier
import time 
import socket
import threading
import hostChatServer
import os

import time

def chat():
    chemin = os.path.join(os.path.dirname(__file__), "chat.txt")
    socket = TCPToHostConnect()

    while True:
        
        time.sleep(0.5)
        command = textModifier(chemin, 'r')
        if command == "/host" :
            hostProcess = threading.Thread(target = hostChatServer.TCPConnect_Chat, daemon=True )
        if command == "/exit" :
            return
        if len(command) != 0 :
            sendToHost(socket, command)
            textModifier(chemin, 'w', "") #supprimer les données

        ####################################################################################################################################
        

def sendToHost(socket, message) : 
    socket.sendall(message.encode())

def TCPToHostConnect() :
    HostIp = textModifier("HostIp.txt", "r")
    PlayerSocket = socket.socket()
    PlayerSocket.connect((HostIp, 1000))
    return PlayerSocket
 
if __name__ == '__main__':
    chat()

