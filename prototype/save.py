import json
from role import *
from player import *
from game import *

def save(game,saveName):
    """Action : Save the date in the Save.json file as a dictionnary named saveName
       Input : instance of class Game, game
               str, saveName (the name of the save)
       Output : None"""
    dict = {f"{saveName}":{"tabPlayerInLife":[], "mayor": None, "nbTurn":game.nbTurn, "lovers":game.lovers}} # creation of a dictionary that will contain every saved game and element to be saved
    if game.mayor != None:
        dict[f"{saveName}"]["mayor"] = game.mayor.name
    for elem in game.tabPlayerInLife: # Save of every player attributes because we can't save object in json
        if elem.card.name != "Sorciere":
            role = {"role":elem.card.name, "id":elem.name}
        else:
            role = {"role":elem.card.name, "id":elem.name, "lifePotion":elem.card.lifePotion, "potionPoison":elem.card.potionPoison}
        if elem.IsHost:
            player = {"id":str(elem.id) , "name":elem.name , "card":role, "IsHost":True}
        else:    
            player = {"id":str(elem.id) , "name":elem.name , "card":role, "IsHost":False}
        dict[f"{saveName}"]["tabPlayerInLife"].append(player)


    saved=dict[f"{saveName}"]

    with open("Save.json", "r") as f: # we check if the file is empty or not to know if we need to add or if it's the first saved to be write
        if len(f.read()) == 0:
            f.close()
            with open("Save.json", "r+") as f:
                json.dump(dict, f, indent=4)
        else:
            with open("Save.json", "r+") as f:
                data=json.load(f)
                data[f"{saveName}"]=saved
                f.seek(0)
                json.dump(data, f, indent=4)

    f.close()


def load(saveName): # L'id des rôle doit être le joueur
    """Action : Load the data named saveName from the Save.json file
       Input : str, saveName (the name of the save)
       Output : tab with every element we need to reload a game, save
    """
    with open("Save.json", "r") as file:
        data = json.load(file)
    save=[]
    tabPlayerInLife=[]
    for elem in data[f"{saveName}"]["tabPlayerInLife"]:
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
        player = Player(elem["id"],elem["name"],elem["IsHost"])
        player.card=elem["card"]
        tabPlayerInLife.append(player)
    save.append(tabPlayerInLife)
    save.append(data[f"{saveName}"]["mayor"])
    save.append(data[f"{saveName}"]["nbTurn"])
    save.append(data[f"{saveName}"]["lovers"])
    file.close()
    return save

#print(load("s1"))