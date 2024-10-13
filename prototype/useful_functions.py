def PlayerChoice(prompt, expected_results):
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
        if choice not in expected_results:
            print("Choix invalide\n")
            choice = int(input(prompt))
        else:
            break
    return choice