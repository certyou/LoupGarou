import socket
import select


class Client:
    def __init__(self):
        pass

    def WithHostConnection(self) :
        BroadcastRecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        BroadcastRecv.bind(('', 65000))
        Buffer = BroadcastRecv.recvfrom(1024)[0].decode()
        HostIp = Buffer[1:Buffer.find(',')]
        HostPort = int(Buffer[Buffer.find(',')+1:-1])

        ToHostConnect = socket.socket()
        ToHostConnect.connect((HostIp, HostPort))
        print(f"Conneced to Host <--> {ToHostConnect.getpeername()}")
        return ToHostConnect
    
    def WithIpConnection(self) :
        Ip = input("Enter the Host IP: ")
        Port = 50000 # port défini par convention
        ToHostConnect = socket.socket()
        ToHostConnect.connect((Ip, Port))
        print(f"Conneced to Host <--> {ToHostConnect.getpeername()}")
        return ToHostConnect
    
    def SendResponse(self, socket, message=""):
        """
        Arg :
            - :socket: socket, socket use to send the message
            - :message: str, the message displayed to the host player
        Out : 
            /
        """
        host_request = socket.recv(1024).decode()
        print(host_request)
        socket.sendall(input("votre rep :").encode())