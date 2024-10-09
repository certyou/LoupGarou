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
    

