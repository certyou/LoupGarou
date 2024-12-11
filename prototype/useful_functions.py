from random import choice
import socket
import time
from chat.chatInput import textModifier


def playerChoice(prompt, expectedResults, local=True, player=None):
    """ this function ask any player for a choice from expected results (in local or not)
    Arg :
        - :prompt: str, the question to ask the player
        - :expectedResults: list, the list of expected results
        - :local: if the player is the host or not
        - :player: the player to ask if player is not the host 
    Out : 
        - :choice: int, player's choice
    """
    if local:
        # request the host for a choice
        choice = input(prompt)
        while True: # check if the choice is valid
            if choice not in expectedResults:
                print("Choix invalide", end="")
                choice = input(prompt)
            else:
                break
    else:
        # request the player for a choice
        choice = HostSendMessage(player.id, prompt, True)
        while True: # check if the choice is valid
            if choice not in expectedResults:
                HostSendMessage(player.id, "Choix invalide\n", False)
                choice = HostSendMessage(player.id, prompt, True)
            else:
                break
    return choice


def broadcastMessage(message, players):
    """ This function take a message and send it to all players
    Arg:
        - :message: str, message to display
        - :players: list of object, list of players to send message
    Out:
        /
    """
    for player in players:
        if player.IsHost: # if the player is the host, print it
            print(message, end="")
        else: # else send it to all players
            HostSendMessage(player.id, message, False)


def ClientSendMessage(server_socket):
    """ The client receive a message from the host and determine if a respond is needed
    Arg:
        - :server_socket: socket, socket of the host
    Out:
        /
    """
    try:
        # receive the message from the host
        data = server_socket.recv(655336).decode('utf-8')
        if not data:
            return None # if no message receive, return None
        
        # split the instruction and the message
        parts = data.split("/")
        if len(parts) != 2: # check if the message is well formated
            print(f"Message mal formé : {parts}")
            return
        
        # get the instruction and the message
        instruction, message = parts
        
        # if the message is a role, write the permission in a file
        if instruction == "NO_REPLY" and message == "⌈⌈loup" :
            textModifier("role.txt", "w", "1")
        if instruction == "NO_REPLY" and message == "⌈⌈fille" :
            textModifier("role.txt", "w", "2")
        # check if a response is needed
        elif instruction == "REPLY":
            print(message, end="")
            response = input("")
            server_socket.sendall(response.encode('utf-8'))
        elif instruction == "NO_REPLY":
            print(message, end="")
        elif instruction == "END_GAME":
            print(message, end="")
            exit()
        else: # if the instruction is unknown
            print(f"Instruction inconnue : {instruction}")

    except socket.error as e:
        print(f"Erreur de communication avec l'hôte : {e}")


def HostSendMessage(client_socket, message, expect_reply=True):
    """ The host send a message to the client, with or without a response expected
    Arg:
        - :client_socket: socket, client socket to send the message to.
        - :message: str, message to send.
        - :expect_reply: boolean, True if a response is needed, False else.
    Out:
        - :response: str, return the response if response was needed
        - None, else
    """
    time.sleep(0.5) # wait for the client to be ready
    if client_socket is None: # if the client is the host, print the message
        print(message, end="")
    else:
        try:
            # determine the instruction to send
            instruction = "REPLY" if expect_reply else "NO_REPLY"
            
            # prepare the message to send
            full_message = f"{instruction}/{message}"
            client_socket.sendall(full_message.encode('utf-8'))
            
            # if a response is needed, receive it
            if expect_reply:
                response = client_socket.recv(655336).decode('utf-8')
                return response
            # else, nothing to wait for
            return None
        except socket.error as e: # if an error occured
            print(f"Erreur de communication avec le client : {e}")
            return None


def playerWithMostVote(tabPlayer, listOfPlayers):
    """ return the player with the most vote from a list of players
    Arg :
        - :tabPlayer: lst of Player object, list of all players participating at the vote
        - :listOfPlayers: lst of Player object, list of all players
    Out : 
        - :maxVotePlayer: Player object, player with the most vote or random player if draw
    """
    broadcastMessage("\nVoici les votes qui ont eu lieu: \n", listOfPlayers)
    maxVote = -1
    for player in tabPlayer:
        # display the votes
        broadcastMessage(f"{player.name} --> {player.vote}\n", listOfPlayers)
        if player.vote > maxVote:
            maxVote = player.vote
            maxVotePlayer = player
        elif player.vote == maxVote:
            temp = [player, maxVotePlayer]
            maxVotePlayer = choice(temp) # if draw, choose randomly with random.choice
        player.resetVote() # reset the vote for the next round
    return maxVotePlayer


def PrintPlayerInLife(tabPlayerInLife):
        """ return a str with all the player in life with a number associate with their name
        Arg :
            - :tabPlayerInLife: lst of Player object, list of all players in life
        Out :
            - :message: str, list of all player in life with a number associate with their name
        """
        message = f"Voici les différents joueurs en vie:\n"
        for x in range(len(tabPlayerInLife)):
            message += f"    {x+1} - {tabPlayerInLife[x].name}\n"
        return message   
