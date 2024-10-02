import threading
import socket
import time


HostIP = socket.gethostbyname(socket.gethostname()) # permet d'avoir l'ip locale de l'hôte (la machine executante)
HostPort = 50000 # port définit par convention
BroadcastIP = '255.255.255.255' # ip sur lequel les messages broadcast vont apparaitre (255*4 signifie que toutes les adresses sont contactés)
BroadcastPort = 65000 # port définit par convention

IPBroadcasterSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # créer un socket utilisant IPV4 et un datagrame (UDP)
IPBroadcasterSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # paramètre le socket pour une utilisation en broadcast

IPDict = list() #cration de la liste des IP et de leurs sockets

def IPBroadcaster(PlayerNumber) :
    """ Fonction de diffusion de l'ip privé de la machine pour que les clients puissent ensuite se connecter en TCP (TCPConnect())
    la fonction se termine quand la fonction il y a autant de connexion TCP que de joueurs attendus
    Cette fonction doit être lancée avec TCPConnect

    Prend en paramètre : 
        - PlayerNumber (int) : le nombre de joueurs attendus
    """
    compteur = 1
    while len(IPDict) < PlayerNumber : # boucle de diffusion de l'IP jusqu'à ce qu'il y ai assez de joueurs connectés
        message = "{" + HostIP + "," + str(HostPort) + "}" # message : coordonnées de la machine
        IPBroadcasterSocket.sendto(message.encode(), (BroadcastIP, BroadcastPort)) # méthode d'envoi du message en broadcast à tous les ip locaux sur le port 65000
        print(f"IPBroadcaster : packet send to --> IP : {BroadcastIP} | Port : {BroadcastPort} ({compteur})", end='\r') # affichage de l'état de la fonction
        time.sleep(3) # envoi du message toutes les 3 secondes est largement suffisant
        compteur += 1 # incrémentation du compteur


def TCPConnect(PlayerNumber) :
    """ Fonction de création de sockets pour une connexion tcp avec les joueurs
    Prend en paramètre : 
        - PlayerNumber (int) : le nombre de joueurs attendus

    Renvoie :
        - IPDict (list) : une liste des socket TCP de chaque joueurs 
    """
    HostSocket = socket.socket() # créer un socket avec les valeurs de base (TCP) (Socket de connexion)
    HostSocket.bind((HostIP, HostPort)) # définit l'adresse réseau de notre socket de connexion
    HostSocket.listen(PlayerNumber) # définition de la taille du backlog du socket
    # nombre de connexion qui peuvent être stocké dans le tampon du socket avant qu'elle soit refusée
    

    while len(IPDict) < PlayerNumber : # boucle de connexion TCP      
        print("TCPConnect : waiting for new connection") # Affichage de l'état de la fonction (en attente de connexion)
        NewSocket, NewAddr = HostSocket.accept() # Méthode bloquante : le programme se stop en attente d'une nouvelle connexion
        # NewSocket est le socket créé pour la nouvelle connexion | NewAddr est l'adresse d'où viens la connexion
        print("\nConnection accepted <-- IP : " + NewAddr[0] + " | Port : " + str(NewAddr[1])) # affichage des information de la nouvelle connexion
        IPDict.append(NewSocket) # ajout du nouveau socket dans la liste
                 

thread1 = threading.Thread(target=IPBroadcaster, args=(1,), daemon=True)
thread1.start()

TCPConnect(1)
print(IPDict)