def PlayerChoice(prompt, expected_results):
    """
    Function to ask the player to make a choice among a list of expected results
    Arg :
        - :prompt: str, the question to ask the player
        - :expected_results: list, the list of expected results
    Out : 
        - :choice: int, player's choice
    """
    choice = input(prompt)
    while True:
        if choice not in expected_results:
            print("Choix invalide")
            choice = input(prompt)
        else:
            break
    return int(choice)

def SendMessage(socket, message, expected_results=None):
    """
    Arg :
        - :socket: socket, socket use to send the message
        - :message: str, the message displayed to the remote player
        - :expected_results: list, the list of expected results
    Out : 
        - :choice: int, player's choice
    """
    socket.sendall(message.encode())
    if expected_results is not None:
        pass
    else:
        player_response = socket.recv(1024).decode()
    return player_response