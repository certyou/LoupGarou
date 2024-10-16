from random import randint
from role import *
from player import Player
import useful_functions as utils


class Game:
    def __init__(self, ListOfPlayers):
        self.ListOfPlayers = ListOfPlayers
        self.NbPlayer = len(ListOfPlayers)
        self.TabPlayerInLife = []
        self.DictRole = {
            2:[Wearwolf(0), Villager(0)], # use for test only
            3:[Wearwolf(0), Villager(0), Villager(0)], # use for test only
            4:[Wearwolf(0), Villager(0), Villager(0), Villager(0)],
            5:[Wearwolf(0), Villager(0), Villager(0), Villager(0), Villager(0)],
            6:[Wearwolf(0), Wearwolf(0), Villager(0), Villager(0), Villager(0), Villager(0)],
            7:[Wearwolf(0), Wearwolf(0), Villager(0), Villager(0), Villager(0), Villager(0), Villager(0)],
            8:[Wearwolf(0), Wearwolf(0), Villager(0), Villager(0), Villager(0), Villager(0), Villager(0), Villager(0)]
        }
    
    def GameInit(self):
        """
        """
        
        TabAvailableCard = self.DictRole[self.NbPlayer]
        for i in range(self.NbPlayer):
            player = self.ListOfPlayers[i]
            card = randint(0,len(TabAvailableCard)-1)
            player.setRole(card)
            self.TabPlayerInLife.append(player)
            TabAvailableCard.pop(card)

    def day(self):
        # chat

        # vote
        for player in self.TabPlayerInLife:
            list_of_player = [str(x)+1 for x in range(0)]
            utils.PlayerChoice("votre vote : ", [str(x) for x in range(len(self.TabPlayerInLife))], False, player)

    def night(self):
        pass

    
    def GameLoop(self):
        IsWin = False
        while not IsWin:
            print("le village s'endort")
            self.night()
            print("le jour se lève")
            self.day()


    def PrintPlayerInLife(self):
        message = f"Joueur en vie:\n   "
        for x in range(len(self.TabPlayerInLife)):
            message += f"   -{x+1}: {self.TabPlayerInLife[x].name}\n"
        print(message)
            
