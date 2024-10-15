import threading
from client import Client
from host import Host
from game import Game
from player import Player
import useful_functions as utils

#test
MAX_PLAYER = 16
MIN_PLAYER = 1

def host():
    NbOfPlayers = utils.PlayerChoice("Nombre de joueurs attendus : ", [str(x) for x in range(MIN_PLAYER, MAX_PLAYER)]) - 1
    GameHost = Host()
    BroadcastThread = threading.Thread(target=GameHost.IPBroadcaster, args=(NbOfPlayers,), daemon=True)
    BroadcastThread.start()
    GameHost.TCPConnect(NbOfPlayers)
    ListOfPlayers = [Player(None, input("votre nom : "))]
    for i in range(NbOfPlayers):
        #print(GameHost.SendRequest(GameHost.IPList[i], "votre nom : "))
        ListOfPlayers.append(Player(GameHost.IPList[i], GameHost.SendRequest(GameHost.IPList[i], "votre nom : ")))

    new_game = Game(ListOfPlayers)
    new_game.GameStarter()
    new_game.GameLoop()

def client():
    You = Client()
    socket = You.WithHostConnection()
    You.SendResponse(socket)

def main():
    print(
"""
joli texte d'introduction avec plein d'ascii art
"""
    )

    print("Voulez-vous être l'hôte ou le client ?")
    print("1. Hôte")
    print("2. Client")

    choice = utils.PlayerChoice("Votre choix : ", ["1", "2"])
    print()
    if choice == 1:
        host()
    elif choice == 2:
        client()

if __name__ == "__main__":
    main()