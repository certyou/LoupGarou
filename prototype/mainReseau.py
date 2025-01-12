import threading
from client import Client
from host import Host
from game import Game
from player import Player
import usefulFunctions as utils
from asciiArt import *
import save as s
import launcher as launcher
from chat.chatInput import textModifier


MAX_PLAYER = 8
MIN_PLAYER = 2

def host():
    """ launch the host side, and wait for the number of players expected
    Args : 
        /
    Out :
        /
    """
    # Ask the number of players expected
    nbOfPlayers = int(utils.playerChoice("Nombre de joueurs attendus : ", [str(x) for x in range(MIN_PLAYER, MAX_PLAYER)])) - 1

    textModifier("playerNumber.txt", 'w', str(nbOfPlayers)) # Save the number of player in a file to use it in the chat

    choice = 2
    with open("Save.json", "r") as file: # check if a save exist
        if len(file.read()) != 0:
            choice = int(utils.playerChoice("\nVoulez-vous chargez une sauvegarde ?\n-1 : Oui \n-2 : Non\nVotre choix : ",["1","2"]))
    if choice == 2:
        saveName = input("\nQuel nom voulez vous donner a votre partie ? : \n")
        gameHost = Host()
        broadcastThread = threading.Thread(target=gameHost.IPBroadcaster, args=(nbOfPlayers,), daemon=True)
        broadcastThread.start()
        gameHost.TCPConnect(nbOfPlayers)
        listOfPlayers = [Player(None, input("votre nom : "), True)]
        for i in range(nbOfPlayers):
            listOfPlayers.append(Player(gameHost.IPList[i], utils.hostSendMessage(gameHost.IPList[i], "votre nom : "), False))

        newGame = Game(listOfPlayers)
        newGame.saveName = saveName
        newGame.gameInit()
        launcher.launchHostChat()
        newGame.gameLoop()
    else: # If the user wants to load a save we upload all the data from the save to recrate a game object from them
        reload = s.reloadGame()
        # Updtate of the listOfPlayers and tabPlayerInLife
        listOfPlayers = reload[0]
        for elem in listOfPlayers:
            elem.setRole(elem.card)
        newGame = Game(listOfPlayers)
        newGame.tabPlayerInLife = listOfPlayers
        
        # associate mayor to the right player
        for elem in listOfPlayers:
            if elem.name == reload[1]:
                newGame.mayor = elem

        # Update the listOfRole
        listOfRole = [elem.card for elem in listOfPlayers]
        newGame.listOfRole = listOfRole

        # Update the name of the game
        newGame.saveName=reload[-1]
        
        # Launch the chat
        launcher.launchHostChat()

        # Update the number of turn, and the lovers
        newGame.nbTurn = reload[2]-1
        newGame.lovers = reload[3]

        # Launch the game loop
        for i in range(0, len(newGame.listOfPlayers)):
                message=f"\n\n {newGame.listOfPlayers[i].card.ascii} \n\n Vous êtes {newGame.listOfPlayers[i].card.name}\n"
                utils.hostSendMessage(newGame.listOfPlayers[i].id, message, False)
        newGame.gameLoop()
            
        

def client():
    """ launch the client side, and wait for message from the host
    Args :
        /
    Out :
        /
    """
    You = Client()
    hostSocket = You.withHostConnection()
    utils.clientSendMessage(hostSocket) # response for pseudo
    launcher.launchClientChat()
    while True: # loop to wait for message from the host
        utils.clientSendMessage(hostSocket)

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