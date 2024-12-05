from chat.chatInput import textModifier
import useful_functions


class Player:
    def __init__(self, id, name, isHost):
        """ Player object
        Arg:
            - :id: int, id of the player
            - :name: str, name of the player
            - :isHost: bool, if the player is the host
        Out:
            - /
        """
        self.id = id
        self.name = name
        self.card = None
        self.vote = 0
        self.IsHost = isHost
        self.mayor = False

    def addVote(self, increment=1):
        """ Add a vote to the player
        Arg:
            - :increment: int, number of vote to add
        Out:
            /
        """
        self.vote += increment
    
    def resetVote(self):
        """ Reset the vote of the player
        Arg:
            /
        Out:
            /
        """
        self.vote = 0

    def setRole(self, role):
        """ Set the role of the player
        Arg:
            - :role: object, role of the player
        Out:
            /
        """
        self.card = role
        if self.card.name == "Loup garou" : # if the player is a werewolf, write permission to discuss in the private chat of wearwolf in a file
            if self.IsHost :
                textModifier("role.txt", "w", "1")
            else :
                useful_functions.HostSendMessage(self.id, "⌈⌈loup", False)
        elif self.card.name == "Petite fille" : # if the player is the little girl, write permission to see in the private chat of wearwolf in a file
            if self.IsHost :
                textModifier("role.txt", "w", "2")

    def __str__(self):
        """ Return the string representation of the player
        Arg:
            /
        Out:
            - :str, string representation of the player
        """
        return f"id: {self.id}\nName: {self.name}\nCard: {self.card.name, self.card.id}"
