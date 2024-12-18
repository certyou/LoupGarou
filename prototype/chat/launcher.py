import subprocess
import sys
import os


# Function to launch a Python script in a new console
def openNewConsole(scriptName):
    try:
        # Use 'start' to open a new console on Windows
        subprocess.Popen(['start', 'cmd', '/K', sys.executable, scriptName], shell=True)
    except Exception as e:
        print(f"Erreur lors de l'ouverture de la console pour {scriptName}: {e}")


def main() :
    # launch the game
    gamePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'main_reseau.py')
    openNewConsole(gamePath)  # open the game in a new console


def launchHostChat() :
    # launch the input and the server chat of the host
    gamePath = os.path.join(os.path.dirname(__file__), 'hostChatServer.py') 
    chatInputPath = os.path.join(os.path.dirname(__file__), 'hostChatInput.py')
    openNewConsole(chatInputPath)
    openNewConsole(gamePath)

def launchClientChat() :
    # launch the input and the client chat
    gamePath = os.path.join(os.path.dirname(__file__), 'chat.py')
    chatInputPath = os.path.join(os.path.dirname(__file__), 'chatInput.py')
    openNewConsole(chatInputPath)
    openNewConsole(gamePath)

if __name__ == '__main__':
    main()
