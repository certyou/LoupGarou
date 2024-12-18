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
    gamePath = os.path.join(os.path.dirname(__file__), 'main_reseau.py')
    open_new_console(gamePath)  # open the game in a new console


def launchHostChat() :
    # launch the input and the server chat of the host
    chatPath = os.path.join(os.path.dirname(__file__), 'chat/hostChatServer.py') 
    chatInputPath = os.path.join(os.path.dirname(__file__), 'chat/hostChatInput.py')
    open_new_console(chatInputPath)
    open_new_console(chatPath)

def launchClientChat() :
    # launch the input and the client chat
    chatPath = os.path.join(os.path.dirname(__file__), 'chat/chat.py')
    chatInputPath = os.path.join(os.path.dirname(__file__), 'chat/chatInput.py')
    open_new_console(chatInputPath)
    open_new_console(chatPath)

if __name__ == '__main__':
    main()
