class Player:

    def __init__(self, id, name, card):
        self.id = id
        self.name = name
        self.card = card
        self.vote = 0

    def AddVote(self):
        self.vote += 1
    
    def ResetVote(self):
        self.vote = 0

    def __str__(self):
        return f"id: {self.id}\nName: {self.name}\nCard: {self.card.name, self.card.id}"
