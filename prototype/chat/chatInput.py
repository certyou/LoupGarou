from time import sleep
import os


def textModifier(chemin, mode='r', contenu=None):
    """
    Fonction pour lire, écrire ou ajouter du contenu à un fichier texte.

    Arguments :
    - chemin (str) : Le chemin du fichier.
    - mode (str) : Le mode de manipulation ('r', 'w', 'a').
    - contenu (str, optionnel) : Le texte à écrire ou ajouter si mode est 'ecrire' ou 'ajouter'.

    Retourne :
    - Le contenu du fichier si mode='r', sinon None.
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

        if input_ == "/exit" :
            return
        
        if input_[0] == '/' :
            if input_.find(" ") == -1 :
                continue
            input_ = '{' + input_[1: input_.find(" ")] + "§" + input_[input_.find(" ")+1:] + '}'

        else :
            input_ = "{None§" + input_ + "}"

        textModifier(chemin, 'a', input_ )
        sleep(0.5)


if __name__ == '__main__' :
    main()