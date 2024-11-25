from chatInput import textModifier
import time 
import socket
import select
import os

from time import sleep

def chat():
    """Main program for receiving text input and displaying those coming from the server

    input --> chat --> server (broadcast) --> chat --> display
    
    """

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
            name = txt[txt.find("{")+1:txt.find("€")]
            text = txt[txt.find("§")+1:txt.find("}")]
            print(f"{name} : {text}")
        
        

def sendToHost(socket, message) : 
    """Function that send a message to the host
    Arg:
        - :socket: socket, socket of the host
        - :message: str, message to send
    """
    socket.sendall(message.encode())

def recvFromHost(socket) :
    """Function that receive a message from the host
    Arg:
        - :socket: socket, socket of the host
    Out:
        - :message: str, message received
    """
    readable, _, _ = select.select([socket], [], [], 0.01)
    if socket in readable :
        message = socket.recv(1024).decode()
        return message
    return None

def TCPToHostConnect() :
    """Function to connect to the host
    Out:
        - :PlayerSocket: socket, socket of the player
    """
    textModifier("HostIp.txt", "w", "")
    a = ""
    while a == "" :
        print("offline.", end="\r")
        sleep(0.5)
        print("offline..", end="\r")
        sleep(0.5)
        print("offline...", end="\r")
        sleep(0.5)
        a = textModifier("HostIp.txt", "r")
    HostIp = textModifier("HostIp.txt", "r")
    PlayerSocket = socket.socket()
    print("status : connected")
    PlayerSocket.connect((HostIp, 1000))
    
    return PlayerSocket
 
if __name__ == '__main__':
    chat()

