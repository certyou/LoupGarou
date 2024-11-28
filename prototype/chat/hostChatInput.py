from time import sleep
import os
from chatInput import textModifier

def main() :
    """Programme principale d'écriture du message sous forme d'une frame contenant des informations ordonnée
    frame générique : {Name€Command€text}
    retourne cette frame sur le fichier texte attitré.
    Ce programme est uniquement dédié à l'hôte
    """
       

    textModifier("hostChat.txt", 'w', "")


    name = ""

    while True : 

        input_ = str(input("$ "))

        if input_.find("{") != -1 and input_.find("}") != -1 :
            print("Vous ne pouvez pas utiliser {}")
            continue

        if input_[0] == '/' :
            command = input_[1: input_.find(" ")] if input_[0] == '/' else None
            text = input_[input_.find(" ")+1:] if input_.find(" ") != len(input_) -1 else None
            message = '{'+ name + "€" + command + "§" + text + '}'

            if input_ == "/exit" :
                return
            
            if command == "name" :
                name = text
                continue
           
        else :
            command = None
            text = input_ 
            message = '{'+ name + "€None§" + text + '}'


        if name == "" :
            print("Vous devez d'abord choisir un nom (commande : /name)")
            continue


        if input_ == "" or input_ ==  " " :
            continue

        textModifier("hostChat.txt", 'a', message )
        sleep(0.5)


if __name__ == '__main__' :
    main()