from time import sleep
import os
from chatInput import textModifier

def main() :
    
    
    chemin = os.path.join(os.path.dirname(__file__), "hostChat.txt")
    

    textModifier(chemin, 'w', "")

    name = ""

    while True : 

        input_ = str(input("$ "))

        if input_[0] == '/' :

            if name == "" and input_[input_.find("/")+1:input_.find(" ")] == "name" :
                name = str(input("Name : "))
                continue

            if name == "" :
                continue

            if input_.find(" ") == len(input_) -1 :
                print("commande invalide")
                continue

            if input_ == "/exit" :
                    return
                
            input_ = '{' + input_[1: input_.find(" ")] + "§" + input_[input_.find(" ")+1:] + '}'

            

        else :
            input_ = "{None§" + input_ + "}"

        textModifier(chemin, 'a', input_ )
        sleep(0.5)


if __name__ == '__main__' :
    main()