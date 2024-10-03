class Wearwolf: # test commit
    def __init__(self, id):
        self.name = "Loup garou"
        self.id = id

    def action(self):
        ChoiseKillPlayer = str(input("Entrez le nom du joueur que vous shouaitez éliminer: "))
        return ChoiseKillPlayer.lower()

class Villager:
    def __init__(self, id):
        self.name = "Villageoi"
        self.id = id

    def action(self):
        return 0
