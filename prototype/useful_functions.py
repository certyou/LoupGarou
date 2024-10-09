def playerChoice(prompt, expectedResults):
    """
    Function to ask the player to make a choice among a list of expected results
    Arg :
        - :prompt: str, the question to ask the player
        - :expected_results: list, the list of expected results
    Out : 
        - :choice: int, player's choice
    """
    choice = int(input(prompt))
    while True:
        if choice not in expectedResults:
            print("Choix invalide")
            choice = int(input(prompt))
        else:
            break
    return int(choice)