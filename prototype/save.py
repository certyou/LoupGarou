import json
from role import *
from player import *
from game import *

def save(tabPlayerInLife,saveName):
    """Action : Save the date in the Save.json file as a dictionnary named saveName
       Input : tab of instances of Player class,tabPlayerInlife (tab of Pllayer alive)
               str, saveName (the name of the save)
       Output : None"""
    dict = {f"{saveName}":{"tabPlayerInLife":[]}}
    
    for elem in tabPlayerInLife:
        if elem.card.name != "Sorciere":
            role = {"role":elem.card.name, "id":elem.card.id}
        else:
            role = {"role":elem.card.name, "id":elem.card.id, "lifePotion":elem.card.lifePotion, "potionPoison":elem.card.potionPoison}
        player = {"id":elem.id , "name":elem.name , "card":role }
        dict[f"{saveName}"]["tabPlayerInLife"].append(player)

    with open("Save.json", "w") as f:
        json.dump(dict, f)


def load(saveName):
    """Action : Load the data named saveName from the Save.json file
       Input : str, saveName (the name of the save)
       Output : tab of instance of Player class, tabPlayerInLife
    """
    with open("Save.json", "r") as f:
        data = json.load(f)
    
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

        tabPlayerInLife.append(Player(elem["id"],elem["name"],elem["card"]))
    save = Game(tabPlayerInLife)
    save.tabPlayerInLife=tabPlayerInLife

    return save
