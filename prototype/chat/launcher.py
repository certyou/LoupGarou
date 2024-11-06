import subprocess
import sys
import os

# Fonction pour lancer un script Python dans une nouvelle console
def open_new_console(script_name):
    try:
        # Utiliser 'start' pour ouvrir une nouvelle console sur Windows
        subprocess.Popen(['start', 'cmd', '/K', sys.executable, script_name], shell=True)
    except Exception as e:
        print(f"Erreur lors de l'ouverture de la console pour {script_name}: {e}")


def main() :
    chat_path = os.path.join(os.path.dirname(__file__), 'chat.py')
    game_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'main_reseau.py')
    chatInputPath = os.path.join(os.path.dirname(__file__), 'chatInput.py')

    open_new_console(chat_path)  # Chat py
    #open_new_console(game_path)  # Ouvrir la deuxième console
    open_new_console(chatInputPath)

if __name__ == '__main__':
    main()
