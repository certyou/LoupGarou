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
            2:[Wearwolf(0), Thief(0)], # use for test only
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
        maxVotedPlayer = utils.playerWithMostVote(self.tabPlayerInLife, self.listOfPlayers)
        self.KillPlayer(maxVotedPlayer)

    def mayorVote(self):
        """
        This fonction add to self.mayor the player who has been voted to become Mayor
        """

        tabOfParticipant = []
        txtVote = "\nQui voulez vous élire ?  :\n"
        for i in range(len(self.tabPlayerInLife)):
            player = self.tabPlayerInLife[i]
            choiceParticipation = int(playerChoice("Voulez vous vous présenter au élection du maire:\n -1 : Oui\n -2 : Non\nChoix: ", ["1","2"], player.IsHost, player))
            if choiceParticipation == 1:
                tabOfParticipant.append(player)
                txtVote += f" -{i+1} : {player.name}\n"
        
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
                    utils.HostSendMessage(player.id, utils.PrintPlayerInLife(self.tabPlayerInLife), False)
                    #time.sleep(1)
                    target = player.card.actionCupidon(self.tabPlayerInLife)
                    self.lovers.append(self.tabPlayerInLife[target[0]])
                    self.lovers.append(self.tabPlayerInLife[target[1]])
                    Message1 = f"Vous êtes tomber fou amoureux de {self.tabPlayerInLife[target[0]].name}, qui est {self.tabPlayerInLife[target[0]].card.name}\n\n"
                    Message2 = f"Vous êtes tomber fou amoureux de {self.tabPlayerInLife[target[1]].name}, qui est {self.tabPlayerInLife[target[1]].card.name}\n\n"
                    utils.HostSendMessage(self.tabPlayerInLife[target[0]].id, Message2, False)
                    utils.HostSendMessage(self.tabPlayerInLife[target[1]].id, Message1, False)

            # ------------------ THIEF ------------------
            for player in self.tabPlayerInLife:
                if player.card.name == "Voleur":
                    utils.HostSendMessage(player.id, utils.PrintPlayerInLife(self.tabPlayerInLife), False)
                    #time.sleep(1)
                    target = player.card.actionThief(self.tabPlayerInLife, player.name)
                    msg_to_thief = f"vous êtes désormais {target.card.name}\n"
                    msg_to_victim = "Vous avez été volé ! Vous êtes désormais le Voleur\n"
                    target.card, player.card = player.card, target.card
                    utils.HostSendMessage(player.id, msg_to_thief, False)
                    utils.HostSendMessage(target.id, msg_to_victim, False)
                    break

        # ------------------ SEER ------------------
        for player in self.tabPlayerInLife:
            if player.card.name == "Voyante":
                utils.HostSendMessage(player.id, utils.PrintPlayerInLife(self.tabPlayerInLife), False)
                #time.sleep(1)
                target = player.card.actionSeer(self.tabPlayerInLife) + "\n"
                utils.HostSendMessage(player.id, target, False)

        # ------------------ WEARWOLF ------------------
        print(self.listOfRole)
        print(Wearwolf in self.listOfRole)
        if Wearwolf in self.listOfRole:
            WearwolfInLife = []
            for player in self.tabPlayerInLife:
                if player.card.name == "Loup garou":
                    WearwolfInLife.append(player)
            # Vote
            strlistOfPlayer = f"---------------- Vote des LG ----------------\n{utils.PrintPlayerInLife(self.tabPlayerInLife)}"
            maxVotedPlayer = {"player":None, "nbVote":0}
            # making player vote
            utils.broadcastMessage(strlistOfPlayer, WearwolfInLife)
            #time.sleep(1)
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

    def KillPlayer(self, victim, killer=None):
        victim2 = None

        if killer == None:
            # displaying results
            voteResult = f"Le village a décidé d'éliminer {victim.name}, et leur sentence est irrévocable.\n"

        elif killer == "Loup garou":
            voteResult = f"{victim.name} a été dévoré par les loups garou !\n"

        elif killer == "Sorcière":
            voteResult = f"La sorcière a décider de vaporiser {victim.name}\n"

        utils.broadcastMessage(voteResult, self.listOfPlayers)
        self.tabPlayerInLife.remove(victim)

        if victim in self.lovers:
            self.lovers.remove(victim)
            victim2 = self.lovers[0]
            voteResult = f"De plus {victim.name} et {victim2.name} était amoureux. {victim2.name} est donc mort de chagrin...\n"
            self.tabPlayerInLife.remove(victim2)
            self.lovers = []

        for role in self.listOfRole:
            if role.id == victim or role.id == victim2:
                self.listOfRole.remove(role)

