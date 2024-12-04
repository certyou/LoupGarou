from time import sleep
import os


def textModifier(chemin, mode='r', contenu=None):
    """
    Function to read, write, or append content to a text file.

    Arguments:
    - chemin (str): The path of the file.
    - mode (str): The mode of operation ('r', 'w', 'a').
    - contenu (str, optional): The text to write or append if mode is 'w' or 'a'.

    Returns:
    - The content of the file if mode='r', otherwise None.
    """

    chemin = os.path.join(os.path.dirname(__file__), chemin)

    if mode == 'r':
        with open(chemin, 'r', encoding='utf-8') as fichier:
            return fichier.read()

    elif mode == 'w':
        with open(chemin, 'w', encoding='utf-8') as fichier:
            fichier.write(contenu)

    elif mode == 'a':
        with open(chemin, 'a', encoding='utf-8') as fichier:
            fichier.write(contenu)

def main() :
    """Programme principale d'écriture du message sous forme d'une frame contenant des informations ordonnée
    frame générique : {Name€Command€text}
    retourne cette frame sur le fichier texte attitré.
    """

    textModifier("chat.txt", 'w', "")

    
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

        textModifier("chat.txt", 'a', message )
        sleep(0.5)


if __name__ == '__main__' :
    main()