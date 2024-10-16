
import threading
import socket
import time
import select

class Host:
    def __init__(self):
        self.HostIP = socket.gethostbyname(socket.gethostname()) # retrieves the local IP of the host (the executing machine)
        self.HostPort = 50000 # port defined by convention
        self.BroadcastIP = '255.255.255.255' # IP where broadcast messages will appear (255*4 means all addresses are contacted)
        self.BroadcastPort = 65000 # port defined by convention
        self.IPBroadcasterSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # creates a socket using IPV4 and a datagram (UDP)
        self.IPBroadcasterSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # configures the socket for broadcasting
        self.IPList = list() # creation of the list of IPs and their sockets

    def IPBroadcaster(self, PlayerNumber) :
        """ Function to broadcast the private IP of the machine so that clients can later connect via TCP (TCPConnect()).
        The function terminates when there are as many TCP connections as expected players.
        This function must be run alongside TCPConnect.

        Arg:
            - PlayerNumber (int): the number of expected players
        """
        counter = 1
        while len(self.IPList) < PlayerNumber : # loop to broadcast the IP until enough players are connected
            message = "{" + self.HostIP + "," + str(self.HostPort) + "}" # message: machine coordinates
            self.IPBroadcasterSocket.sendto(message.encode(), (self.BroadcastIP, self.BroadcastPort)) # method to send the message in broadcast to all local IPs on port 65000
            print(f"IPBroadcaster : packet send to --> IP : {self.BroadcastIP} | Port : {self.BroadcastPort} ({counter})", end='\r') # display the function status
            time.sleep(3) # sending the message every 3 seconds is more than enough
            counter += 1 # increment the counter


    def TCPConnect(self, PlayerNumber) :
        """ Function to create sockets for TCP connections with players.
        Arg:
            - PlayerNumber (int): the number of expected players

        Out:
            - IPDict (list): a list of TCP sockets for each player
        """
        HostSocket = socket.socket() # create a socket with default values (TCP) (connection socket)
        HostSocket.bind((self.HostIP, self.HostPort)) # sets the network address for our connection socket
        HostSocket.listen(PlayerNumber) # defines the socket's backlog size
        # number of connections that can be stored in the socket buffer before being refused
        
        while len(self.IPList) < PlayerNumber: # TCP connection loop
            print("TCPConnect: waiting for new connection") # Display the function status (waiting for connection)
            NewSocket, NewAddr = HostSocket.accept() # Blocking method: the program stops waiting for a new connection
            # NewSocket is the socket created for the new connection | NewAddr is the address from which the connection comes
            print("\nConnection accepted <-- IP: " + NewAddr[0] + " | Port: " + str(NewAddr[1])) # Display information about the new connection
            self.IPList.append(NewSocket) # Add the new socket to the list, this is the list of each sockets linked to a player
    
    def SendRequest(self, socket, message):
        """
        Arg :
            - :socket: socket, socket use to send the message
            - :message: str, the message displayed to the remote player
        Out : 
            - :player_response: str, player's response
        """
        socket.sendall(message.encode())
        player_response = socket.recv(1024).decode()
        print(player_response)
        return player_response
    
    def sendToPlayer(self,playerId, message, typeOfReturn) :
        frame = str()
        frame = "{" + typeOfReturn + "$" + message + "}"
        if self.IPList[playerId] != None :
            self.IPList[playerId].sendall(frame.encode())

    def listening(self, playerId) :
        """
        Function to listen the buffer of the socket with select
        This function should be started in a thread
        Arg : 
            - :playerId: int, the id of the player to identify which socket to listen
        Out : 
            - :bool: bool, True if there is a message in the buffer ready to be read, False otherwise
        """
        readable, [], [] = select.select([self.IPList[playerId]], [], [], 0)
        return readable != []

