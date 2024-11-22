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
        choice = HostSendMessage(player.id, prompt, True)
        while True:
            if choice not in expectedResults:
                HostSendMessage(player.id, "Choix invalide\n", False)
                choice = HostSendMessage(player.id, prompt, True)
            else:
                break
        return choice

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
            HostSendMessage(player.id, message, False)

def ClientSendMessage(server_socket):
    """
    Le client reçoit un message de l'hôte et détermine s'il doit répondre ou non.
    """
    try:
        # Recevoir le message
        data = server_socket.recv(655336).decode('utf-8')
        if not data:
            return  # Si aucune donnée n'est reçue, sortir
        
        # Diviser l'instruction et le message
        parts = data.split("|", 1)
        if len(parts) != 2:
            print(f"Message mal formé : {data}")
            return
        
        instruction, message = parts
        print(message)
        
        # Vérifier si une réponse est attendue
        if instruction == "REPLY":
            response = input("")
            server_socket.sendall(response.encode('utf-8'))
        elif instruction == "NO_REPLY":
            #print("Aucune réponse requise.")
            pass
        else:
            print(f"Instruction inconnue : {instruction}")
    except socket.error as e:
        print(f"Erreur de communication avec l'hôte : {e}")

def HostSendMessage(client_socket, message, expect_reply):
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
    if client_socket is None:
        print(message)
    else:
        try:
            # Déterminer l'instruction à envoyer
            instruction = "REPLY" if expect_reply else "NO_REPLY"
            
            # Préparer le message à envoyer
            full_message = f"{instruction}|{message}"
            client_socket.sendall(full_message.encode('utf-8'))
            
            # Si une réponse est attendue, la recevoir
            if expect_reply:
                response = client_socket.recv(655336).decode('utf-8')
                return response
            
            # Sinon, rien à attendre
            return None
        except socket.error as e:
            print(f"Erreur de communication avec le client : {e}")
            return None

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