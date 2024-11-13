def playerChoice(prompt, expectedResults, local=True, player=None):
    """
    Function to ask the player to make a choice among a list of expected results
    Arg :
        - :prompt: str, the question to ask the player
        - :expectedResults: list, the list of expected results
        - :local: if the player is the host or not
        - :player: the player to ask if player is not the host 
    Out : 
        - :choice: int, player's choice
    """
    if local:
        choice = input(prompt)
        while True:
            if choice not in expectedResults:
                print("Choix invalide", end="")
                choice = input(prompt)
            else:
                break
        return choice
    else:
        choice = SendRequest(player.id, prompt)
        while True:
            if choice not in expectedResults:
                print("Choix invalide", end="")
                choice = SendRequest(player.id, True)
            else:
                break
        return choice
    
def SendRequest(socket, message, response=True):
        """
        Arg :
            - :socket: socket, socket use to send the message
            - :message: str, the message displayed to the remote player
        Out : 
            - :player_response: str, player's response
        """
        socket.sendall(message.encode())
        if response:
            player_response = socket.recv(65536).decode()
            return player_response

def SendResponse(socket, response=True):
        """
        Arg :
            - :socket: socket, socket use to send the message
            - :response: bool, if the player must respond or not
        Out : 
            /
        """
        host_request = socket.recv(65536).decode()
        if response:
            socket.sendall(input(host_request).encode())

def buffer(message) :
    """
    Function that identify the first frame of information inside the message
    1 frame has to be like this : {type_of_return$str_message}
    Arg : 
        - : message : str, the message to analyze
    Out :
        - : strMessage : str, message that will be prompted to the player console
        - : typeOfReturn : str, type of return the player has to give
        - : message : str, message without the first frame"""
    
    typeOfReturn = message[message.find("{")+1: message.find("$")]
    strMessage = message[message.find("$")+1: message.find("}")]
    message = message[message.find("}")+1:]

    return typeOfReturn, strMessage, message

def broadcastMessage(message, players):
     for player in players:
        if player.IsHost:
            print(message, end="")
        else:
            player.id.sendall(message.encode())