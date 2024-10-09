from useful_functions import *

class Wearwolf: # test commit
    def __init__(self, id):
        self.name = "Loup garou"
        self.id = id


    def actionWearwolf(self, length):
        """
        Input: int length (number of players in life)
        Output: int choisePlayer (number of the player voted)
        Action: Werewolves must choose one person to kill each night.
        """
        expected_results = [i for i in range(1,length+1)]
        choicePlayer = PlayerChoice("Entrez le numéro du joueur que vous shouaitez éliminer: ", expected_results)
        return choicePlayer

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

    def actionWearwolf(self, tabPlayerInLife):
        """
        Input: lst tabPlayerInLife (table listing the player objects of living players)
        Output: str choicePlayer (return the name of the choosing person and his associate card)
        Action: The seer can choose to see the card of a person of her choice each night. 
        """
        expected_results = [i for i in range(1,len(tabPlayerInLife)+1)]
        choicePlayer = PlayerChoice("Entrez le numéro du joueur dont vous shouaitez voir la carte: ", expected_results)
        playerVoted = tabPlayerInLife[choicePlayer-1]
        return f"Le rôle de {playerVoted.name} est: {playerVoted.card.name}"
    
class Thief:
    def __init__(self, id):
        self.name="Voleur"
        self.id = id

    def actionTief(self, tabPlayerInLife):
        """
        Input: lst tabPlayerInLife (table listing the player objects of living players)
        Output: Player object (the person whose card is to be exchanged)
        Action: The thief can choose to swap his card with that of another player (on the first night) 
        and then players who become thieves in turn can also swap their cards. 
        """
        choicePlayer = PlayerChoice("Voulez vous échanger votre carte avec un joueur?\n    1: oui\n    2: non\n\n", [1,2])
        if choicePlayer == 1:
            expected_results = [i for i in range(1,len(tabPlayerInLife)+1)]
            choicePlayer = PlayerChoice("Entrez le numéro du joueur avec le quel vous voulez échanger votre carte: ", expected_results)
            return tabPlayerInLife[choicePlayer-1]

        
        return None


class Hunter:
    def __init__(self, id):
        self.name="Chasseur"
        self.id = id
    
    def ActionHunter(self,lenght):

        """Input : int lenght (number of player alive)
           Output : int ChoiseKillPlayer (number of the player to kill)
           Action : Ask the player to choose a player to kill when the Hunter dies"""
        
        prompt = "Entrez le numéro du joueur que vous souhaitez éliminer: "
        expected_results = [str(i) for i in range(1,lenght+1)]
        ChoiseKillPlayer = PlayerChoice(prompt, expected_results)

        return ChoiseKillPlayer

class Witch:
    def __init__(self, id):
        self.name="Sorcière"
        self.id = id
        self.Potion = True
        self.Poison = True
