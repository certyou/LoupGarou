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
            2:[Wearwolf(), Witch()], # use for test only
            3:[Wearwolf(), Thief(), Cupidon()], # use for test only
            4:[Wearwolf(), Villager(), Villager(), Villager()],
            5:[Wearwolf(), Villager(), Villager(), Villager(), Villager()],
            6:[Wearwolf(), Wearwolf(), Villager(), Villager(), Villager(), Villager()],
            7:[Wearwolf(), Wearwolf(), Villager(), Villager(), Villager(), Villager(), Villager()],
            8:[Wearwolf(), Wearwolf(), Villager(), Villager(), Villager(), Villager(), Villager(), Villager()]
        }
    
    def GameInit(self):
        """
        In : /
        Out : /
        Distrib role in random order to all players
        """
        # select the rigth distibution of role in function of the number of player
        tabAvailableCard = self.dictRole[self.nbPlayer]
        for i in range(self.nbPlayer):
            player = self.listOfPlayers[i]
            card = tabAvailableCard[randint(0,len(tabAvailableCard)-1)]
            player.setRole(card)
            player.card.id = player # allows to find the player from his role
            self.tabPlayerInLife.append(player)
            tabAvailableCard.remove(card)
        # keep trace of active player's role
        self.listOfRole = [self.tabPlayerInLife[x].card for x in range(self.nbPlayer)]
        for i in range(0, len(self.listOfPlayers)):
                message=f"\n\n {self.listOfPlayers[i].card.ascii} \n\n Vous êtes {self.listOfPlayers[i].card.name}\n"
                utils.HostSendMessage(self.listOfPlayers[i].id, message, False)



    def day(self):
        # ----------- Mayor Vote ------------------
        if self.nbTurn == 2:
            utils.broadcastMessage("---------------- Vote du maire ----------------\n", self.listOfPlayers)
            self.mayorVote()
            utils.broadcastMessage(f"\nVous avez élu(e) {self.mayor.name} en tant que nouveau maire du village.\nSon vote compte à présent double.\n\n", self.listOfPlayers)

        # ----------- Vote ------------------
        strlistOfPlayer = f"---------------- Vote du Village ----------------\n{utils.PrintPlayerInLife(self.tabPlayerInLife)}"
        # send the list of players in life
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
        dead = {}
        # first night
        if self.nbTurn == 1:
            # ------------------ CUPIDON ------------------
            if any(isinstance(role, Cupidon) for role in self.listOfRole):
                for player in self.tabPlayerInLife:
                    if player.card.name == "Cupidon":
                        utils.HostSendMessage(player.id, utils.PrintPlayerInLife(self.tabPlayerInLife), False)
                        target = player.card.actionCupidon(self.tabPlayerInLife)
                        self.lovers.append(self.tabPlayerInLife[target[0]])
                        self.lovers.append(self.tabPlayerInLife[target[1]])
                        Message1 = f"Vous êtes tomber fou amoureux de {self.tabPlayerInLife[target[0]].name}, qui est {self.tabPlayerInLife[target[0]].card.name}\n\n"
                        Message2 = f"Vous êtes tomber fou amoureux de {self.tabPlayerInLife[target[1]].name}, qui est {self.tabPlayerInLife[target[1]].card.name}\n\n"
                        utils.HostSendMessage(self.tabPlayerInLife[target[0]].id, Message2, False)
                        utils.HostSendMessage(self.tabPlayerInLife[target[1]].id, Message1, False)

            # ------------------ THIEF ------------------
            if any(isinstance(role, Thief) for role in self.listOfRole):
                for player in self.tabPlayerInLife:
                    if player.card.name == "Voleur":
                        utils.HostSendMessage(player, utils.PrintPlayerInLife(self.tabPlayerInLife), False)
                        target = player.card.actionThief(self.tabPlayerInLife, player.name)
                        msg_to_thief = f"vous êtes désormais {target.card.name}\n"
                        msg_to_victim = "Vous avez été volé ! Vous êtes désormais le Voleur\n"
                        target.card, player.card = player.card, target.card
                        utils.HostSendMessage(player.id, msg_to_thief, False)
                        utils.HostSendMessage(target.id, msg_to_victim, False)
                        break

        # ------------------ SEER ------------------
        if any(isinstance(role, Seer) for role in self.listOfRole):
            for player in self.tabPlayerInLife:
                if player.card.name == "Voyante":
                    utils.HostSendMessage(player.id, utils.PrintPlayerInLife(self.tabPlayerInLife), False)
                    target = player.card.actionSeer(self.tabPlayerInLife) + "\n"
                    utils.HostSendMessage(player.id, target, False)

        # ------------------ WEARWOLF ------------------
        if any(isinstance(role, Wearwolf) for role in self.listOfRole):
            WearwolfInLife = []
            for player in self.tabPlayerInLife:
                if player.card.name == "Loup garou":
                    WearwolfInLife.append(player)
            # Vote
            strlistOfPlayer = f"---------------- Vote des Loups Garous ----------------\n{utils.PrintPlayerInLife(self.tabPlayerInLife)}"
            maxVotedPlayer = {"player":None, "nbVote":0}
            # making player vote
            utils.broadcastMessage(strlistOfPlayer, WearwolfInLife)
            for player in WearwolfInLife:
                vote = int(utils.playerChoice("\nvotre vote : ", [str(x+1) for x in range(len(self.tabPlayerInLife))], player.IsHost, player))-1
                self.tabPlayerInLife[vote].addVote()
            # counting and reseting vote
            victim = utils.playerWithMostVote(self.tabPlayerInLife, WearwolfInLife)
            dead["Loup garou"] = victim
        
        # ------------------ WITCH ------------------
        if any(isinstance(role, Witch) for role in self.listOfRole):
            for player in self.tabPlayerInLife:
                if player.card.name == "Sorcière":
                    utils.HostSendMessage(player.id, utils.PrintPlayerInLife(self.tabPlayerInLife), False)
                    choice = player.card.actionWitch(self.tabPlayerInLife, victim)
                    utils.HostSendMessage(player.id, choice, False)
            if choice[0] != None and choice[1]:
                dead = {"Sorcière" : choice[0]}
            elif choice[0] != None:
                dead["Sorcière"] = choice[0]
            elif choice[1]:
                dead = {}
        
        # kill players at the end of the night
        for key in dead:
            self.KillPlayer(dead[key], key)

    def IsWin(self):
        """
        Output: -str (str which contain the name of the winer(s))
                -boolean (true if sombody win and false otherwise)

        Goal: Know if sombody win to stop the game and print the winer(s)
        """
                
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
        """This is the main Game"""
        while True:
            self.nbTurn += 1
            utils.broadcastMessage("\nle village s'endort\n\n"+COUCHER_DE_SOLEIL+"\n\n", self.listOfPlayers)
            save=int(playerChoice(("\n\n voulez sauvegarder la partie ? :\n -1 : Oui\n -2 : Non\nChoix: "),["1","2"]))
            if save == 1:
                saveName = input("Quel nom voulez vous donner a votre sauvegarde ? : ")
                s.save(self,saveName)
                quit=int(playerChoice(("\n\n voulez vous quitter la partie ? :\n -1 : Oui\n -2 : Non\nChoix: "),["1","2"]))
                if quit == 1:
                    utils.broadcastMessage("\nl'hôte a décidé de sauvegarder et quitter la partie. Vous allez être déconnecté.\n\n", self.listOfPlayers)
                    return None
            self.night()
            isWin = self.IsWin()
            if isWin[0]:
                break
            utils.broadcastMessage("\nLe jour se lève\n\n"+LEVER_DE_SOLEIL+"\n\n", self.listOfPlayers)
            self.day()
            isWin = self.IsWin()
            if isWin[0]:
                break
        utils.broadcastMessage(f"\nLes {isWin[1]} ont gagnés !!!\n\n", self.listOfPlayers)
    

    def KillPlayer(self, victim, killer=None):
        """
        Imput: -victim: Player object (The player who have been killed)
               -killer: str (The role of the killer if he exist), None (automatic if there are no killer)
        Output: void

        Goal: -Print a personalised texte depending on the person killed and the circumstances of their death
              -Do all the acction link to the death of a player
        """

        victim2,victim3 = None, None
        isMayor = None
        isHunter = None
        if victim == self.mayor:
            isMayor = victim

        if killer == None:
            voteResult = f"Le village a décidé d'éliminer {victim.name}, et leur sentence est irrévocable.\n"
            utils.HostSendMessage(victim.id, f"\n\nLe village a décidé de vous éliminer et leur sentence est irrévocable!\n\n {MORT}", False)


        elif killer == "Loup garou":
            voteResult = f"{victim.name} a été dévoré par les loups garou !"
            utils.HostSendMessage(victim.id, f"\n\nLes loups garou vous ont dévoré!\n\n {MORT}", False)


        elif killer == "Sorcière":
            voteResult = f"La sorcière a décider de vaporiser {victim.name}"
            utils.HostSendMessage(victim.id, f"\n\nLa sorcière a décider de vous vaporiser!\n\n {MORT}", False)


        if victim.card.name =="Chasseur":
            isHunter = victim
        else:
            voteResult += f"\n{victim.name} étais {victim.card.name}\n\n"
        utils.broadcastMessage(voteResult, self.listOfPlayers)
        self.tabPlayerInLife.remove(victim)

        #If the player is a lover
        if victim in self.lovers:
            self.lovers.remove(victim)
            victim2 = self.lovers[0]
            if victim2 == self.mayor:
                isMayor = victim2
            voteResult = f"De plus {victim.name} et {victim2.name} était amoureux. {victim2.name} est donc mort de chagrin..."
            if victim.card.name =="Hunter":
                isHunter = victim
            else:
                voteResult += f"\n{victim2.name} étais {victim2.card.name}\n\n"
            utils.broadcastMessage(voteResult, self.listOfPlayers)
            utils.HostSendMessage(victim2.id, f"\n\nVous êtes mort de chagrin... !\n\n {MORT}", False)
            self.tabPlayerInLife.remove(victim2)
            self.lovers = []

        #If the player is the Hunter
        if isHunter != None:
            utils.broadcastMessage(f"{isHunter.name} était le chasseur et va donc entrainer un joueur avec lui dans la mort!",self.listOfPlayers)
            utils.HostSendMessage(isHunter.id,f"---------------- Choix du chasseur ----------------\n{self.PrintPlayerInLife()}", False)
            victim3 = isHunter.card.actionHunter(self.tabPlayerInLife)
            voteResult = f"\n{victim3.name} à étais abatu(e) par le chasseur.\n{victim3.name} étais {victim3.card.name}"
            utils.broadcastMessage(voteResult, self.listOfPlayers)
            utils.HostSendMessage(victim3.id, f"\n\nVous avez été tué par le chasseur !\n\n {MORT}", False)
            self.tabPlayerInLife.remove(victim3)
         
        #If one of the players is the mayor
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
            if role.id == victim  or role.id == victim2 or role.id == victim3:
                self.listOfRole.remove(role)