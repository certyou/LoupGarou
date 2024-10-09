from random import randint
from role import *
from player import Player
import useful_functions as utils


class Game:
    def __init__(self, NbPlayer):
        self.NbPlayer = NbPlayer
        self.TabPlayerInLife = []
        self.DictRole = {
            2:[Wearwolf(0), Villager(0)], # use for test only
            3:[Wearwolf(0), Villager(0), Villager(0)], # use for test only
            4:[Wearwolf(0), Villager(0), Villager(0), Villager(0)],
            5:[Wearwolf(0), Villager(0), Villager(0), Villager(0), Villager(0)],
            6:[Wearwolf(0), Wearwolf(0), Villager(0), Villager(0), Villager(0), Villager(0)],
            7:[Wearwolf(0), Wearwolf(0), Villager(0), Villager(0), Villager(0), Villager(0), Villager(0)],
            8:[Wearwolf(0), Wearwolf(0), Villager(0), Villager(0), Villager(0), Villager(0), Villager(0), Villager(0)]
        }
    
    def GameStater(self):

        TabAvailableCard = self.DictDistibCard[self.NbPlayer]
        for i in range(1, self.NbPlayer+1):
            card = randint(0,len(TabAvailableCard)-1)
            player = Player(i, input(f"Entré le nom du joueur {i}: "), TabAvailableCard[card]) 
            self.TabPlayerInLife.append(player)
            if TabAvailableCard[card].name in self.DictRole.keys():
                self.DictRole[TabAvailableCard[card].name].append(player)
            else:
                self.DictRole[TabAvailableCard[card].name] = [player]
            TabAvailableCard.pop(card)

    
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
            
