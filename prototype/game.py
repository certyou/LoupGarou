from random import randint
from role import *
from player import Player
import useful_functions as utils


class Game:
    def __init__(self, ListOfPlayers, mayor=None):
        self.ListOfPlayers = ListOfPlayers
        self.NbPlayer = len(ListOfPlayers)
        self.tabPlayerInLife = []
        self.mayor = mayor
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
            self.tabPlayerInLife.append(player)
            TabAvailableCard.pop(card)


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
        for x in range(len(self.tabPlayerInLife)):
            message += f"   -{x+1}: {self.tabPlayerInLife[x].name}\n"
        print(message)
            
