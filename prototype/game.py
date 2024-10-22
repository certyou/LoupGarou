from random import randint
from role import *
from player import Player
import useful_functions as utils


class Game:
    def __init__(self, ListOfPlayers, mayor=None):
        self.ListOfPlayers = ListOfPlayers
        self.ListOfRole = []
        self.NbPlayer = len(ListOfPlayers)
        self.tabPlayerInLife = []
        self.mayor = mayor
        self.NbTurn = 0
        self.DictRole = {
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
        
        TabAvailableCard = self.DictRole[self.NbPlayer]
        for i in range(self.NbPlayer):
            player = self.ListOfPlayers[i]
            card = randint(0,len(TabAvailableCard)-1)
            player.setRole(card)
            player.card.id = player
            self.TabPlayerInLife.append(player)
            TabAvailableCard.pop(card)
        self.ListOfRole = [self.TabPlayerInLife[x].card for x in range(self.NbPlayer)]




    


    def day(self):
        # ----------- Vote ------------------
        listOfPlayer = self.PrintPlayerInLife()
        maxVotedPlayer = {"player":None, "nbVote":0}
        # making player vote
        utils.broadcastMessage(listOfPlayer, self.ListOfPlayers)
        for player in self.TabPlayerInLife:
            vote = int(utils.playerChoice("\nvotre vote : ", [str(x+1) for x in range(len(self.TabPlayerInLife))], player.IsHost, player))-1
            self.TabPlayerInLife[vote].addVote()
        print()
        # counting and reseting vote
        for player in self.TabPlayerInLife:
            print(player.name, "-->", player.vote)
            if maxVotedPlayer["nbVote"] < player.vote:
                maxVotedPlayer = {"player":player, "nbVote":player.vote}
            player.resetVote()
        # displaying results
        voteResult = f"Le village a décidé d'éliminer {maxVotedPlayer['player'].name}, et leur sentence est irrévocable."
        utils.broadcastMessage(voteResult, self.ListOfPlayers)
        self.TabPlayerInLife.remove(maxVotedPlayer['player'])

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
        
        return self.playerWithMostVote(tabOfParticipant)

        
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
        if self.NbTurn == 1:
            # cupidon
            pass
            # voleur
        
        
    
    def GameLoop(self):
        IsWin = False
        while not IsWin:
            self.NbTurn += 1
            utils.broadcastMessage("\nle village s'endort\n\n",self.ListOfPlayers)
            self.night()
            utils.broadcastMessage("\nle jour se lève\n\n",self.ListOfPlayers)
            self.day()



    def PrintPlayerInLife(self):
        message = f"Joueurs en vie:\n"
        for x in range(len(self.TabPlayerInLife)):
            message += f"    {x+1} - {self.TabPlayerInLife[x].name}\n"
        return message