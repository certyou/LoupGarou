import threading
import client
import host
from game import Game
import useful_functions as utils


MAX_PLAYER = 16
MIN_PLAYER = 1


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
        NbOfPlayers = utils.PlayerChoice("Nombre de joueurs attendus : ", [str(x) for x in range(MIN_PLAYER, MAX_PLAYER)]) - 1
        GameHost = host.Host(NbOfPlayers)
        BroadcastThread = threading.Thread(target=GameHost.IPBroadcaster, args=(NbOfPlayers,), daemon=True)
        BroadcastThread.start()
        GameHost.TCPConnect(NbOfPlayers)
        print(GameHost.IPDict)
        new_game = Game(NbOfPlayers)
        new_game.GameStater()
        new_game.GameLoop()
    elif choice == 2:
        You = client.Client()
        You.WithHostConnection()

if __name__ == "__main__":
    main()