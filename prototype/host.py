import socket
import time
import select

class Host:
    def __init__(self):
        self.hostIP = socket.gethostbyname(socket.gethostname()) # retrieves the local IP of the host (the executing machine)
        self.hostPort = 50000 # port defined by convention
        self.broadcastIP = '255.255.255.255' # IP where broadcast messages will appear (255*4 means all addresses are contacted)
        self.broadcastPort = 65000 # port defined by convention
        self.IPBroadcasterSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # creates a socket using IPV4 and a datagram (UDP)
        self.IPBroadcasterSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # configures the socket for broadcasting
        self.IPList = list() # creation of the list of IPs and their sockets

    def IPBroadcaster(self, playerNumber) :
        """ Function to broadcast the private IP of the machine so that clients can later connect via TCP (TCPConnect()).
        The function terminates when there are as many TCP connections as expected players.
        This function must be run alongside TCPConnect.

        Arg:
            - PlayerNumber (int): the number of expected players
        """
        counter = 1
        while len(self.IPList) < playerNumber : # loop to broadcast the IP until enough players are connected
            message = "{" + self.hostIP + "," + str(self.hostPort) + "}" # message: machine coordinates
            self.IPBroadcasterSocket.sendto(message.encode(), (self.broadcastIP, self.broadcastPort)) # method to send the message in broadcast to all local IPs on port 65000
            print(f"IPBroadcaster : packet send to --> IP : {self.broadcastIP} | Port : {self.broadcastPort} ({counter})", end='\r') # display the function status
            time.sleep(3) # sending the message every 3 seconds is more than enough
            counter += 1 # increment the counter


    def TCPConnect(self, playerNumber) :
        """ Function to create sockets for TCP connections with players.
        Arg:
            - PlayerNumber (int): the number of expected players

        Out:
            - IPDict (list): a list of TCP sockets for each player
        """
        hostSocket = socket.socket() # create a socket with default values (TCP) (connection socket)
        hostSocket.bind((self.hostIP, self.hostPort)) # sets the network address for our connection socket
        hostSocket.listen(playerNumber) # defines the socket's backlog size
        # number of connections that can be stored in the socket buffer before being refused
        
        while len(self.IPList) < playerNumber: # TCP connection loop
            print("TCPConnect: waiting for new connection") # Display the function status (waiting for connection)
            newSocket, newAddr = hostSocket.accept() # Blocking method: the program stops waiting for a new connection
            # NewSocket is the socket created for the new connection | NewAddr is the address from which the connection comes
            print("\nConnection accepted <-- IP: " + newAddr[0] + " | Port: " + str(newAddr[1])) # Display information about the new connection
            self.IPList.append(newSocket) # Add the new socket to the list, this is the list of each sockets linked to a player
    
    def SendRequest(self, socket, message):
        """
        Arg :
            - :socket: socket, socket use to send the message
            - :message: str, the message displayed to the remote player
        Out : 
            - :player_response: str, player's response
        """
        socket.sendall(message.encode())
        playerResponse = socket.recv(1024).decode()
        print(playerResponse)
        return playerResponse
    
    def sendToPlayer(self, playerId, message, typeOfReturn) :
        """
        Function to send a message to a player
        The function will send a type of return, it is the type the player will have to send back
        Arg : 
            - :playerId: int, the id of the player to identify which socket to use
            - :message: str, the message to send to the player
            - :typeOfReturn: str, the type of message to send (see protocol)
        """
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
            - :readable: bool, True if there is a message in the buffer ready to be read, False otherwise
        """
        readable, [], [] = select.select([self.IPList[playerId]], [], [], 0)
        return readable != []

