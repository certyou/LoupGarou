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
from chat.chatInput import textModifier


MAX_PLAYER = 16
MIN_PLAYER = 1

def host():
    """ launch the host side, and wait for the number of players expected
    Args : 
        /
    Out :
        /
    """
    # Ask the number of players expected
    NbOfPlayers = int(utils.playerChoice("Nombre de joueurs attendus : ", [str(x) for x in range(MIN_PLAYER, MAX_PLAYER)])) - 1

    textModifier("playerNumber.txt", 'w', str(NbOfPlayers)) # Save the number of player in a file to use it in the chat

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
        # Updtate of the listOfPlayers and tabPlayerInLife
        listOfPlayers = reload[0]
        for elem in listOfPlayers:
            elem.setRole(elem.card)
        new_Game = Game(listOfPlayers)
        new_Game.tabPlayerInLife = listOfPlayers
        
        # associate mayor to the right player
        for elem in listOfPlayers:
            if elem.name == reload[1]:
                new_Game.mayor = elem

        # Update the listOfRole
        listOfRole = [elem.card for elem in listOfPlayers]
        new_Game.listOfRole = listOfRole

        # Launch the chat
        launcher.launchHostChat()

        # Update the number of turn, and the lovers
        new_Game.nbTurn = reload[2]-1
        new_Game.lovers = reload[3]

        # Launch the game loop
        for i in range(0, len(new_Game.listOfPlayers)):
                message=f"\n\n {new_Game.listOfPlayers[i].card.ascii} \n\n Vous êtes {new_Game.listOfPlayers[i].card.name}\n"
                utils.HostSendMessage(new_Game.listOfPlayers[i].id, message, False)
        new_Game.GameLoop()
            
        

def client():
    """
    Args :
        /
    Out :
        /
    launch the client side, and wait for message from the host
    """
    You = Client()
    host_socket = You.WithHostConnection()
    utils.ClientSendMessage(host_socket) # response for pseudo
    launcher.launchClientChat()
    while True: # loop to wait for message from the host
        utils.ClientSendMessage(host_socket)

def main():
    """ launch the main menu, and ask the player if he wants to be the host or the client
    Args :
        /
    Out :
        /
    """
    print("\n\n"+INTRO+"\n\n")
    print("Voulez-vous être l'hôte ou le client ?")
    print("1. Hôte")
    print("2. Client")

    choice = int(utils.playerChoice("Votre choix : ", ["1", "2"]))
    print()
    if choice == 1: # if the player is the host
        host()
    elif choice == 2: # if the player is the client
        client()

if __name__ == "__main__":
    main()