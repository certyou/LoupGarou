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