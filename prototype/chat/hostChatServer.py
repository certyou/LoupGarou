from chatInput import textModifier
import time
import socket
import select

def hostChatServer() :
    """Main program for the chat server
    this program is the same as chat.py but for the host
    it is also used as the server of the whole chat system"""

    print(    """
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
          Amusez-vous bien !""")

    nbplayer = int(textModifier("playerNumber.txt", "r"))
    playerSock = TCPConnect_Chat(nbplayer)

    while True : 
        time.sleep(0.5)
        messages = receve(playerSock)
        messageHost = textModifier("hostChat.txt", "r")
        if messageHost != "" :
            messages.append(textModifier("hostChat.txt", 'r'))
        textModifier("hostChat.txt", "w", "")


        for i in messages : 
            if i != None or i != "":
                PlayersNames = list()

                # Le chat des joueurs regarde deja si le joueur est nomé.
                # je possède les sockets des joueurs, je peux faire un systeme de dictionnaire pour le /talk (note à moi meme)

                publish(playerSock, i)
                
                name = i[i.find("{")+1:i.find("€")]
                text = i[i.find("§")+1:i.find("}")]
                print(f"{name} : {text}")

        

    

    
def TCPConnect_Chat(nbPlayers) :
    """Function to create a TCP connection with all players
    Arg:
        - :nbPlayers: int, number of players expected
    Out:
        - :sockets: list, list of sockets of every player
    """
    port = 1000
    sockets = list()
    listener = socket.socket()
    HostIp = socket.gethostbyname(socket.gethostname())
    
    listener.bind((HostIp, port))
    listener.listen(nbPlayers)

    while len(sockets) != nbPlayers :
        newSock, _  = listener.accept()
        sockets.append(newSock)  
        
    return sockets

def publish(sockets, message):
    """Function that send a message to every players
    Arg:
        - :sockets: list, list of sockets of every player
        - :message: str, the message to send
    Out:
        /
    """ 

    for i in sockets :
        i.sendall(message.encode())

def receve(sockets) :
    """Function that receive messages from every player
    Arg:
        - :sockets: list, list of sockets of every player
    Out:
        - :list, list of messages received
    """
    messages = list()
    for i in sockets :
        #recv is a blocking function, so we use select to avoid blocking
        readable, _, _ = select.select([i], [], [], 0.1)

        if i in readable :
            messages.append(i.recv(1024).decode())
    return messages
    
if __name__ == "__main__" :
    hostChatServer()