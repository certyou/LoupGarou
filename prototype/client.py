import socket
from chat.chatInput import textModifier


class Client:
    def __init__(self):
        pass

    def WithHostConnection(self) :
        """ Connect to the host and return the socket
        Args :
            /
        Out :
            - :ToHostConnect: socket, socket connected to the host
        """
        BroadcastRecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        BroadcastRecv.bind(('', 65000))
        Buffer = BroadcastRecv.recvfrom(1024)[0].decode()
        HostIp = Buffer[1:Buffer.find(',')]
        HostPort = int(Buffer[Buffer.find(',')+1:-1])

        # Save the Host IP in a file for the chat
        textModifier("HostIp.txt", "w", str(HostIp))

        ToHostConnect = socket.socket()
        ToHostConnect.connect((HostIp, HostPort))
        print(f"Connected to Host <--> {ToHostConnect.getpeername()}")
        return ToHostConnect
    
    def WithIpConnection(self) :
        """ ask for the IP address, connect with the host and then return the socket
        Args :
            /
        Out :
            - :ToHostConnect: socket, socket connected to the host
        """
        Ip = input("Enter the Host IP: ")
        Port = 50000 # port défini par convention
        ToHostConnect = socket.socket()
        ToHostConnect.connect((Ip, Port))
        print(f"Conneced to Host <--> {ToHostConnect.getpeername()}")
        return ToHostConnect