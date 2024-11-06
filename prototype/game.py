from random import randint
import time
from role import *
from player import Player
import useful_functions as utils


class Game:
    def __init__(self, ListOfPlayers):
        self.listOfPlayers = ListOfPlayers
        self.listOfRole = []
        self.nbPlayer = len(ListOfPlayers)
        self.tabPlayerInLife = []
        self.nbTurn = 0
        self.lovers = []
        self.dictRole = {
            2:[Wearwolf(0), Villager(0)], # use for test only
            3:[Wearwolf(0), Villager(0), Cupidon(0)], # use for test only
            4:[Wearwolf(0), Villager(0), Villager(0), Villager(0)],
            5:[Wearwolf(0), Villager(0), Villager(0), Villager(0), Villager(0)],
            6:[Wearwolf(0), Wearwolf(0), Villager(0), Villager(0), Villager(0), Villager(0)],
            7:[Wearwolf(0), Wearwolf(0), Villager(0), Villager(0), Villager(0), Villager(0), Villager(0)],
            8:[Wearwolf(0), Wearwolf(0), Villager(0), Villager(0), Villager(0), Villager(0), Villager(0), Villager(0)]
        }
    
    def GameInit(self):
        """
        In : /
        Out : /
        Distrib role in random order to all players
        """
        tabAvailableCard = self.dictRole[self.nbPlayer]
        for i in range(self.nbPlayer):
            player = self.listOfPlayers[i]
            card = tabAvailableCard[randint(0,len(tabAvailableCard)-1)]
            player.setRole(card)
            player.card.id = player
            self.tabPlayerInLife.append(player)
            tabAvailableCard.remove(card)
        # keep trace of active player's role
        self.listOfRole = [self.tabPlayerInLife[x].card for x in range(self.nbPlayer)]


    def day(self):
        # ---------------- Vote ------------------
        strListOfPlayer = self.PrintPlayerInLife() + "---------------- Vote du conseil ----------------\n"
        maxVotedPlayer = {"player":None, "nbVote":0}
        # making player vote
        utils.broadcastMessage(strListOfPlayer, self.listOfPlayers)
        for player in self.tabPlayerInLife:
            vote = int(utils.playerChoice("votre vote : ", [str(x+1) for x in range(len(self.tabPlayerInLife))], player.IsHost, player))-1
            self.tabPlayerInLife[vote].addVote()
        # counting and reseting vote
        for player in self.tabPlayerInLife:
            utils.broadcastMessage(player.name + " --> " + str(player.vote) + "\n", self.listOfPlayers)
            if maxVotedPlayer["nbVote"] < player.vote:
                maxVotedPlayer = {"player":player, "nbVote":player.vote}
            player.resetVote()
        # displaying results
        voteResult = f"Le village a décidé d'éliminer {maxVotedPlayer['player'].name}, et leur sentence est irrévocable."
        utils.broadcastMessage(voteResult, self.listOfPlayers)
        self.tabPlayerInLife.remove(maxVotedPlayer['player'])
        

    def night(self):
        # ---------------- first night ----------------
        if self.nbTurn == 1:
            # cupidon
            pass
            # voleur
    
    def IsWin(self):
        countOfWerewolf = 0
        countOfVillager = 0
        for role in self.listOfRole:
            if role.name == "Loup garou":
                countOfWerewolf += 1
            else:
                countOfVillager += 1
        if len(self.tabPlayerInLife) <= countOfWerewolf:
            return True, "Loup garou"
        elif countOfWerewolf == 0:
            return True, "Villageoi"
        elif len(self.tabPlayerInLife) == len(self.lovers) == 2:
            return True, "Amoureux"
        else:
            return False, "No one"
    
    def GameLoop(self):
        isWin = False
        while not isWin:
            self.nbTurn += 1
            utils.broadcastMessage("\nle village s'endort\n\n", self.listOfPlayers)
            self.night()
            utils.broadcastMessage("\nle jour se lève\n\n", self.listOfPlayers)
            self.day()


    def PrintPlayerInLife(self):
        message = f"Joueurs en vie:\n"
        for x in range(len(self.tabPlayerInLife)):
            message += f"    {x+1} - {self.tabPlayerInLife[x].name}\n"
        return message