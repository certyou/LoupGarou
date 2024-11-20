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
    chemin = os.path.join(os.path.dirname(__file__), "chat.txt")

    textModifier(chemin, 'w', "")

    while True : 
        input_ = str(input("$ "))

        if input_[0] == '/' :
            if input_.find(" ") == len(input_) -1 :
                print("commande invalide")
                continue
                
            input_ = '{' + input_[1: input_.find(" ")] + "§" + input_[input_.find(" ")+1:] + '}'

            if input_ == "/exit" :
                    return

        else :
            input_ = "{None§" + input_ + "}"

        textModifier(chemin, 'a', input_ )
        sleep(0.5)


if __name__ == '__main__' :
    main()