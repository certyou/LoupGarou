from random import choice

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
    this function ask any player for a choice from expected results (in local or not)
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
                SendMessage(player, "Choix invalide")
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
        this function decode the response of the remote player
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
        This function ask the target remote player
        """
        host_request = socket.recv(65536).decode()
        if response:
            socket.sendall(input(host_request).encode())
        else:
            print(host_request, end="")

def SendMessage(player, message):
    """
    Arg :
        - :socket: socket, socket use to send the message
        - :message: str, message to display
    Out :
        /
    This function display a message to traget player
    """
    if player.IsHost:
        print(message, end="")
    else:
        player.id.sendall(message.encode())

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
     """
     Arg:
        - :message: str, message to display
        - :players: list of object, list of players to send message
    Out:
        /
    This function take a message and send it to all players
     """
     for player in players:
        if player.IsHost:
            print(message, end="")
        else:
            player.id.sendall(message.encode())

def playerWithMostVote(tabPlayer, listOfPlayers):
    """
    Arg :
        - :tabPlayer: lst of Player object
    Out : 
        - :maxVotePlayer: Player object, player with the most vote or random player if draw
    """
    broadcastMessage("\nVoici les votes qui ont eu lieu: ", listOfPlayers)
    maxVote = -1
    for player in tabPlayer:
        broadcastMessage(f"{player.name} --> {player.vote}\n", listOfPlayers)
        if player.vote > maxVote:
            maxVote = player.vote
            maxVotePlayer = player
        elif player.vote == maxVote:
            temp = [player, maxVotePlayer]
            maxVotePlayer = choice(temp)
        player.resetVote()
    return maxVotePlayer

def PrintPlayerInLife(tabPlayerInLife):
        message = f"Joueurs en vie:\n"
        for x in range(len(tabPlayerInLife)):
            message += f"    {x+1} - {tabPlayerInLife[x].name}\n"
        return message   