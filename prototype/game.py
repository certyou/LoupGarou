from random import randint
from role import *
import usefulFunctions as utils
from asciiArt import *
import save as s


class Game:
    def __init__(self, listOfPlayers):
        """ This function initialize the game with the list of players
        Args :
            - :listOfPlayers: list of Player object, list of players
        Out :
            /
        """
        self.listOfPlayers = listOfPlayers
        self.listOfRole = []
        self.nbPlayer = len(listOfPlayers)
        self.tabPlayerInLife = []
        self.saveName=""
        self.mayor = None
        self.nbTurn = 0
        self.lovers = []
        self.mayor = None
        self.dictRole = { # dict of role distribution in function of the number of player
            2:[Wearwolf(), Thief()], # use for test only
            3:[Wearwolf(), Seer(), Witch()], # use for test only
            4:[Wearwolf(), Seer(), Thief(), Hunter()],
            5:[Wearwolf(), Seer(), Witch(), Hunter(), Thief()],
            6:[Wearwolf(), Wearwolf(), Seer(), Witch(), Hunter(), Thief()],
            7:[Wearwolf(), Wearwolf(), Seer(), Witch(), Hunter(), Thief(), LittleGirl()],
            8:[Wearwolf(), Wearwolf(), Seer(), Witch(), Hunter(), Thief(), Cupidon(), LittleGirl()]
        }


    def gameInit(self):
        """ Distrib role in random order to all players
        Args:
            - self: Game object
        Out:
            /
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
                utils.hostSendMessage(self.listOfPlayers[i].id, message, False)


    def day(self):
        """
        This function is the day part of the game
        Args:
            - self: Game object
        Out:
            /
        """
        # ----------- Mayor Vote ------------------
        if self.nbTurn == 2: # if it's the second day, the mayor is elected
            utils.broadcastMessage("---------------- Vote du maire ----------------\n", self.listOfPlayers)
            self.mayorVote()
            utils.broadcastMessage(f"\nVous avez élu(e) {self.mayor.name} en tant que nouveau maire du village.\nSon vote comptera double à partir de maintenant.\n\n", self.listOfPlayers)

        # ----------- Vote ------------------
        strlistOfPlayer = f"---------------- Vote du Village ----------------\n{utils.printPlayerInLife(self.tabPlayerInLife)}"
        # send the list of players in life
        utils.broadcastMessage(strlistOfPlayer, self.listOfPlayers)
        for player in self.tabPlayerInLife:
            # making players vote
            vote = int(utils.playerChoice("\nQuel joueur voulez-vous éliminer : ", [str(x+1) for x in range(len(self.tabPlayerInLife))], player.isHost, player))-1
            if player == self.mayor: # if the player is the mayor, his vote count double
                self.tabPlayerInLife[vote].addVote(2)
            else:
                self.tabPlayerInLife[vote].addVote()
        # counting and reseting vote
        maxVotePlayer = utils.playerWithMostVote(self.tabPlayerInLife, self.listOfPlayers)
        maxVotedPlayer = {"player":maxVotePlayer, "nbVote":maxVotePlayer.vote}
        
        # displaying results
        self.killPlayer(maxVotedPlayer['player'])


    def mayorVote(self):
        """ This function is the mayor vote part of the game
        Args:
            - self: Game object
        Out:
            /
        """
        tabOfParticipant = []
        txtVote = "\nQui voulez-vous élire ?  :\n"
        nbParticipant = 1
        for i in range(len(self.tabPlayerInLife)):
            player = self.tabPlayerInLife[i]
            choiceParticipation = int(playerChoice("Voulez-vous vous présenter aux élections du maire:\n -1 : Oui\n -2 : Non\nChoix: ", ["1","2"], player.isHost, player))
            if choiceParticipation == 1: # if the player want to participate, add him to the list of participant
                tabOfParticipant.append(player)
                txtVote += f" -{nbParticipant} : {player.name}\n"
                nbParticipant += 1
        
        expectedResultsVote = [str(i+1) for i in range(len(tabOfParticipant))]
        txtVote += "Choix: "

        # making players vote
        for player in self.tabPlayerInLife:
            choiceMayor = int(playerChoice(txtVote, expectedResultsVote, player.isHost, player))
            tabOfParticipant[choiceMayor-1].addVote()

        # counting and reseting vote
        mayor = utils.playerWithMostVote(tabOfParticipant, self.listOfPlayers)
        self.mayor = mayor
        mayor.increment = 2
        mayor.resetVote()


    def night(self):
        """ This function is the night part of the game
        Args:
            - self: Game object
        Out:
            /
        """
        dead = {}
        thief = None
        # first night
        if self.nbTurn == 1:
            # ------------------ CUPIDON ------------------
            if any(isinstance(role, Cupidon) for role in self.listOfRole): # if there is a Cupidon in the game
                strlistOfPlayer = f"\n---------------- Tour de cupidon ----------------\n"
                utils.broadcastMessage(strlistOfPlayer, self.listOfPlayers)
                for player in self.tabPlayerInLife:
                    if player.card.name == "Cupidon":
                        # send the list of players in life
                        utils.hostSendMessage(player.id, "---------------- Tour de Cupidon ----------------\n" +utils.PrintPlayerInLife(self.tabPlayerInLife), False)
                        # making cupidon vote for the lovers
                        target = player.card.actionCupidon(self.tabPlayerInLife)
                        self.lovers.append(self.tabPlayerInLife[target[0]])
                        self.lovers.append(self.tabPlayerInLife[target[1]])
                        # send the result to the lovers
                        messageLover1 = f"Vous êtes tomber fou amoureux de {self.tabPlayerInLife[target[0]].name}, qui est {self.tabPlayerInLife[target[0]].card.name}\n\n"
                        messageLover2 = f"Vous êtes tomber fou amoureux de {self.tabPlayerInLife[target[1]].name}, qui est {self.tabPlayerInLife[target[1]].card.name}\n\n"
                        utils.hostSendMessage(self.tabPlayerInLife[target[0]].id, messageLover1, False)
                        utils.hostSendMessage(self.tabPlayerInLife[target[1]].id, messageLover2, False)

            # ------------------ THIEF ------------------
            if any(isinstance(role, Thief) for role in self.listOfRole):
                strlistOfPlayer = f"\n---------------- Tour du voleur ----------------\n"
                utils.broadcastMessage(strlistOfPlayer, self.listOfPlayers)
                for player in self.tabPlayerInLife:
                    if player.card.name == "Voleur":
                        # making thief vote for the role he want to steal
                        thief = player
                        utils.hostSendMessage(player.id, utils.printPlayerInLife(self.tabPlayerInLife), False)
                        targetOfThief = player.card.actionThief(self.tabPlayerInLife, player.name)
                        messageThief1 = f"Vous prendrez connaissance de votre nouveau rôle au lever du jour.\n"
                        messageThief2 = f"Vous êtes désormais {targetOfThief.card.name}\n"
                        messageVictim = "Vous avez été volé ! Vous êtes désormais le Vilageois\n"
                        utils.hostSendMessage(player.id, messageThief1, False)
                        break

        # ------------------ SEER ------------------
        if any(isinstance(role, Seer) for role in self.listOfRole): # if there is a Seer in the game
            strlistOfPlayer = f"\n---------------- Tour de la voyante ----------------\n"
            utils.broadcastMessage(strlistOfPlayer, self.listOfPlayers)
            for player in self.tabPlayerInLife:
                if player.card.name == "Voyante":
                    # send the list of players in life
                    utils.hostSendMessage(player.id, utils.printPlayerInLife(self.tabPlayerInLife), False)
                    # making seer vote for the player he want to see the role
                    target = player.card.actionSeer(self.tabPlayerInLife) + "\n"
                    # send the result to the seer
                    utils.hostSendMessage(player.id, target, False)

        # ------------------ WEARWOLF ------------------
        if any(isinstance(role, Wearwolf) for role in self.listOfRole): # if there is a Wearwolf in the game
            wearwolfInLife = []
            for player in self.tabPlayerInLife:
                if player.card.name == "Loup garou":
                    wearwolfInLife.append(player)
            # send the list of players in life
            strlistOfPlayer = f"\n---------------- Vote des Loups Garous ----------------\n"
            messageLoupGarou = f"{utils.printPlayerInLife(self.tabPlayerInLife)}"
            utils.broadcastMessage(strlistOfPlayer, self.listOfPlayers)
            utils.broadcastMessage(messageLoupGarou, wearwolfInLife)
            for player in wearwolfInLife: # making wearwolves vote for a victim
                vote = int(utils.playerChoice("\nQui souhaitez-vous dévorer ce soir : ", [str(x+1) for x in range(len(self.tabPlayerInLife))], player.isHost, player))-1
                self.tabPlayerInLife[vote].addVote()
            # counting and reseting vote
            victim = utils.playerWithMostVote(self.tabPlayerInLife, wearwolfInLife)
            # add the victim to the dead dict
            dead["Loup garou"] = victim
        
        # ------------------ WITCH ------------------
        if any(isinstance(role, Witch) for role in self.listOfRole): # if there is a Witch in the game
            strlistOfPlayer = f"\n---------------- Tour de la sorcière ----------------\n"
            utils.broadcastMessage(strlistOfPlayer, self.listOfPlayers)
            for player in self.tabPlayerInLife:
                if player.card.name == "Sorcière":
                    # send the list of players in life
                    utils.hostSendMessage(player.id, utils.printPlayerInLife(self.tabPlayerInLife), False)
                    # making witch vote for the victim to kill or save
                    choice = player.card.actionWitch(self.tabPlayerInLife, victim)
                    # send the result to the witch
                    utils.hostSendMessage(player.id, choice, False)
            if choice[0] != None and choice[1]: # if the witch decide to save the victim and kill someone else
                dead = {"Sorcière" : choice[0]}
            elif choice[0] != None: # if the witch decide to kill someone
                dead["Sorcière"] = choice[0]
            elif choice[1]: # if the witch decide to save the victim
                dead = {}

        # ------------------ END OF THE NIGHT ------------------
        strlistOfPlayer = f"\n---------------- Fin de la nuit ----------------\n"
        utils.broadcastMessage(strlistOfPlayer, self.listOfPlayers)
        # Exchange card if the thief has played
        if thief:
            thief.card =  targetOfThief.card
            thief.card.id = thief
            targetOfThief.card = Villager(targetOfThief)
            utils.hostSendMessage(thief.id, messageThief2, False)
            utils.hostSendMessage(targetOfThief.id, messageVictim, False)

        # kill players at the end of the night
        for key in dead:
            self.killPlayer(dead[key], key)


    def isWin(self):
        """ check if someone win the game
        Args:
            - self : Game object
        Out:
            - boolean : True if someone win the game, False else
            - str : Role(s) that win the game
        """
        countOfWerewolf = 0
        countOfVillager = 0
        for role in self.listOfRole: # check the equilibrium of the game
            if role.name == "Loup garou":
                countOfWerewolf += 1
            else:
                countOfVillager += 1
        if len(self.tabPlayerInLife) <= countOfWerewolf: # if the number of werewolf is greater than the number of villager, the werewolf win
            return True, "Loup garou"
        elif countOfWerewolf == 0: # if there is no more villager in life, the village win
            return True, "Villageoi"
        elif len(self.tabPlayerInLife) == len(self.lovers) == 2: # if lovers are the only one remainings then they win
            return True, "Amoureux"
        else:
            return False, "No one"


    def gameLoop(self):
        """ This function is the main loop of the game
        Args:
            - self: Game object
        Out:
            /
        """
        while True:
            self.nbTurn += 1
            utils.broadcastMessage("\nle village s'endort\n\n"+COUCHER_DE_SOLEIL+"\n\n", self.listOfPlayers)
            # Save the game
            s.save(self)
            utils.broadcastMessage("\nLa partie a été sauvegardée\n\n", self.listOfPlayers)
            # night part
            self.night()
            isWin = self.isWin()
            if isWin[0]: # if someone win the game, break the loop
                break
            utils.broadcastMessage("\nLe jour se lève\n\n"+LEVER_DE_SOLEIL+"\n\n", self.listOfPlayers)
            # day part
            self.day()
            isWin = self.isWin()
            if isWin[0]: # if someone win the game, break the loop
                break
        # display the winner
        utils.broadcastMessage(f"\nLes {isWin[1]} ont gagnés !!!\n\n", self.listOfPlayers)
        # disconnect all players
        for player in self.listOfPlayers:
            if not player.isHost:
                disconnect = "END_GAME/fin de la partie"
                player.id.sendall(disconnect.encode('utf-8'))
    

    def killPlayer(self, victim, killer=None):
        """ This function handle the death of a player
        Args:
            - self: Game object
            - victim: Player object (The player who have been killed)
            - killer: str (The role of the killer if he exist), None (automatic if there are no killer's role)
        Out:
            /
        """
        victim2,victim3 = None, None
        isMayor = None
        isHunter = None
        if victim == self.mayor: # if the victim is the mayor, he can choose a new mayor
            isMayor = victim

        if killer == None: # if there are no killer, this is the village's vote
            voteResult = f"Le village a décidé d'éliminer {victim.name}, et leur sentence est irrévocable.\n"
            utils.hostSendMessage(victim.id, f"\n\nLe village a décidé de vous éliminer et leur sentence est irrévocable!\n\n {MORT}", False)


        elif killer == "Loup garou": # if the killer's role is werewolf
            voteResult = f"{victim.name} a été dévoré par les loups garou !"
            utils.hostSendMessage(victim.id, f"\n\nLes loups garou vous ont dévoré!\n\n {MORT}", False)


        elif killer == "Sorcière": # if the killer's role is witch
            voteResult = f"La sorcière a décider de vaporiser {victim.name}"
            utils.hostSendMessage(victim.id, f"\n\nLa sorcière a décider de vous vaporiser!\n\n {MORT}", False)


        if victim.card.name =="Chasseur": # if the victim is the Hunter
            isHunter = victim
        else:
            voteResult += f"\n{victim.name} étais {victim.card.name}\n\n"

        # broadcast the result of the vote
        utils.broadcastMessage(voteResult, self.listOfPlayers)
        self.tabPlayerInLife.remove(victim) # remove the victim from the list of player in life

        if victim in self.lovers: # If the player is a lover
            self.lovers.remove(victim)
            victim2 = self.lovers[0]
            if victim2 == self.mayor: # if the lover is the mayor, he can choose a new mayor
                isMayor = victim2
            voteResult = f"De plus {victim.name} et {victim2.name} était amoureux. {victim2.name} est donc mort de chagrin..."
            if victim.card.name =="Chasseur": # if the lover is the Hunter
                isHunter = victim
            else:
                voteResult += f"\n{victim2.name} étais {victim2.card.name}\n\n"
            
            # broadcast the result of the vote
            utils.broadcastMessage(voteResult, self.listOfPlayers)
            utils.hostSendMessage(victim2.id, f"\n\nVous êtes mort de chagrin... !\n\n {MORT}", False)
            self.tabPlayerInLife.remove(victim2)
            self.lovers = []

        # If the player is the Hunter
        if isHunter != None:
            utils.broadcastMessage(f"{isHunter.name} était le chasseur et va donc entrainer un joueur avec lui dans la mort!",self.listOfPlayers)
            utils.hostSendMessage(isHunter.id,f"---------------- Choix du chasseur ----------------\n{utils.printPlayerInLife(self.tabPlayerInLife)}", False)
            victim3 = isHunter.card.actionHunter(self.tabPlayerInLife)
            voteResult = f"\n{victim3.name} à étais abatu(e) par le chasseur.\n{victim3.name} étais {victim3.card.name}"
            utils.broadcastMessage(voteResult, self.listOfPlayers)
            utils.hostSendMessage(victim3.id, f"\n\nVous avez été tué par le chasseur !\n\n {MORT}", False)
            self.tabPlayerInLife.remove(victim3)
         
        # If one of the players is the mayor
        if isMayor != None:
            utils.broadcastMessage(f"{isMayor.name} était le maire et doit donc choisir un successeur.",self.listOfPlayers)
            message = self.printPlayerInLife()
            if isMayor.id == None:
                print(message)
            else:
                utils.SendRequest(isMayor.id, message, False)
            # making the mayor choose a new mayor
            expectedResultsVote = [str(i+1) for i in range(len(self.tabPlayerInLife))]
            choice = int(playerChoice("\nEntrez le numero de la personne qui sera votre successeur : ", expectedResultsVote, isMayor.isHost, isMayor))
            self.mayor = self.tabPlayerInLife[choice-1]
            utils.broadcastMessage(f"\nLe nouveau maire désigné est {self.mayor.name}. Son vote compte à présent double",self.listOfPlayers)

        for role in self.listOfRole: # remove the dead player from the list of active role
            if role.id == victim  or role.id == victim2 or role.id == victim3:
                self.listOfRole.remove(role)