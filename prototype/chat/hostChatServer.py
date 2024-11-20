from chatInput import textModifier
import time
import socket

def hostChatServer() :
    """Main function simulating a chat server"""

    nbplayer = input("combien de")
    playerSock = TCPConnect_Chat(nbplayer)

    while True : 
        time.sleep(0.5)
        messages = receve(playerSock)
        messages.append(textModifier("HostChat.txt", 'r'))
        textModifier("HostChat.txt", "w", "")

        for i in messages : ###############################
            if True :
                return

    return

    
def TCPConnect_Chat(nbPlayers) :
    """Function to create a TCP connection with all players
    Arg:
        - :nbPlayers: int, number of players expected
    Out:
        - :sockets: list, list of sockets of every player
    """
    port = "1000"
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
        messages.append(i.recv(1024).decode())
    return messages
    