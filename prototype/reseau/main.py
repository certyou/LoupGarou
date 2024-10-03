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
    elif choice == "2":
        You = client.Client()

if __name__ == "__main__":
    main()