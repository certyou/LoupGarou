from random import choice
import socket

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
            player_response = socket.recv(1024).decode()
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
        host_request = socket.recv(1024).decode()
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

def client_receive_and_process(server_socket):
    """
    Le client reçoit un message de l'hôte et détermine s'il doit répondre ou non.
    """
    try:
        # Recevoir le message
        data = server_socket.recv(1024).decode('utf-8')
        if not data:
            return  # Si aucune donnée n'est reçue, sortir
        
        # Diviser l'instruction et le message
        parts = data.split("|", 1)
        if len(parts) != 2:
            print(f"Message mal formé : {data}")
            return
        
        instruction, message = parts
        print(f"Message reçu : {message}")
        
        # Vérifier si une réponse est attendue
        if instruction == "REPLY":
            response = input("Votre réponse : ")
            server_socket.sendall(response.encode('utf-8'))
        elif instruction == "NO_REPLY":
            print("Aucune réponse requise.")
        else:
            print(f"Instruction inconnue : {instruction}")
    except socket.error as e:
        print(f"Erreur de communication avec l'hôte : {e}")

def host_send_message(client_socket, message, expect_reply):
    """
    L'hôte envoie un message au client, avec ou sans attente de réponse.
    
    Arguments :
    - client_socket : socket du client.
    - message : le message à envoyer.
    - expect_reply : booléen, True si une réponse est attendue, False sinon.
    
    Retourne :
    - La réponse du client si une réponse est attendue.
    - None si aucune réponse n'est attendue ou en cas d'erreur.
    """
    try:
        # Déterminer l'instruction à envoyer
        instruction = "REPLY" if expect_reply else "NO_REPLY"
        
        # Préparer le message à envoyer
        full_message = f"{instruction}|{message}"
        client_socket.sendall(full_message.encode('utf-8'))
        
        # Si une réponse est attendue, la recevoir
        if expect_reply:
            response = client_socket.recv(1024).decode('utf-8')
            return response
        
        # Sinon, rien à attendre
        return None
    except socket.error as e:
        print(f"Erreur de communication avec le client : {e}")
        return None
