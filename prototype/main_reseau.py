import threading
import client
import host
from game import Game
from player import Player
import useful_functions as utils


MAX_PLAYER = 16
MIN_PLAYER = 1

def host():
    NbOfPlayers = utils.PlayerChoice("Nombre de joueurs attendus : ", [str(x) for x in range(MIN_PLAYER, MAX_PLAYER)]) - 1
    ListOfPlayers = []
    GameHost = host.Host(NbOfPlayers)
    BroadcastThread = threading.Thread(target=GameHost.IPBroadcaster, args=(NbOfPlayers,), daemon=True)
    BroadcastThread.start()
    GameHost.TCPConnect(NbOfPlayers)
    for  i in range(NbOfPlayers):
        ListOfPlayers.append(Player(GameHost.IPList[i], utils.SendMessage(GameHost.IPList[i], "votre nom : ")))
    

    new_game = Game(ListOfPlayers)
    new_game.GameStater()
    new_game.GameLoop()

def client():
    You = client.Client()
    You.WithHostConnection()

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