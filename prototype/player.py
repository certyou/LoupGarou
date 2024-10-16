class Player:

    def __init__(self, id, name, IsHost):
        self.id = id
        self.name = name
        self.card = None
        self.vote = 0
        self.IsHost = IsHost

    def AddVote(self):
        self.vote += 1
    
    def ResetVote(self):
        self.vote = 0

    def setRole(self, role):
        self.card = role


    def __str__(self):
        return f"id: {self.id}\nName: {self.name}\nCard: {self.card.name, self.card.id}"
