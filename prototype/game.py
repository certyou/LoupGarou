import time
from random import randint, choice
from role import *
from player import Player
import useful_functions as utils
from ascii_art import *
import save as s

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
            2:[Wearwolf(0), Seer(0)], # use for test only
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
        for i in range(0,len(self.listOfPlayers)):
                message=f"\n\n {self.listOfPlayers[i].card.ascii} \n\n Vous êtes {self.listOfPlayers[i].card.name}\n"
                SendMessage(self.listOfPlayers[i], message)



    def day(self):
        # ----------- Mayor Vote ------------------
        if self.nbTurn == 1:
            utils.broadcastMessage("---------------- Vote du maire ----------------\n\n"+MAIRE, self.tabPlayerInLife)
            self.mayorVote()
            utils.broadcastMessage(f"\nVous avez élu(e) {self.mayor.name} en tant que nouveau maire du village.\nSon vote compte à présent double.\n\n", self.tabPlayerInLife)

        # ----------- Vote ------------------
        strlistOfPlayer = f"---------------- Vote du Village ----------------\n\n{VOTE}\n\n{self.PrintPlayerInLife()}"
        maxVotedPlayer = {"player":None, "nbVote":0}
        # making player vote
        utils.broadcastMessage(strlistOfPlayer, self.listOfPlayers)
        for player in self.tabPlayerInLife:
            vote = int(utils.playerChoice("\nvotre vote : ", [str(x+1) for x in range(len(self.tabPlayerInLife))], player.IsHost, player))-1
            if player == self.mayor:
                self.tabPlayerInLife[vote].addVote(2)
            else:
                self.tabPlayerInLife[vote].addVote()
        print()
        # counting and reseting vote
        maxVotePlayer = self.playerWithMostVote(self.tabPlayerInLife)
        maxVotedPlayer = {"player":maxVotePlayer, "nbVote":maxVotePlayer.vote}
        
        # displaying results
        voteResult = "\n"+f"Le village a décidé d'éliminer {maxVotedPlayer['player'].name}, et leur sentence est irrévocable!"
        utils.broadcastMessage(voteResult, self.listOfPlayers)
        SendRequest(maxVotedPlayer['player'].id, MORT, False)
        self.tabPlayerInLife.remove(maxVotedPlayer['player'])

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
        
        mayor = self.playerWithMostVote(tabOfParticipant)
        self.mayor = mayor
        mayor.increment = 2
        mayor.resetVote()
        
    def playerWithMostVote(self, tabPlayer):
        """
        Arg :
            - :tabPlayer: lst of Player object
        Out : 
            - :maxVotePlayer: Player object, player with the most vote or random player if draw
        """
        utils.broadcastMessage("\nVoici les votes qui ont eu lieu: ", self.listOfPlayers)
        maxVote = -1
        for player in tabPlayer:
            utils.broadcastMessage("\n"+f"{player.name} --> {player.vote}", self.listOfPlayers)
            if player.vote > maxVote:
                maxVote = player.vote
                maxVotePlayer = player
            elif player.vote == maxVote:
                temp = [player, maxVotePlayer]
                maxVotePlayer = choice(temp)
            player.resetVote()
        return maxVotePlayer
    
    def night(self):
        # ----------- first night ------------------
        if self.nbTurn == 1:
            # cupidon
            pass
            # thief
        
        # seer
        for player in self.tabPlayerInLife:
            if player.card.name == "Voyante":
                utils.SendMessage(player, self.PrintPlayerInLife())
                target = player.card.actionSeer(self.tabPlayerInLife) + "\n"
                utils.SendMessage(player, target)

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
        isWin = (False, "No one")
        while not isWin[0]:
            self.nbTurn += 1
            utils.broadcastMessage("\nle village s'endort\n\n"+COUCHER_DE_SOLEIL+"\n\n", self.listOfPlayers)
            print(self.tabPlayerInLife[1].id)
            save=int(playerChoice(("\n\n voulez sauvegarder la partie ? :\n -1 : Oui\n -2 : Non\nChoix: "),["1","2"]))
            if save == 1:
                saveName = input("Quel nom voulez vous donner a votre sauvegarde ? : ")
                s.save(self,saveName)
                quit=int(playerChoice(("\n\n voulez vous quitter la partie ? :\n -1 : Oui\n -2 : Non\nChoix: "),["1","2"]))
                if quit == 1:
                    utils.broadcastMessage("\nl'hôte a décidé de sauvegarder et quitter la partie. Vous allez être déconnecté.\n\n", self.listOfPlayers)
                    return None
            self.night()
            utils.broadcastMessage("\nle jour se lève\n\n"+LEVER_DE_SOLEIL+"\n\n", self.listOfPlayers)
            self.day()
            isWin = self.IsWin()
        utils.broadcastMessage(f"\nle(s) {isWin[1]} a/ont gagné(s) !!!\n\n", self.listOfPlayers)

    def PrintPlayerInLife(self):
        message = f"Joueurs en vie:\n"
        for x in range(len(self.tabPlayerInLife)):
            message += f"    {x+1} - {self.tabPlayerInLife[x].name}\n"
        return message
    

    def KillPlayer(self, victim, killer=None):
        victim2 = None

        if killer == None:
            # displaying results
            voteResult = f"Le village a décidé d'éliminer {victim.name}, et leur sentence est irrévocable.\n"

        elif killer.card.name == "Loup garou":
            voteResult = f"{victim.name} a été dévoré par les loups garou !\n"

        elif killer.card.name == "Sorcière":
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

