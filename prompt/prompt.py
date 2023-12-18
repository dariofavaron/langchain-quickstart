
class Prompts:
    """
    A class to store all prompts for the game.

    
    """
    def __init__(self):
        self.first_prompt = {"prompt": "Enter your name:"}

    def update_prompt(self, new_prompt):
        self.first_prompt = new_prompt
