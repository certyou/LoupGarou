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

    print(    r"""
          _           _                                     _ 
      ___| |__   __ _| |_    __ _  ___ _ __   ___ _ __ __ _| |
     / __| '_ \ / _` | __|  / _` |/ _ \ '_ \ / _ \ '__/ _` | |
    | (__| | | | (_| | |_  | (_| |  __/ | | |  __/ | | (_| | |
     \___|_| |_|\__,_|\__|  \__, |\___|_| |_|\___|_|  \__,_|_|
                            |___/                             

    """)

    print("""Bienvenue dans le chat du LOUP GAROU
           - Pour quitter le chat, tapez /exit
           - Pour changer de nom, tapez /name nom
          Amusez-vous bien !\n\n""")

    chemin = os.path.join(os.path.dirname(__file__), "chat.txt")
    socket = TCPToHostConnect()

    loup = False

    while True:

        #check if the player is a loup
        if textModifier("role.txt", "r") == "1" and not loup:
            loup = True
            print("--------------------------------------\nVous êtes un loup garou !! \nutilisez la commande /loup pour envoyer un message au autres loups\n--------------------------------------")
        
        #processing input from the other console
        time.sleep(0.5)
        txt = textModifier(chemin, 'r')
        textModifier(chemin, 'w', "") # delete the content of the file

        # if the command is loup and the player is a loup, we add the tag {LOUP} to the message
        if "loup" in txt[txt.find("€"): txt.find("§")+1] and loup :
            txt = "{LOUP " + txt[txt.find("{") +1 :]
        elif "loup" in txt[txt.find("€")+1: txt.find("§")] :
            #if the player is not a loup, we skip the loop to not display the message
            print("<Erreur Role> : vous n'est pas loup !")
            continue
        
        #if the message is not empty, we send it to the host
        if len(txt) != 0 :
            sendToHost(socket, txt)
            

        # processing the received message
        # {name€command€text}
        txt = recvFromHost(socket)
        
        # if the received message is not empty, we display it
        if txt != None :
            name = txt[txt.find("{")+1:txt.find("€")]
            text = txt[txt.find("§")+1:txt.find("}")]
            command = txt[txt.find("€")+1:txt.find("§")]
            
            #if the command is loup and the player is not a loup, we skip the loop to not display the message
            if command == "loup" and not loup :
                    continue
                    #skip the loop to not display the message

            # general display printing
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
    
    a = ""

    while a == "" :
        # beautiful display for the connection status
        print("offline.   ", end="\r")
        sleep(0.5)
        print("offline..   ", end="\r")
        sleep(0.5)
        print("offline...  ", end="\r")
        sleep(0.5)
        # wait for the IP to be written in the file
        a = textModifier("HostIp.txt", "r")
    
    # then, take the IP of the Host to connect the chat
    HostIp = textModifier("HostIp.txt", "r")
    # Delete the content of the file
    textModifier("HostIp.txt", "w", "")
    
    PlayerSocket = socket.socket()
    print("status : connected")
    # connection
    PlayerSocket.connect((HostIp, 1000))
    
    return PlayerSocket
 
if __name__ == '__main__':
    chat()

