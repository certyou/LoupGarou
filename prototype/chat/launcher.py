import subprocess
import sys
import os
# Function to launch a Python script in a new console
def open_new_console(script_name):
    try:
        # Use 'start' to open a new console on Windows
        subprocess.Popen(['start', 'cmd', '/K', sys.executable, script_name], shell=True)
    except Exception as e:
        print(f"Erreur lors de l'ouverture de la console pour {script_name}: {e}")


def main() :
    # launch the game
    game_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'main_reseau.py')
    open_new_console(game_path)  # open the game in a new console


def launchHostChat() :
    # launch the input and the server chat of the host
    chat_path = os.path.join(os.path.dirname(__file__), 'hostChatServer.py')
    chatInputPath = os.path.join(os.path.dirname(__file__), 'hostChatInput.py')
    open_new_console(chatInputPath)
    open_new_console(chat_path)

def launchClientChat() :
    # launch the input and the client chat
    chat_path = os.path.join(os.path.dirname(__file__), 'chat.py')
    chatInputPath = os.path.join(os.path.dirname(__file__), 'chatInput.py')
    open_new_console(chatInputPath)
    open_new_console(chat_path)

if __name__ == '__main__':
    main()
