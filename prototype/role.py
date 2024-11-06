from useful_functions import *

class Wearwolf: # test commit
    def __init__(self, id):
        self.name = "Loup garou"
        self.id = id


    def actionWearwolf(self, tabPlayerInLife):
        """
        Input: lst tabPlayerInLife (table listing the player objects of living players)
        Output: Player object (player voted by the wearwolf)
        Action: Werewolves must choose one person to kill each night.
        """
        expected_results = [str(i) for i in range(1,len(tabPlayerInLife)+1)]
        print(expected_results)
        choicePlayer = int(playerChoice("Entrez le numéro du joueur que vous shouaitez éliminer: ", expected_results))
        return tabPlayerInLife[choicePlayer-1]

class Villager:
    def __init__(self, id):
        self.name = "Villageoi"
        self.id = id

    def actionVillager(self):
        "A voir plus tard"
        return 0
    
class Seer:
    def __init__(self, id):
        self.name="Voyante"
        self.id = id

    def actionSeer(self, tabPlayerInLife):
        """
        Input: lst tabPlayerInLife (table listing the player objects of living players)
        Output: str choicePlayer (return the name of the choosing person and his associate card)
        Action: The seer can choose to see the card of a person of her choice each night. 
        """
        expected_results = [str(i) for i in range(1,len(tabPlayerInLife)+1)]
        choicePlayer = int(playerChoice("Entrez le numéro du joueur dont vous shouaitez voir la carte: ", expected_results))
        playerVoted = tabPlayerInLife[choicePlayer-1]
        return f"Le rôle de {playerVoted.name} est: {playerVoted.card.name}"
    
class Thief:
    def __init__(self, id):
        self.name="Voleur"
        self.id = id

    def actionThief(self, tabPlayerInLife, thiefName):
        """
        Input: lst tabPlayerInLife (table listing the player objects of living players)
        Output: Player object (the person whose card is to be exchanged)
        Action: The thief can choose to swap his card with that of another player (on the first night) 
        and then players who become thieves in turn can also swap their cards. 
        """
        choicePlayer = playerChoice("Voulez vous échanger votre carte avec un joueur?\n    1: oui\n    2: non\n\nChoix: ", [1,2])
        if choicePlayer == 1:
            expected_results = [str(i) for i in range(1, len(tabPlayerInLife) + 1) if tabPlayerInLife[i-1].name != thiefName]
            choicePlayer = int(playerChoice("\nEntrez le numéro du joueur avec le quel vous voulez échanger votre carte: ", expected_results))
            return tabPlayerInLife[choicePlayer-1]

        return None


class Hunter:
    def __init__(self, id):
        self.name="Chasseur"
        self.id = id
    
    def actionHunter(self,tabPlayerInLife):

        """Action : Ask the player to choose a player to kill when the Hunter dies
           Input : int length (number of player alive)
           Output : int ChoiseKillPlayer (number of the player to kill)"""
        
        prompt = "\n Entrez le numéro du joueur que vous souhaitez éliminer: \n "
        expectedResults = [str(i) for i in range(1,len(tabPlayerInLife)+1)]
        choiceKillPlayer = int(playerChoice(prompt, expectedResults))

        return tabPlayerInLife[choiceKillPlayer-1]

class Witch:
    def __init__(self, id):
        self.name = "Sorcière"
        self.id = id
        self.lifePotion = True
        self.potionPoison = True

    def actionWitch(self,tabPlayerInLife, playerName):
        """Action : during the night, after werewolfs, the witch can choose to use her life potion or/and her death potion or nothing
           Input : int length (number of player alive)
                   str playerName (Name of the player who will die)
           Output : tuple choices, (tuple instance with choiceKillPlayer and choiceToSave)
                    int choiceKillPlayer, (0 if no kill, else the number of the player to kill)
                    boolean choiceToSave, (True if the witch want to save a player life, else False)"""
        
        choiceToSave = False
        choices = ()
        expectedResults=[]

        if self.lifePotion == True and self.potionPoison == True :
            prompt = f"\n Sorcière, {playerName} va mourrir si vous ne faites rien. Vous avez plusieurs choix :\n 0: ne rien faire \n 1: utiliser la potion de vie \n 2: utiliser la potion de mort \n 3: utiliser les deux potions \n \n"
            expectedResults = [0,1,2,3]

        elif self.lifePotion == True and self.potionPoison == False:
            prompt = f"\n Sorcière, {playerName} va mourrir si vous ne faites rien. Vous avez plusieurs choix :\n 0: ne rien faire \n 1: utiliser la potion de vie \n \n "
            expectedResults = [0,1]

        elif self.lifePotion == False and self.potionPoison == True:
            prompt = f"\n Sorcière, {playerName} va mourrir si vous ne faites rien. Vous avez plusieurs choix :\n 0: ne rien faire \n 1: utiliser la potion de mort \n \n "
            expectedResults = [0,1]

        else:
            print("\n Sorcière, vous n'avez plus de potions \n \n")
            whatToDo = 0

        if expectedResults:
            whatToDo=int(playerChoice(prompt, expectedResults))

        if whatToDo == 0:
            choiceKillPlayer = 0
            choiceToSave = False

        elif whatToDo == 1 and self.lifePotion == True:
            choiceToSave = True
            choiceKillPlayer = 0
            self.lifePotion = False

        elif (whatToDo == 1 and self.potionPoison == True) or (whatToDo == 2):
            choiceToSave=True
            prompt = "\n Entrez le numéro du joueur que vous souhaitez éliminer: \n \n"
            expectedResults = [str(i) for i in range(1,len(tabPlayerInLife)+1)]
            choiceKillPlayer = int(playerChoice(prompt, expectedResults))
            self.potionPoison = False

        else:
            choiceToSave=True
            prompt = "\n Entrez le numéro du joueur que vous souhaitez éliminer: \n \n"
            expectedResults = [str(i) for i in range(1,len(tabPlayerInLife)+1)]
            choiceKillPlayer = int(playerChoice(prompt, expectedResults))
            self.lifePotion = False
            self.potionPoison = False

        choices=(choiceKillPlayer,choiceToSave)
        return choices

        
class Cupidon :
    def __init__(self, id):
        self.name = "Cupidon"
        self.id = id

    def actionCupidon(self, length):
        """Action : during the night, Cupidon can choose 2 persons to link them. If one of them die, the other one also die
           Input : int length (number of player alive)
           Output : tuple choices, (tuple instance with the numbers of both players to link)"""
        secondPlayerToLink = 0
        prompt = "\n entrez le numéro de la première personne à lier : \n"
        expectedResults = [str(i) for i in range(1,length+1)]
        firstPlayerToLink = int(playerChoice(prompt, expectedResults))

        prompt = "\n entrez le numéro de la deuxième personne à lier : \n" 
        while secondPlayerToLink == 0 or secondPlayerToLink == firstPlayerToLink :
            secondPlayerToLink = int(playerChoice(prompt, expectedResults))
        
        choices = (firstPlayerToLink,secondPlayerToLink)
        return choices
