import socket

def WithHostConnection() :
    BroadcastRecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    BroadcastRecv.bind(('', 65000))
    Buffer = BroadcastRecv.recvfrom(1024)[0].decode()
    HostIp = Buffer[1:Buffer.find(',')]
    HostPort = int(Buffer[Buffer.find(',')+1:-1])

    ToHostConnect = socket.socket()
    ToHostConnect.connect((HostIp, HostPort))
    return ToHostConnect
    

socket = WithHostConnection()
print(f"Conneced to Host <--> {socket.getpeername()}")


#bonjour