from useful_functions import *
import ascii_art

class Wearwolf: # test commit
    def __init__(self, id):
        self.name = "Loup garou"
        self.ascii = ascii_art.WEREWOLF
        self.id = id


    def actionWearwolf(self, tabPlayerInLife):
        """
        Input: lst tabPlayerInLife (table listing the player objects of living players)
        Output: Player object (player voted by the wearwolf)
        Action: Werewolves must choose one person to kill each night.
        """
        expected_results = [str(i) for i in range(1,len(tabPlayerInLife)+1)]
        print(expected_results)
        choicePlayer = int(playerChoice("Entrez le numéro du joueur que vous shouaitez éliminer: ", expected_results, self.id.IsHost, self.id))
        return choicePlayer

class Villager:
    def __init__(self, id):
        self.name = "Villageoi"
        self.ascii = ascii_art.VILLAGER
        self.id = id

    def actionVillager(self):
        "A voir plus tard"
        return 0
    
class Seer:
    def __init__(self, id):
        self.name = "Voyante"
        self.ascii = ascii_art.SEER
        self.id = id

    def actionSeer(self, tabPlayerInLife):
        """
        Input: lst tabPlayerInLife (table listing the player objects of living players)
        Output: str choicePlayer (return the name of the choosing person and his associate card)
        Action: The seer can choose to see the card of a person of her choice each night. 
        """
        expected_results = [str(i) for i in range(1,len(tabPlayerInLife)+1)]
        choicePlayer = int(playerChoice("Entrez le numéro du joueur dont vous souhaitez voir la carte: ", expected_results, self.id.IsHost, self.id))
        playerVoted = tabPlayerInLife[choicePlayer-1]
        return f"Le rôle de {playerVoted.name} est: {playerVoted.card.name}"
    
class Thief:
    def __init__(self, id):
        self.name="Voleur"
        self.ascii = ascii_art.THIEF
        self.id = id

    def actionThief(self, tabPlayerInLife, thiefName):
        """
        Input: lst tabPlayerInLife (table listing the player objects of living players)
        Output: Player object (the person whose card is to be exchanged)
        Action: The thief can choose to swap his card with that of another player (on the first night) 
        and then players who become thieves in turn can also swap their cards. 
        """
        choicePlayer = int(playerChoice("Voulez vous échanger votre carte avec un joueur?\n    1: oui\n    2: non\n\nChoix: ", ["1","2"], self.id.IsHost, self.id))
        if choicePlayer == 1:
            expected_results = [str(i) for i in range(1, len(tabPlayerInLife) + 1) if tabPlayerInLife[i-1].name != thiefName]
            choicePlayer = int(playerChoice("\nEntrez le numéro du joueur avec le quel vous voulez échanger votre carte: ", expected_results, self.id.IsHost, self.id))
            return tabPlayerInLife[choicePlayer-1]


class Hunter:
    def __init__(self, id):
        self.name="Chasseur"
        self.ascii = ascii_art.HUNTER
        self.id = id
    
    def actionHunter(self,tabPlayerInLife):

        """Action : Ask the player to choose a player to kill when the Hunter dies
           Input : list (tab of all the players in life)
           Output : Player object (Player selected by the Hunter)"""
        
        prompt = "\n Entrez le numéro du joueur que vous souhaitez éliminer: \n "
        expectedResults = [str(i) for i in range(1,len(tabPlayerInLife)+1)]
        choiceKillPlayer = int(playerChoice(prompt, expectedResults, self.id.IsHost, self.id))

        return tabPlayerInLife[choiceKillPlayer-1]

class Witch:
    def __init__(self, id):
        self.name = "Sorcière"
        self.ascii = ascii_art.WITCH
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
            whatToDo=int(playerChoice(prompt, expectedResults, self.id.IsHost, self.id))

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
            choiceKillPlayer = int(playerChoice(prompt, expectedResults, self.id.IsHost, self.id))
            self.potionPoison = False

        else:
            choiceToSave=True
            prompt = "\n Entrez le numéro du joueur que vous souhaitez éliminer: \n \n"
            expectedResults = [str(i) for i in range(1,len(tabPlayerInLife)+1)]
            choiceKillPlayer = int(playerChoice(prompt, expectedResults, self.id.IsHost, self.id))
            self.lifePotion = False
            self.potionPoison = False

        choices=(choiceKillPlayer,choiceToSave)
        return choices

        
class Cupidon :
    def __init__(self, id):
        self.name = "Cupidon"
        self.ascii = ascii_art.CUPIDON
        self.id = id

    def actionCupidon(self, tabPlayerInLife):
        """Action : during the night, Cupidon can choose 2 persons to link them. If one of them die, the other one also die
           Input : int length (number of player alive)
           Output : tuple choices, (tuple instance with the numbers of both players to link)"""
        secondPlayerToLink = 0
        prompt = "\nentrez le numéro de la première personne à lier : "
        expectedResults = [str(i) for i in range(1,len(tabPlayerInLife)+1)]
        firstPlayerToLink = int(playerChoice(prompt, expectedResults, self.id.IsHost, self.id))

        prompt = "\nentrez le numéro de la deuxième personne à lier : "
        while secondPlayerToLink == 0 or secondPlayerToLink == firstPlayerToLink:
            secondPlayerToLink = int(playerChoice(prompt, expectedResults, self.id.IsHost, self.id))
        
        choices = (firstPlayerToLink-1, secondPlayerToLink-1)
        return choices
    
class LittleGirl:
    def __init__(self, id):
        self.name = "Petite fille"
        self.ascii = ascii_art.LITTLE_GIRL
        self.id = id