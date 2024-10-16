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
        # ----------- Chat ------------------

        # ----------- Vote ------------------
        listOfPlayer = self.PrintPlayerInLife()
        maxVotedPlayer = {"player":None, "nbVote":0}
        # making player vote
        for player in self.TabPlayerInLife:
            vote = int(utils.playerChoice(listOfPlayer+"\nvotre vote : ", [str(x+1) for x in range(len(self.TabPlayerInLife))], player.IsHost, player))-1
            self.TabPlayerInLife[vote].addVote()
        print()
        # counting and reseting vote
        for player in self.TabPlayerInLife:
            print(player.name, "-->", player.vote)
            if maxVotedPlayer["nbVote"] < player.vote:
                maxVotedPlayer = {"player":player, "nbVote":player.vote}

    def night(self):
        pass

    
    def GameLoop(self):
        IsWin = False
        while not IsWin:
            print("\nle village s'endort\n\n")
            self.night()
            print("\nle jour se lève\n\n")
            self.day()


    def PrintPlayerInLife(self):
        message = f"Joueurs en vie:\n"
        for x in range(len(self.TabPlayerInLife)):
            message += f"    {x+1} - {self.TabPlayerInLife[x].name}\n"
        return message
            
