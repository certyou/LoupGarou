from random import randint
from cartes import *
from player import Player
import useful_functions as utils


class Game:
    def __init__(self, NbPlayer):
        self.NbPlayer = NbPlayer
        self.TabPlayerInLife = []
        self.ListRole = [Wearwolf(i) for i in range((NbPlayer)//4)] + [Villager(j) for j in range(((NbPlayer)//4)*3)]
        print(self.ListRole)
    
    def GameStater(self):

        for i in range(1, self.NbPlayer+1):
            card = randint(0,len(self.ListRole)-1)
            player = Player(i, input(f"Entré le nom du joueur {i}: "), self.ListRole[card]) 
            self.TabPlayerInLife.append(player)
            if self.ListRole[card].name in self.DictRole.keys():
                self.DictRole[self.ListRole[card].name].append(player)
            else:
                self.DictRole[self.ListRole[card].name] = [player]
            self.ListRole.pop(card)

    
    def GameLoop(self):
        for player in self.TabPlayerInLife:
            print(f"C'est au tour du joueur {player.id}:\n")
            self.PrintPlayerInLife()
            PlayerChoise = player.card.action()

            if player.card.name == "Loup garou":
                for player in self.TabPlayerInLife:
                    if PlayerChoise == player.name.lower():
                        player.AddVote()


    def PrintPlayerInLife(self):
        message = f"Joueur en vie:\n   "
        for player in self.TabPlayerInLife:
            message += f"{player.id}: {player.name} / "
        print(message)
            
