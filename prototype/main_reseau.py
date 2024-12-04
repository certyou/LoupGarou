import threading
from client import Client
from host import Host
from game import Game
from player import Player
import useful_functions as utils
from ascii_art import *
import save as s
import os
import chat.launcher as launcher


#test
MAX_PLAYER = 16
MIN_PLAYER = 1

def host():
    NbOfPlayers = int(utils.playerChoice("Nombre de joueurs attendus : ", [str(x) for x in range(MIN_PLAYER, MAX_PLAYER)])) - 1

    file = open(os.path.join(os.path.dirname(__file__), "chat\\playerNumber.txt"), 'w', encoding='utf-8')
    file.write
    with open(os.path.join(os.path.dirname(__file__), "chat\\playerNumber.txt"), 'a', encoding='utf-8') as file:
            file.write(str(NbOfPlayers))

    choice=2
    with open("Save.json", "r") as file: # check if a save exist
        if len(file.read()) != 0:
            choice=int(utils.playerChoice("\nVoulez-vous chargez une sauvegarde ?\n-1 : Oui \n-2 : Non\nVotre choix : ",["1","2"]))
    if choice == 2:
        GameHost = Host()
        BroadcastThread = threading.Thread(target=GameHost.IPBroadcaster, args=(NbOfPlayers,), daemon=True)
        BroadcastThread.start()
        GameHost.TCPConnect(NbOfPlayers)
        ListOfPlayers = [Player(None, input("votre nom : "), True)]
        for i in range(NbOfPlayers):
            ListOfPlayers.append(Player(GameHost.IPList[i], utils.HostSendMessage(GameHost.IPList[i], "votre nom : "), False))

        new_game = Game(ListOfPlayers)
        new_game.GameInit()
        launcher.launchHostChat()
        new_game.GameLoop()
    else: # If the user wants to load a save we upload all the data from the save to recrate a game object from them
        reload = s.reloadGame()
        listOfPlayers = reload[0]
        new_Game = Game(listOfPlayers)
        new_Game.tabPlayerInLife = listOfPlayers
        listOfRole = []
        for elem in listOfPlayers:
            if elem.name == reload[1]:

                new_Game.mayor = elem

        listOfRole = [elem.card for elem in listOfPlayers]
        new_Game.listOfRole = listOfRole
        launcher.launchHostChat()
        print(new_Game.listOfRole)
        new_Game.nbTurn = reload[2]-1
        new_Game.lovers = reload[3]
        new_Game.GameLoop()
            
        

def client():
    You = Client()
    host_socket = You.WithHostConnection()
    utils.ClientSendMessage(host_socket) # ask for pseudo
    while True:
        utils.ClientSendMessage(host_socket)

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
        launcher.launchClientChat()
        client()

if __name__ == "__main__":
    main()