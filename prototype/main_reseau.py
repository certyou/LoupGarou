import threading
from client import Client
from host import Host
from game import Game
from player import Player
import useful_functions as utils
from ascii_art import *
from save import *

#test
MAX_PLAYER = 16
MIN_PLAYER = 1

def host():
    choice=2
    with open("Save.json", "r") as file:
        if len(file.read()) != 0:
            choice=int(utils.playerChoice("\nVoulez-vous chargez une sauvegarde ?\n-1 : Oui \n-2 : Non\n",["1","2"]))
    if choice == 2:
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
    else:
        with open("Save.json", "r") as file:
            data=json.load(file)
        print("Quel sauvegarde voulez vous charger ? : ")
        saveList=[]
        for key in data.keys():
            print(key)
            saveList.append(key)
        choice = utils.playerChoice("Votre choix : ", saveList)
        save=load(choice)
        NbOfPlayers=len(save[0])
        print("\nnombre de joueurs attendu :"+str(NbOfPlayers))
        GameHost = Host()
        BroadcastThread = threading.Thread(target=GameHost.IPBroadcaster, args=(NbOfPlayers-1,), daemon=True)
        BroadcastThread.start()
        GameHost.TCPConnect(NbOfPlayers-1)
        listOfPlayersSaved=save[0]
        listOfPlayers=[]
        for elem in listOfPlayersSaved:
            if elem.IsHost==True:
                elem.id=None
                elem.card.id=elem
                listOfPlayersSaved.remove(elem)
                listOfPlayers.append(elem)
        name=[]
        for elem in listOfPlayersSaved:
            name.append(elem.name)
        for i in range(len(listOfPlayersSaved)):
            listOfPlayersSaved[i].id=GameHost.IPList[i]
            listOfPlayers.append(listOfPlayersSaved[i])
            SendMessage(listOfPlayersSaved[i], "\nLes différents noms de la dernière partie sont : \n")
            for i in range(len(name)):
                SendMessage(listOfPlayersSaved[i], f"- {name[i]}\n")
            namechoice=utils.playerChoice("Quel est votre nom de la dernière partie  ? : ", name , False, listOfPlayersSaved[i])
            for j in range(len(listOfPlayers)):
                if listOfPlayers[j].name==namechoice:
                    listOfPlayers[j].id=GameHost.IPList[i]
                    listOfPlayers[j].card.id=listOfPlayers[j]
                    name.remove(namechoice)

        new_Game=Game(listOfPlayers)
        new_Game.tabPlayerInLife=listOfPlayers
        new_Game.mayor=save[1]
        
        new_Game.nbTurn=save[2]-1
        new_Game.lovers=save[3]
        new_Game.GameLoop()
            
        

def client():
    You = Client()
    host_socket = You.WithHostConnection()
    utils.SendResponse(host_socket) # ask for pseudo
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