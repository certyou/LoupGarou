import threading
import client
import host
import useful_functions as utils


MAX_PLAYER = 16
MIN_PLAYER = 4


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
    if choice == "1":
        NbOfPlayers = utils.PlayerChoice("Nombre de joueurs attendus : ", [str(x) for x in range(MIN_PLAYER, MAX_PLAYER)])
        GameHost = host.Host(NbOfPlayers)
        BroadcastThread = threading.Thread(target=GameHost.IPBroadcaster, args=(1,), daemon=True).start() # replace 1 by NbOfPlayers
        GameHost.TCPConnect(1) # replace 1 by NbOfPlayers
        print(GameHost.IPDict)
    elif choice == "2":
        You = client.Client()
        You.WithHostConnection()

if __name__ == "__main__":
    main()