from time import sleep
import os
from chatInput import textModifier

def main() :
    """Programme principale d'écriture du message sous forme d'une frame contenant des informations ordonnée
    frame générique : {Name€Command€text}
    retourne cette frame sur le fichier texte attitré.
    Ce programme est uniquement dédié à l'hôte
    """
    
    chemin = os.path.join(os.path.dirname(__file__), "hostChat.txt")
    

    textModifier(chemin, 'w', "")

    print(    """
          _           _                                     _ 
      ___| |__   __ _| |_    __ _  ___ _ __   ___ _ __ __ _| |
     / __| '_ \ / _` | __|  / _` |/ _ \ '_ \ / _ \ '__/ _` | |
    | (__| | | | (_| | |_  | (_| |  __/ | | |  __/ | | (_| | |
     \___|_| |_|\__,_|\__|  \__, |\___|_| |_|\___|_|  \__,_|_|
                            |___/                             

    """)

    print("""Bienvenue dans le chat du LOUP GAROU
           - Pour quitter le chat, tapez /exit
           - Pour changer de nom, tapez /name nom
          Amusez-vous bien !""")

    name = ""

    while True : 

        input_ = str(input("$ "))

        command = input_[1: input_.find(" ")] if input_[0] == '/' else None
        text = input_[input_.find(" ")+1:] if input_.find(" ") != len(input_) -1 else None

        if command == "name" :
            name = text
            continue

        if name == "" :
            print("Vous devez d'abord choisir un nom (commande : /name)")
            continue

        if input_ == "/exit" :
            return
        
        if input_ == "" :
            continue
       
        input_ = '{'+ name + "€" + input_[1: input_.find(" ")] + "§" + input_[input_.find(" ")+1:] + '}'


        textModifier(chemin, 'a', input_ )
        sleep(0.5)


if __name__ == '__main__' :
    main()