from chatInput import textModifier
import time
import socket
import select


def hostChatServer() :


    """Main program for the chat server
    this program is the same as chat.py but for the host
    it is also used as the server of the whole chat system"""

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
          Amusez-vous bien !""")

    nbplayer = int(textModifier("playerNumber.txt", "r"))
    print("Start connection to players")
    playerSock = TCPConnect_Chat(nbplayer)

    loup = False
    fille = False

    while True : 
        
        if textModifier("role.txt", "r") == "1" and not loup:
            loup = True
            print("--------------------------------------\nVous êtes un loup garou !! \nutilisez la commande /loup pour envoyer un message au autres loups\n--------------------------------------")
            textModifier("role.txt", "w", "")
        if textModifier("role.txt", "r") == "2" and not fille:
            fille = True
            print("--------------------------------------\nVous êtes la fille !! \nVous entenderez les messages de loups !\n--------------------------------------")
            textModifier("role.txt", "w", "")
        

        time.sleep(0.5)
        # reveive messages from players
        messages = receve(playerSock)

        # check if the host has sent a message
        messageHost = textModifier("hostChat.txt", "r")

        # if the host has sent a message, we check if it is a loup message
        if messageHost != "" :
            if "loup" == messageHost[messageHost.find("€")+1: messageHost.find("§")] and loup :
                messageHost = "{LOUP " + messageHost[messageHost.find("{") +1 :]
                messages.append(messageHost)

            # if the host is not a loup, we skip the loop to not display the message
            elif "loup" in messageHost[messageHost.find("€")+1: messageHost.find("§")] :
                print("<Erreur Role> : vous n'est pas loup !")
                
            # if the message is not empty, we send it to the players
            if "loup" not in messageHost[messageHost.find("€")+1: messageHost.find("§")] :
                messages.append(textModifier("hostChat.txt", 'r'))
            
        # we delete the content of the file      
        textModifier("hostChat.txt", "w", "")


        # we travel through the message list and display the messages
        for i in messages : 
            if i != None or i != "":

                publish(playerSock, i)
                
                name = i[i.find("{")+1:i.find("€")]
                text = i[i.find("§")+1:i.find("}")]
                command = i[i.find("€")+1:i.find("§")]
                
                if command == "loup" and not loup :
                    if fille :
                        print(f"{name[:5]} : {text}")
                    continue
                print(f"{name} : {text}")

        

    

    
def TCPConnect_Chat(nbPlayers) :
    """Function to create a TCP connection with all players
    Arg:
        - :nbPlayers: int, number of players expected
    Out:
        - :sockets: list, list of sockets of every player
    """
    port = 40000
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