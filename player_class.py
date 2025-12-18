"""
Player Class Module
Defines the Player class with attributes and methods for tracking player statistics
"""

class Player:
    """
    Player class to store player information and statistics
    """
    def __init__(self, name, score=0):
        """
        Initialize a Player object
        """
        self.name = name
        self.score = score
        self.games_played = 1
        self.best_score = score
        self.score_history = [score]
        self.current_streak = 0
    
    def update_score(self, new_score):
        """
        Update player's score and statistics
        """
        self.score = new_score
        self.games_played += 1
        self.score_history.append(new_score)
        
        # Update best score
        if new_score > self.best_score:
            self.best_score = new_score
            self.current_streak += 1
        else:
            self.current_streak = 0
    
    def get_average_score(self):
        """
        Calculate average score across all games
        """
        if len(self.score_history) == 0:
            return 0
        return sum(self.score_history) / len(self.score_history)
    
    def __str__(self):
        """
        String representation of Player
        """
        return f"{self.name}: {self.score} points"
    
    def __repr__(self):
        """
        Official representation of Player
        """
        return f"Player('{self.name}', {self.score})"