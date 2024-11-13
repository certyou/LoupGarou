import threading
from client import Client
from host import Host
from game import Game
from player import Player
import useful_functions as utils
from ascii_art import *

#test
MAX_PLAYER = 16
MIN_PLAYER = 1

def host():
    NbOfPlayers = int(utils.playerChoice("Nombre de joueurs attendus : ", [str(x) for x in range(MIN_PLAYER, MAX_PLAYER)])) - 1
    GameHost = Host()
    BroadcastThread = threading.Thread(target=GameHost.IPBroadcaster, args=(NbOfPlayers,), daemon=True)
    BroadcastThread.start()
    GameHost.TCPConnect(NbOfPlayers)
    ListOfPlayers = [Player(None, input("votre nom : "), True)]
    for i in range(NbOfPlayers):
        ListOfPlayers.append(Player(GameHost.IPList[i], utils.SendRequest(GameHost.IPList[i], "votre nom : "), False))

    new_game = Game(ListOfPlayers)
    new_game.GameInit()
    new_game.GameLoop()

def client():
    You = Client()
    host_socket = You.WithHostConnection()
    while True:
        utils.SendResponse(host_socket)

def main():
    print("\n\n"+INTRO+"\n\n")


    print("Voulez-vous être l'hôte ou le client ?")
    print("1. Hôte")
    print("2. Client")

    choice = int(utils.playerChoice("Votre choix : ", ["1", "2"]))
    print()
    if choice == 1:
        host()
    elif choice == 2:
        client()

if __name__ == "__main__":
    main()