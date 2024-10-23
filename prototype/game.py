from random import randint
from role import *
from player import Player
import useful_functions as utils


class Game:
    def __init__(self, listOfPlayers, mayor=None):
        self.listOfPlayers = listOfPlayers
        self.listOfRole = []
        self.nbPlayer = len(listOfPlayers)
        self.tabPlayerInLife = []
        self.mayor = mayor
        self.nbTurn = 0
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
        """
        
        tabAvailableCard = self.dictRole[self.nbPlayer]
        for i in range(self.nbPlayer):
            player = self.listOfPlayers[i]
            card = randint(0,len(tabAvailableCard)-1)
            player.setRole(card)
            self.tabPlayerInLife.append(player)
            tabAvailableCard.pop(card)
        self.listOfRole = [self.tabPlayerInLife[x].card for x in range(self.nbPlayer)]


    def day(self):
        # ----------- Mayor Vote ------------------
        if self.nbTurn == 1:
           self.mayorVote()


        # ----------- Vote ------------------
        listOfPlayer = self.PrintPlayerInLife()
        maxVotedPlayer = {"player":None, "nbVote":0}
        # making player vote
        utils.broadcastMessage(listOfPlayer, self.listOfPlayers)
        for player in self.tabPlayerInLife:
            vote = int(utils.playerChoice("\nvotre vote : ", [str(x+1) for x in range(len(self.tabPlayerInLife))], player.IsHost, player))-1
            self.tabPlayerInLife[vote].addVote()
        print()
        # counting and reseting vote
        for player in self.tabPlayerInLife:
            print(player.name, "-->", player.vote)
            if maxVotedPlayer["nbVote"] < player.vote:
                maxVotedPlayer = {"player":player, "nbVote":player.vote}
            player.resetVote()
        # displaying results
        voteResult = f"Le village a décidé d'éliminer {maxVotedPlayer['player'].name}, et leur sentence est irrévocable."
        utils.broadcastMessage(voteResult, self.listOfPlayers)
        self.tabPlayerInLife.remove(maxVotedPlayer['player'])


    def mayorVote(self):
        """
        
        """

        tabOfParticipant = []
        txtVote = "Qui voulez vous élire:\n"
        for i in range(len(self.tabPlayerInLife)):
            player = self.tabPlayerInLife[i]
            choiceParticipation = int(playerChoice("Voulez vous présenter au élection du maire:\n -1 : Oui\n -2 : Non\nChoix: ", ["1","2"], player.IsHost, player))
            if choiceParticipation == 1:
                tabOfParticipant.append(player)
                txtVote += f" -{i+1} : {player.name}\n"
        
        expectedResultsVote = [str(i+1) for i in range(len(tabOfParticipant))]
        txtVote += "Choix: "
        
        for player in self.tabPlayerInLife:
            choiceMayor = int(playerChoice(txtVote, expectedResultsVote, player.IsHost, player))
            tabOfParticipant[choiceMayor-1].addVote()
        
        mayor = self.playerWithMostVote(tabOfParticipant)
        self.mayor = mayor
        mayor.increment = 2


        
    def playerWithMostVote(self, tabPlayer):
        """
        Arg :
            - :tabPlayer: lst of Player object
        Out : 
            - :maxVotePlayer: Player object, player with the most vote
        """
        maxVote = tabPlayer[0].vote
        maxVotePlayer = tabPlayer[0]
        for player in tabPlayer[1:]:
            if player.vote > maxVote:
                maxVote = player.vote
                maxVotePlayer = player
        return maxVotePlayer
        

    def night(self):
        # ----------- first night ------------------
        if self.nbTurn == 1:
            # cupidon
            pass
            # voleur
        
        
    
    def GameLoop(self):
        IsWin = False
        while not IsWin:
            self.nbTurn += 1
            utils.broadcastMessage("\nle village s'endort\n\n",self.listOfPlayers)
            self.night()
            utils.broadcastMessage("\nle jour se lève\n\n",self.listOfPlayers)
            self.day()



    def PrintPlayerInLife(self):
        message = f"Joueurs en vie:\n"
        for x in range(len(self.tabPlayerInLife)):
            message += f"    {x+1} - {self.tabPlayerInLife[x].name}\n"
        return message