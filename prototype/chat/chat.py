from chatInput import textModifier
from time import time

import time

def chat():
    textFile = "prototype\\chat\\chat.txt"

    while True:
        time.sleep(0.5)
        command = textModifier(textFile, 'r')
        if len(command) != 0 :
            print(command)
            textModifier(textFile, 'w', "") #supprimer les données
        
        
    
if __name__ == '__main__':
    chat()

