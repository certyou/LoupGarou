import useful_functions

class Wearwolf: # test commit
    def __init__(self, id):
        self.name = "Loup garou"
        self.id = id

    """
    Input: int length (number of players in life)
    Output: int choisePlayer (number of the player voted)
    Action: Werewolves must choose one person to kill each night.
    """
    def ActionWearwolf(self, length):
        expected_results = [i for i in range(1,length+1)]
        choisePlayer = PlayerChoice("Entrez le numéro du joueur que vous shouaitez éliminer: ", expected_results)
        return choisePlayer

class Villager:
    def __init__(self, id):
        self.name = "Villageoi"
        self.id = id

    def ActionVillager(self):
        "A voir plus tard"
        return 0

class Hunter:
    def __init__(self, id):
        self.name="Chasseur"
        self.id = id
    
    def actionHunter(self,length):

        """Action : Ask the player to choose a player to kill when the Hunter dies
           Input : int length (number of player alive)
           Output : int ChoiseKillPlayer (number of the player to kill)"""
        
        prompt = "Entrez le numéro du joueur que vous souhaitez éliminer: "
        expectedResults = [str(i) for i in range(1,length+1)]
        choiceKillPlayer = playerChoice(prompt, expectedResults)

        return choiceKillPlayer

class Witch:
    def __init__(self, id):
        self.name = "Sorcière"
        self.id = id
        self.lifePotion = True
        self.potionPoison = True

    def actionWitch(self,playerName,length):
        """Action : lors de la nuit, après les loup garous la sorcière peut utiliser sa potion de vie pour sauver un joueur et/ou sa potion de mort pour tuer un joueur. Elle peut également ne rien faire.
           Input : int length (number of player alive)
                   str playerName (Name of the player who will die)
           Output : tuple choices, (tuple instance with choiceKillPlayer and choiceToSave)
                    int choiceKillPlayer, (0 if no kill, else the number of the player to kill)
                    boolean choiceToSave, (True if the witch want to save a player life, else False)"""
        
        choiceToSave = False
        choices = ()

        if self.lifePotion == True and self.potionPoison == True :
            prompt = f"Sorcière, {playerName} va mourrir si vous ne faites rien. Vous avez plusieur choix :\n 0: ne rien faire \n 1: utiliser la potion de vie \n 2: utiliser la potion de mort \n 3: utiliser les deux potions"
            expectedResults = [0,1,2,3]

        elif self.lifePotion == True and self.potionPoison == False:
            prompt = f"Sorcière, {playerName} va mourrir si vous ne faites rien. Vous avez plusieur choix :\n 0: ne rien faire \n 1: utiliser la potion de vie"
            expectedResults = [0,1]

        elif self.lifePotion == False and self.potionPoison == True:
            prompt = f"Sorcière, {playerName} va mourrir si vous ne faites rien. Vous avez plusieur choix :\n 0: ne rien faire \n 1: utiliser la potion de mort"
            expectedResults = [0,1]

        else:
            print("Sorcière, vous n'avez plus de potions")
            whatToDo = 0

        if len(expectedResults != 1):
            whatToDo=playerChoice(prompt, expectedResults)

        if whatToDo == 0:
            choiceKillPlayer = 0
            choiceToSave = False

        elif whatToDo == 1 and self.lifePotion == True:
            choiceToSave = True
            choiceKillPlayer = 0
            self.lifePotion = False

        elif (whatToDo == 1 and self.potionPoison == True) or (whatToDo == 2):
            choiceToSave=True
            prompt = "Entrez le numéro du joueur que vous souhaitez éliminer: "
            expectedResults = [str(i) for i in range(1,length+1)]
            choiceKillPlayer = playerChoice(prompt, expectedResults)
            self.potionPoison = False

        else:
            choiceToSave=True
            prompt = "Entrez le numéro du joueur que vous souhaitez éliminer: "
            expectedResults = [str(i) for i in range(1,length+1)]
            choiceKillPlayer = playerChoice(prompt, expectedResults)
            self.lifePotion = False
            self.potionPoison = False

        choices=(choiceKillPlayer,choiceToSave)
        return choices

        

