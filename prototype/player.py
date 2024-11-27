from chat.chatInput import textModifier

class Player:

    def __init__(self, id, name, isHost):
        self.id = id
        self.name = name
        self.card = None
        self.vote = 0
        self.IsHost = isHost
        self.mayor = False


    def addVote(self, increment=1):
        self.vote += increment
    
    def resetVote(self):
        self.vote = 0

    def setRole(self, role):
        self.card = role

        if self.card.name == "Loup garou" :
            textModifier("role.txt", "w", "")
            textModifier("role.txt", "w", "1")
        elif self.card.name == "Petite fille" :
            textModifier("role.txt", "w", "")
            textModifier("role.txt", "w", "2")


    def __str__(self):
        return f"id: {self.id}\nName: {self.name}\nCard: {self.card.name, self.card.id}"
