from chatInput import textModifier
import time 
import socket
import threading
import hostChatServer
import os

from time import sleep

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
    textModifier("HostIp.txt", "w", "")
    while textModifier("HostIp.txt", "r") == "" :
        print("status : offline", end="\r")
        sleep(1)
    HostIp = textModifier("HostIp.txt", "r")
    PlayerSocket = socket.socket()
    print("status : connected")
    PlayerSocket.connect((HostIp, 1000))
    
    return PlayerSocket
 
if __name__ == '__main__':
    chat()

