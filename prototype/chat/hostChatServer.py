from chatInput import textModifier
import time
import socket
import select

def hostChatServer() :
    """Main function simulating a chat server"""

    nbplayer = int(textModifier("playerNumber.txt", "r"))
    playerSock = TCPConnect_Chat(nbplayer)

    while True : 
        time.sleep(0.5)
        messages = receve(playerSock)
        messages.append(textModifier("HostChat.txt", 'r'))
        textModifier("hostChat.txt", "w", "")

        for i in messages : 
            if i != None :
                PlayersNames = list()

                Name = i[1:i.find("€")]
                command = i[i.find("€") +1 : i.find("§" )]
                text = i[i.find("§") +1 : -1]

                # Le chat des joueurs regarde deja si le joueur est nomé.
                #je possède les sockets des joueurs, je peux faire un systeme de dictionnaire pour le /talk (note à moi meme)

                publish(playerSock, text)

    

    
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
    HostIp = textModifier("HostIp.txt", 'r')
    
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
    return

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
        else :
            messages.append("")
    return messages
    
if __name__ == "__main__" :
    hostChatServer()