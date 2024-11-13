from chatInput import textModifier
import time
import socket

def hostChatServer() :
    nbplayer = input("combien de")
    playerSock = TCPConnect_Chat(nbplayer)
    return

    

def TCPConnect_Chat(nbPlayers) :
    port = "1000"
    sockets = list()
    listener = socket.socket()
    HostIp = textModifier("HostIp.txt", 'r')
    
    listener.bind((HostIp, port))
    listener.listen(nbPlayers)

    while len(sockets) != nbPlayers :
        newSock, addr  = listener.accept()
        sockets.append(newSock)
        

    return sockets

def publish(socket, message):
    return

if __name__ == '__main__' :
    hostChatServer()