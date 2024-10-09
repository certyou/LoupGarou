
import threading
import socket
import time

class Host:
    def __init__(self, PlayerNumber):
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

        Takes the following parameter:
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
        Takes the following parameter:
            - PlayerNumber (int): the number of expected players

        Returns:
            - IPDict (list): a list of TCP sockets for each player
        """
        HostSocket = socket.socket() # create a socket with default values (TCP) (connection socket)
        HostSocket.bind((self.HostIP, self.HostPort)) # sets the network address for our connection socket
        HostSocket.listen(PlayerNumber) # defines the socket's backlog size
        # number of connections that can be stored in the socket buffer before being refused
        

        while len(self.IPList) < PlayerNumber : # boucle de connexion TCP      
            print("TCPConnect : waiting for new connection") # Affichage de l'état de la fonction (en attente de connexion)
            NewSocket, NewAddr = HostSocket.accept() # Méthode bloquante : le programme se stop en attente d'une nouvelle connexion
            # NewSocket est le socket créé pour la nouvelle connexion | NewAddr est l'adresse d'où viens la connexion
            print("\nConnection accepted <-- IP : " + NewAddr[0] + " | Port : " + str(NewAddr[1])) # affichage des information de la nouvelle connexion
            self.IPList.append(NewSocket) # ajout du nouveau socket dans la liste
    
    def SendMessage(socket, message):
        """
        Arg :
            - :socket: socket, socket use to send the message
            - :message: str, the message displayed to the remote player
            - :expected_results: list, the list of expected results
        Out : 
            - :choice: int, player's choice
        """
        socket.sendall(message.encode())
        player_response = socket.recv(1024).decode()
        print(player_response)
        return player_response