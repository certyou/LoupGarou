from useful_functions import *
import ascii_art


class Wearwolf:
    def __init__(self, id=None):
        """ Constructor of the Wearwolf class
        Args:
            - :id: socket, socket of the player
        Out:
            - /
        """
        self.name = "Loup garou"
        self.ascii = ascii_art.WEREWOLF
        self.id = id

class Villager:
    def __init__(self, id=None):
        """ Constructor of the Villager class
        Args:
            - :id: socket, socket of the player
        Out:
            - /
        """
        self.name = "Villageoi"
        self.ascii = ascii_art.VILLAGER
        self.id = id
    
class Seer:
    def __init__(self, id=None):
        """ Constructor of the Seer class
        Args:
            - :id: socket, socket of the player
        Out:
            - /
        """
        self.name = "Voyante"
        self.ascii = ascii_art.SEER
        self.id = id

    def actionSeer(self, tabPlayerInLife):
        """ choose a player from player in life and return his role
        Args:
            - :tabPlayerInLife: list of player, list of player still alive
        Out:
            - :str, return the role of the player
        """
        expected_results = [str(i) for i in range(1,len(tabPlayerInLife)+1)]
        choicePlayer = int(playerChoice("Entrez le numéro du joueur dont vous souhaitez voir la carte: ", expected_results, self.id.IsHost, self.id))
        playerVoted = tabPlayerInLife[choicePlayer-1]
        return f"Le rôle de {playerVoted.name} est: {playerVoted.card.name}"
    
class Thief:
    def __init__(self, id=None):
        """ Constructor of the Thief class
        Args:
            - :id: socket, socket of the player
        Out:
            - /
        """
        self.name="Voleur"
        self.ascii = ascii_art.THIEF
        self.id = id

    def actionThief(self, tabPlayerInLife, thiefName):
        """ choose a player from player in life and return it
        Args:
            - :tabPlayerInLife: list of player, list of player still alive
            - :thiefName: str, name of the thief
        Out:
            - :Player object, return the player selected by the thief
        """
        expected_results = [str(i) for i in range(1, len(tabPlayerInLife) + 1) if tabPlayerInLife[i-1].name != thiefName]
        choicePlayer = int(playerChoice("\nEntrez le numéro du joueur avec le quel vous voulez échanger votre carte: ", expected_results, self.id.IsHost, self.id))
        return tabPlayerInLife[choicePlayer-1]


class Hunter:
    def __init__(self, id=None):
        """ Constructor of the Hunter class
        Args:
            - :id: socket, socket of the player
        Out:
            - /
        """
        self.name="Chasseur"
        self.ascii = ascii_art.HUNTER
        self.id = id
    
    def actionHunter(self,tabPlayerInLife):
        """ choose a player from player in life and return it
        Args:
            - :tabPlayerInLife: list of player, list of player still alive
        Out:
            - :Player object, return the player selected by the hunter
        """
        prompt = "\n Entrez le numéro du joueur que vous souhaitez éliminer: \n "
        expectedResults = [str(i) for i in range(1,len(tabPlayerInLife)+1)]
        choiceKillPlayer = int(playerChoice(prompt, expectedResults, self.id.IsHost, self.id))
        return tabPlayerInLife[choiceKillPlayer-1]

class Witch:
    def __init__(self, id=None):
        """ Constructor of the Witch class
        Args:
            - :id: socket, socket of the player
        Out:
            - /
        """
        self.name = "Sorcière"
        self.ascii = ascii_art.WITCH
        self.id = id
        self.lifePotion = True
        self.potionPoison = True

    def actionWitch(self, tabPlayerInLife, player):
        """ select from four choices : do nothing, use life potion, use death potion or use both
        Args:
            - :tabPlayerInLife: list of player, list of player still alive
            - :player: Player object, player who will die
        Out:
            - :tuple: tuple with the player to kill and if the witch want to save a player
        """
        choiceToSave = False
        expectedResults=[]

        # if the witch has both potions
        if self.lifePotion == True and self.potionPoison == True :
            prompt = f"\n Sorcière, {player.name} va mourrir si vous ne faites rien. Vous avez plusieurs choix :\n 0: ne rien faire \n 1: utiliser la potion de vie \n 2: utiliser la potion de mort \n 3: utiliser les deux potions \n \n"
            expectedResults = [str(i) for i in range(4)]

        # if the witch has only the life potion
        elif self.lifePotion == True and self.potionPoison == False:
            prompt = f"\n Sorcière, {player.name} va mourrir si vous ne faites rien. Vous avez plusieurs choix :\n 0: ne rien faire \n 1: utiliser la potion de vie \n \n "
            expectedResults = ["0","1"]

        # if the witch has only the death potion
        elif self.lifePotion == False and self.potionPoison == True:
            prompt = f"\n Sorcière, {player.name} va mourrir si vous ne faites rien. Vous avez plusieurs choix :\n 0: ne rien faire \n 1: utiliser la potion de mort \n \n "
            expectedResults = ["0","1"]

        # if the witch has no potions
        else:
            HostSendMessage(self.id.id, "\n Sorcière, vous n'avez plus de potions \n \n", False)
            whatToDo = 0

        # if the witch has at least one potion
        if expectedResults != []:
            whatToDo=int(playerChoice(prompt, expectedResults, self.id.IsHost, self.id))

        # if the witch has no potions
        if whatToDo == 0:
            choiceKillPlayer = 0
            choiceToSave = False

        # if the witch want to save a player
        elif whatToDo == 1 and self.lifePotion == True:
            choiceToSave = True
            choiceKillPlayer = 0
            self.lifePotion = False

        # if the witch want to kill a player
        elif (whatToDo == 1 and self.potionPoison == True) or (whatToDo == 2):
            choiceToSave=True
            prompt = "\n Entrez le numéro du joueur que vous souhaitez éliminer: \n \n"
            expectedResults = [str(i) for i in range(1,len(tabPlayerInLife)+1)]
            choiceKillPlayer = int(playerChoice(prompt, expectedResults, self.id.IsHost, self.id))
            self.potionPoison = False

        # if the witch want to save and kill a player
        else:
            choiceToSave=True
            prompt = "\n Entrez le numéro du joueur que vous souhaitez éliminer: \n \n"
            expectedResults = [str(i) for i in range(1,len(tabPlayerInLife)+1)]
            choiceKillPlayer = int(playerChoice(prompt, expectedResults, self.id.IsHost, self.id))
            self.lifePotion = False
            self.potionPoison = False
        
        return (None, choiceToSave) if choiceKillPlayer == 0 else (tabPlayerInLife[choiceKillPlayer-1], choiceToSave)

        
class Cupidon :
    def __init__(self, id=None):
        """ Constructor of the Cupidon class
        Args:
            - :id: socket, socket of the player
        Out:
            - /
        """
        self.name = "Cupidon"
        self.ascii = ascii_art.CUPIDON
        self.id = id

    def actionCupidon(self, tabPlayerInLife):
        """ choose two players from player in life and return them
        Args:
            - :tabPlayerInLife: list of player, list of player still alive
        Out:
            - :tuple: tuple with the index of the two players selected by Cupidon
        """
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
    def __init__(self, id=None):
        """ Constructor of the LittleGirl class
        Args:
            - :id: socket, socket of the player
        Out:
            - /
        """
        self.name = "Petite fille"
        self.ascii = ascii_art.LITTLE_GIRL
        self.id = id