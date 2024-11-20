import time
from random import randint, choice
from role import *
from player import Player
import useful_functions as utils
from ascii_art import *

class Game:
    def __init__(self, listOfPlayers):
        self.listOfPlayers = listOfPlayers
        self.listOfRole = []
        self.nbPlayer = len(listOfPlayers)
        self.tabPlayerInLife = []
        self.mayor = None
        self.nbTurn = 0
        self.lovers = []
        self.mayor = None
        self.dictRole = {
            2:[Cupidon(0),Villager(0)], # use for test only
            3:[Wearwolf(0), Thief(0), Cupidon(0)], # use for test only
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
        # ----------- Mayor Vote ------------------
        if self.nbTurn == 2:
            utils.broadcastMessage("---------------- Vote du maire ----------------\n", self.listOfPlayers)
            self.mayorVote()
            utils.broadcastMessage(f"\nVous avez élu(e) {self.mayor.name} en tant que nouveau maire du village.\nSon vote compte à présent double.\n\n", self.listOfPlayers)

        # ----------- Vote ------------------
        strlistOfPlayer = f"---------------- Vote du Village ----------------\n{utils.PrintPlayerInLife(self.tabPlayerInLife)}"
        maxVotedPlayer = {"player":None, "nbVote":0}
        # making player vote
        utils.broadcastMessage(strlistOfPlayer, self.listOfPlayers)
        for player in self.tabPlayerInLife:
            vote = int(utils.playerChoice("\nvotre vote : ", [str(x+1) for x in range(len(self.tabPlayerInLife))], player.IsHost, player))-1
            if player == self.mayor:
                self.tabPlayerInLife[vote].addVote(2)
            else:
                self.tabPlayerInLife[vote].addVote()
        # counting and reseting vote
        maxVotePlayer = utils.playerWithMostVote(self.tabPlayerInLife, self.listOfPlayers)
        maxVotedPlayer = {"player":maxVotePlayer, "nbVote":maxVotePlayer.vote}
        
        # displaying results
        self.KillPlayer(maxVotedPlayer['player'])


    def mayorVote(self):
        """
        This fonction add to self.mayor the player who has been voted to become Mayor
        """

        tabOfParticipant = []
        txtVote = "\nQui voulez vous élire ?  :\n"
        nbParticipant = 1
        for i in range(len(self.tabPlayerInLife)):
            player = self.tabPlayerInLife[i]
            choiceParticipation = int(playerChoice("Voulez vous vous présenter au élection du maire:\n -1 : Oui\n -2 : Non\nChoix: ", ["1","2"], player.IsHost, player))
            if choiceParticipation == 1:
                tabOfParticipant.append(player)
                txtVote += f" -{nbParticipant} : {player.name}\n"
                nbParticipant += 1
        
        expectedResultsVote = [str(i+1) for i in range(len(tabOfParticipant))]
        txtVote += "Choix: "
        
        for player in self.tabPlayerInLife:
            choiceMayor = int(playerChoice(txtVote, expectedResultsVote, player.IsHost, player))
            tabOfParticipant[choiceMayor-1].addVote()
        
        mayor = utils.playerWithMostVote(tabOfParticipant, self.listOfPlayers)
        self.mayor = mayor
        mayor.increment = 2
        mayor.resetVote()

    def night(self):
        # first night
        if self.nbTurn == 1:
            # ------------------ CUPIDON ------------------
            for player in self.tabPlayerInLife:
                if player.card.name == "Cupidon":
                    utils.SendMessage(player, utils.PrintPlayerInLife(self.tabPlayerInLife))
                    target = player.card.actionCupidon(self.tabPlayerInLife)
                    self.lovers.append(self.tabPlayerInLife[target[0]])
                    self.lovers.append(self.tabPlayerInLife[target[1]])
                    Message1 = f"Vous êtes tomber fou amoureux de {self.tabPlayerInLife[target[0]].name}, qui est {self.tabPlayerInLife[target[0]].card.name}\n\n"
                    Message2 = f"Vous êtes tomber fou amoureux de {self.tabPlayerInLife[target[1]].name}, qui est {self.tabPlayerInLife[target[1]].card.name}\n\n"
                    utils.SendMessage(self.tabPlayerInLife[target[0]], Message2)
                    utils.SendMessage(self.tabPlayerInLife[target[1]], Message1)

            # ------------------ THIEF ------------------
            for player in self.tabPlayerInLife:
                if player.card.name == "Voleur":
                    utils.SendMessage(player, utils.PrintPlayerInLife(self.tabPlayerInLife))
                    target = player.card.actionThief(self.tabPlayerInLife, player.name)
                    msg_to_thief = f"vous êtes désormais {target.card.name}\n"
                    msg_to_victim = "Vous avez été volé ! Vous êtes désormais le Voleur\n"
                    target.card, player.card = player.card, target.card
                    utils.SendMessage(player, msg_to_thief)
                    utils.SendMessage(target, msg_to_victim)
                    break

        # ------------------ SEER ------------------
        for player in self.tabPlayerInLife:
            if player.card.name == "Voyante":
                utils.SendMessage(player, utils.PrintPlayerInLife(self.tabPlayerInLife))
                target = player.card.actionSeer(self.tabPlayerInLife) + "\n"
                utils.SendMessage(player, target)

        # ------------------ WEARWOLF ------------------
        WearwolfInLife = []
        for player in self.tabPlayerInLife:
            if player.card.name == "Loup garou":
                WearwolfInLife.append(player)
        # Vote
        strlistOfPlayer = f"---------------- Vote des LG ----------------\n{utils.PrintPlayerInLife(self.tabPlayerInLife)}"
        maxVotedPlayer = {"player":None, "nbVote":0}
        # making player vote
        utils.broadcastMessage(strlistOfPlayer, WearwolfInLife)
        for player in WearwolfInLife:
            vote = int(utils.playerChoice("\nvotre vote : ", [str(x+1) for x in range(len(self.tabPlayerInLife))], player.IsHost, player))-1
            self.tabPlayerInLife[vote].addVote()
        # counting and reseting vote
        maxVotedPlayer = utils.playerWithMostVote(self.tabPlayerInLife, WearwolfInLife)
        self.KillPlayer(maxVotedPlayer, "Loup garou")

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
        while True:
            self.nbTurn += 1
            utils.broadcastMessage("\nle village s'endort\n\n"+COUCHER_DE_SOLEIL+"\n\n", self.listOfPlayers)
            self.night()
            isWin = self.IsWin()
            if isWin[0]:
                break
            utils.broadcastMessage("\nle jour se lève\n\n"+LEVER_DE_SOLEIL+"\n\n", self.listOfPlayers)
            self.day()
            isWin = self.IsWin()
            if isWin[0]:
                break
        utils.broadcastMessage(f"\nle(s) {isWin[1]} a/ont gagné(s) !!!\n\n", self.listOfPlayers)

    def PrintPlayerInLife(self):
        message = f"\nJoueurs en vie:\n"
        for x in range(len(self.tabPlayerInLife)):
            message += f"    {x+1} - {self.tabPlayerInLife[x].name}\n"
        return message
    

    def KillPlayer(self, victim, killer=None):
        """
        Imput: -victim: Player object (The player who have been killed)
               -killer: str (The role of the killer if he exist), None (automatic if there are no killer)
        Output: void

        Goal: Print a personalised texte depending on the person killed and the circumstances of their death
        """

        victim2 = None
        if victim == self.mayor:
            isMayor = victim
        else:
            isMayor = None

        if killer == None:
            voteResult = f"Le village a décidé d'éliminer {victim.name}, et leur sentence est irrévocable.\n"

        elif killer == "Loup garou":
            voteResult = f"{victim.name} a été dévoré par les loups garou !"

        elif killer == "Sorcière":
            voteResult = f"La sorcière a décider de vaporiser {victim.name}"

        utils.broadcastMessage(voteResult, self.listOfPlayers)
        self.tabPlayerInLife.remove(victim)

        if victim in self.lovers:
            self.lovers.remove(victim)
            victim2 = self.lovers[0]
            if victim2 == self.mayor:
                isMayor = victim2
            voteResult = f"De plus {victim.name} et {victim2.name} était amoureux. {victim2.name} est donc mort de chagrin..."
            utils.broadcastMessage(voteResult, self.listOfPlayers)
            self.tabPlayerInLife.remove(victim2)
            self.lovers = []

        if isMayor != None:
            utils.broadcastMessage(f"{isMayor.name} était le maire et doit donc choisir un successeur.",self.listOfPlayers)
            message = self.PrintPlayerInLife()
            if isMayor.id == None:
                print(message)
            else:
                utils.SendRequest(isMayor.id, message, False)
            expectedResultsVote = [str(i+1) for i in range(len(self.tabPlayerInLife))]
            choice = int(playerChoice("\nEntrez le numero de la personne qui sera votre successeur : ", expectedResultsVote, isMayor.IsHost, isMayor))
            self.mayor = self.tabPlayerInLife[choice-1]
            utils.broadcastMessage(f"\nLe nouveau maire désigné est {self.mayor.name}. Son vote compte à présent double",self.listOfPlayers)

        for role in self.listOfRole:
            if role.id == victim or role.id == victim2:
                self.listOfRole.remove(role) 

        
