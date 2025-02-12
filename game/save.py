import json
from role import *
from player import *
from game import *
from host import Host
import threading


def save(game):
    """ Save the data in the Save.json file as a dictionnary
    Args:
        - :game: Game object, game to save
    Out:
        - /
    """
    dict = {f"{game.saveName}":{"tabPlayerInLife":[], "mayor": None, "nbTurn":game.nbTurn, "lovers":game.lovers}} # creation of a dictionary that will contain every saved game and element to be saved
    if game.mayor != None:
        dict[f"{game.saveName}"]["mayor"] = game.mayor.name
    for elem in game.tabPlayerInLife: # Save of every player attributes because we can't save object in json
        if elem.card.name != "Sorciere":
            role = {"role":elem.card.name, "id":elem.name}
        else:
            role = {"role":elem.card.name, "id":elem.name, "lifePotion":elem.card.lifePotion, "potionPoison":elem.card.potionPoison}
        if elem.isHost:
            player = {"id":str(elem.id) , "name":elem.name , "card":role, "isHost":True}
        else:    
            player = {"id":str(elem.id) , "name":elem.name , "card":role, "isHost":False}
        dict[f"{game.saveName}"]["tabPlayerInLife"].append(player)
    saved=dict[f"{game.saveName}"]

    with open("Save.json", "r") as f: # we check if the file is empty or not to know if we need to add or if it's the first saved to be write
        if len(f.read()) == 0:
            f.close()
            with open("Save.json", "w") as f:
                json.dump(dict, f, indent=4)
        else:
            with open("Save.json", "r+") as f: # we read the file in r+ to be able to add things
                data=json.load(f)
                data[f"{game.saveName}"]=saved
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
    f.close()


def load(saveName):
    """ Load the data with the same name as the argument from the Save.json file
    Args:
        - :saveName: str, name of the save
    Out:
        - :save: list, list of every element we need to recreate a game (list of players, mayor, nbTurn, lovers)
    """
    with open("Save.json", "r") as file: # we open the file to read it's content
        data = json.load(file)
    save=[]
    tabPlayerInLife=[]
    for elem in data[f"{saveName}"]["tabPlayerInLife"]: # we recreate every player from their attributes and add them in tabPlayerInLife
        if elem["card"]["role"] == "Villageoi":
            elem["card"]=Villager(elem["card"]["id"])
        elif elem["card"]["role"] == "Loup garou":
            elem["card"]=Wearwolf(elem["card"]["id"])
        elif elem["card"]["role"] == "Chasseur":
            elem["card"]=Hunter(elem["card"]["id"])
        elif elem["card"]["role"] == "Sorciere":
            elem["card"]=Witch(elem["card"]["id"],elem["card"]["lifePotion"],elem["card"]["potionPoison"])
        elif elem["card"]["role"] == "Cupidon":
            elem["card"]=Cupidon(elem["card"]["id"])
        elif elem["card"]["role"] == "Voyante":
            elem["card"]=Seer(elem["card"]["id"])
        elif elem["card"]["role"] == "Voleur":
            elem["card"]=Thief(elem["card"]["id"])
        player = Player(elem["id"],elem["name"],elem["isHost"])
        player.card=elem["card"]
        tabPlayerInLife.append(player)
    save.append(tabPlayerInLife) # We then recreate every attribute of Game that are important and add them to a list that will be returned
    save.append(data[f"{saveName}"]["mayor"])
    save.append(data[f"{saveName}"]["nbTurn"])
    save.append(data[f"{saveName}"]["lovers"])
    file.close()
    return save

def reloadGame():
    """ This function is called when the player wants to load a save. It will ask the player which save he wants to load and then load it.
    Args:
        /
    Out:
        - list save, list of every element we need to recreate a game (list of players, mayor, nbTurn, lovers, ...)
    """
    with open("Save.json", "r") as file: # we ask wich save the player want to load
        data = json.load(file)
        print("\nQuel sauvegarde voulez vous charger ? : ")
        saveList = [str(i) for i in range (1,len(data.keys())+1) ]
        saves = []
        cpt = 0

        for key in data.keys():
            saves.append(key)
            cpt += 1
            print(f"{cpt} : {key}")

        choice = int(utils.playerChoice("Votre choix : ", saveList))
        save = load(saves[choice-1])
        nbOfPlayers = len(save[0])
        print("\nNombre de joueurs attendu :"+str(nbOfPlayers)+"\n")

        # connection to the host
        gameHost = Host()
        broadcastThread = threading.Thread(target=gameHost.IPBroadcaster, args=(nbOfPlayers-1,), daemon=True)
        broadcastThread.start()
        gameHost.TCPConnect(nbOfPlayers-1)

        listOfPlayersSaved = save[0]
        listOfPlayers = []

        for elem in listOfPlayersSaved: # we add the host as the first player of the list to not have conflict 
            if elem.isHost == True:
                elem.id = None
                elem.card.id = elem
                listOfPlayersSaved.remove(elem)
                listOfPlayers.append(elem)

        name = []
        for elem in listOfPlayersSaved: # we get the name of every players to ask them wich one it was last time
            name.append(elem.name)
        nameExpected = [str(i) for i in range (1,len(name)+1)]
        cpt = 1

        for i in range(len(listOfPlayersSaved)):
            listOfPlayersSaved[i].id=gameHost.IPList[i]
            savedNames = "\nLes différents noms de la dernière partie sont : \n"
            for j in range(len(name)):
                savedNames += f"{j+1} - {name[j]}\n"
            utils.hostSendMessage(listOfPlayersSaved[i].id, savedNames, False)

        for elem in listOfPlayersSaved: # we ask the name of the player to the player so we can associate the good player to the good role with the good id
            namechoice=int(utils.playerChoice("\nQuel est votre nom de la dernière partie ? :\n ", nameExpected , False, elem))
            player=Player(elem.id, name[namechoice-cpt], False)
            player.card=elem.card
            player.card.id = elem
            listOfPlayers.append(player)
            name.remove(name[namechoice-cpt])
            cpt+=1

        return [listOfPlayers,save[1],save[2],save[3],saves[choice-1]]