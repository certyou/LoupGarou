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