import socket
from chat.chatInput import textModifier


class Client:
    def __init__(self):
        pass

    def withHostConnection(self) :
        """ Connect to the host and return the socket
        Args :
            /
        Out :
            - :ToHostConnect: socket, socket connected to the host
        """
        broadcastRecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcastRecv.bind(('', 65000))
        buffer = broadcastRecv.recvfrom(1024)[0].decode()
        hostIp = buffer[1:buffer.find(',')]
        hostPort = int(buffer[buffer.find(',')+1:-1])

        # Save the Host IP in a file for the chat
        textModifier("HostIp.txt", "w", str(hostIp))

        toHostConnect = socket.socket()
        toHostConnect.connect((hostIp, hostPort))
        print(f"Connected to Host <--> {toHostConnect.getpeername()}")
        return toHostConnect
    
    def withIpConnection(self) :
        """ ask for the IP address, connect with the host and then return the socket
        Args :
            /
        Out :
            - :ToHostConnect: socket, socket connected to the host
        """
        ip = input("Enter the Host IP: ")
        port = 50000 # port défini par convention
        toHostConnect = socket.socket()
        toHostConnect.connect((ip, port))
        print(f"Conneced to Host <--> {toHostConnect.getpeername()}")
        return toHostConnect