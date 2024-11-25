from chatInput import textModifier
import time 
import socket
import select
# import threading
# import hostChatServer
import os

from time import sleep

def chat():

    chemin = os.path.join(os.path.dirname(__file__), "chat.txt")
    socket = TCPToHostConnect()

    while True:
        
        #traitement de l'input 
        time.sleep(0.5)
        txt = textModifier(chemin, 'r')
        textModifier(chemin, 'w', "") #supprimer les données

        if txt == "/exit" :
            return
        if len(txt) != 0 :
            sendToHost(socket, txt)
            

        #traitement du massage reçu
        # {name€command€text}
        txt = recvFromHost(socket)
        if txt != None :
            print(txt)
        
        

def sendToHost(socket, message) : 
    socket.sendall(message.encode())

def recvFromHost(socket) :
    readable, _, _ = select.select([socket], [], [], 0.01)
    if socket in readable :
        message = socket.recv(1024).decode()
        return message
    return None

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

