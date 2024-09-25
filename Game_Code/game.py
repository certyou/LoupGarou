from random import randint
from cartes import *
from player import Player


class Game:
    def __init__(self):
        self.TabPlayerInLife = []
        self.DicoRole = {}
        self.DicoDistibCard = {2:[Wearwolf(0), Villager(0)]}
    
    def GameStater(self):

        while True:
            try:
                ChoiseNbPlayer = int(input("Choisissez le nombre de joueurs pour cette partie: "))
                assert ChoiseNbPlayer in self.DicoDistibCard.keys() 
                break
            except:
                print(f"Vous ne pouvez pas jouer avec {ChoiseNbPlayer} joueurs. Veuillez ressayer.\n\n")

        TabAvailableCard = self.DicoDistibCard[ChoiseNbPlayer]
        for i in range(1, ChoiseNbPlayer+1):
            card = randint(0,len(TabAvailableCard)-1)
            player = Player(i, input(f"Entré le nom du joueur {i}: "), TabAvailableCard[card]) 
            self.TabPlayerInLife.append(player)
            if TabAvailableCard[card].name in self.DicoRole.keys():
                self.DicoRole[TabAvailableCard[card].name].append(player)
            else:
                self.DicoRole[TabAvailableCard[card].name] = [player]
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
            