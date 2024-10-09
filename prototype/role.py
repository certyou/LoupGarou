import useful_functions

class Wearwolf: # test commit
    def __init__(self, id):
        self.name = "Loup garou"
        self.id = id

    def ActionWearwolf(self):
        ChoiseKillPlayer = str(input("Entrez le nom du joueur que vous shouaitez éliminer: "))
        return ChoiseKillPlayer.lower()

class Villager:
    def __init__(self, id):
        self.name = "Villageoi"
        self.id = id

    def ActionVillager(self):
        return 0

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