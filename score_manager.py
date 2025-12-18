"""
Score Manager Module
Contains ScoreValidator and Leaderboard classes for managing game scores
"""

import os
from datetime import datetime
from player_class import Player

def leaderboard_header(func):
    """
    Decorator to add a formatted header to leaderboard display
    """
    def wrapper(*args, **kwargs):
        print("\n" + "="*60)
        print( " VIDEO GAME LEADERBOARD ".center(56) )
        print("="*60)
        result = func(*args, **kwargs)
        print("="*60 + "\n")
        return result
    return wrapper


class ScoreValidator:
    """
    Class to validate game scores
    """
    @staticmethod
    def validate_score(score):
        """
        Validate if a score is valid
        """
        try:
            score = int(score)
            if score < 0:
                print(" Error: Score cannot be negative!")
                return False
            if score > 10000:
                print(" Error: Score too high! Maximum is 10000")
                return False
            return True
        except ValueError:
            print(" Error: Score must be a number!")
            return False
    
    @staticmethod
    def validate_name(name):
        """
        Validate if a player name is valid
        
        Args:
            name (str): Name to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not name or len(name.strip()) == 0:
            print(" Error: Name cannot be empty!")
            return False
        if len(name) > 20:
            print(" Error: Name too long! Maximum 20 characters")
            return False
        return True


class Leaderboard:
    """
    Class to manage the game leaderboard
    """
    def __init__(self):
        """Initialize the Leaderboard"""
        self.players = {}  # Dictionary: {name: Player object}
        self.filename = "leaderboard.txt"
        self.load_leaderboard()
    
    def add_score(self, name, score):
        """
        Add a new score to the leaderboard
        
        Args:
            name (str): Player name
            score (int): Player score
            
        Returns:
            bool: True if added successfully
        """
        # Validate inputs
        if not ScoreValidator.validate_name(name):
            return False
        if not ScoreValidator.validate_score(score):
            return False
        
        score = int(score)
        
        # Check if player exists
        if name in self.players:
            print(f"  Player '{name}' already exists. Updating score...")
            self.players[name].update_score(score)
        else:
            # Create new player
            self.players[name] = Player(name, score)
            print(f" New player '{name}' added with score {score}!")
        
        self.save_leaderboard()
        return True
    
    def get_top_players(self, n=5):
        """
        Get top N players sorted by score
        
        Args:
            n (int): Number of top players to return (default: 5)
            
        Returns:
            list: List of Player objects sorted by score
        """
        # Using lambda for sorting (descending order)
        sorted_players = sorted(
            self.players.values(), 
            key=lambda player: player.score, 
            reverse=True
        )
        return sorted_players[:n]
    
    @leaderboard_header
    def display_leaderboard(self):
        """
        Display the top 5 players in the leaderboard
        Uses decorator for header formatting
        """
        top_players = self.get_top_players(5)
        
        if not top_players:
            print("No players yet. Add some scores to get started!")
            return
        
        print(f"{'Rank':<6} {'Player Name':<20} {'Score':<10} {'Gap':<10}")
        print("-" * 60)
        
        prev_score = None
        for rank, player in enumerate(top_players, 1):
            # Calculate score gap from previous rank
            if prev_score is None:
                gap = "-"
            else:
                gap = prev_score - player.score
            
            print(f"{rank:<6} {player.name:<20} {player.score:<10} {gap:<10}")
            prev_score = player.score
    
    def save_leaderboard(self):
        """
        Save leaderboard to file
        """
        try:
            with open(self.filename, 'w') as f:
                f.write(f"Leaderboard - Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n")
                
                for player in self.get_top_players(10):
                    f.write(f"{player.name}|{player.score}|{player.games_played}|")
                    f.write(f"{player.best_score}|{','.join(map(str, player.score_history))}\n")
            
            print(f" Leaderboard saved to {self.filename}")
        except Exception as e:
            print(f" Error saving leaderboard: {e}")
    
    def load_leaderboard(self):
        """
        Load leaderboard from file
        """
        if not os.path.exists(self.filename):
            print(f"  No existing leaderboard found. Starting fresh!")
            return
        
        try:
            with open(self.filename, 'r') as f:
                lines = f.readlines()[2:]  # Skip header lines
                
                for line in lines:
                    if line.strip():
                        parts = line.strip().split('|')
                        name = parts[0]
                        score = int(parts[1])
                        games_played = int(parts[2])
                        best_score = int(parts[3])
                        score_history = list(map(int, parts[4].split(',')))
                        
                        # Create player with loaded data
                        player = Player(name, score)
                        player.games_played = games_played
                        player.best_score = best_score
                        player.score_history = score_history
                        
                        self.players[name] = player
            
            print(f" Leaderboard loaded from {self.filename}")
        except Exception as e:
            print(f" Error loading leaderboard: {e}")
    
    def get_player_stats(self, name):
        """
        Get detailed statistics for a player
        
        """
        if name not in self.players:
            print(f" Player '{name}' not found!")
            return None
        
        player = self.players[name]
        return {
            'name': player.name,
            'current_score': player.score,
            'best_score': player.best_score,
            'games_played': player.games_played,
            'average_score': player.get_average_score(),
            'current_streak': player.current_streak,
            'score_history': player.score_history
        }
    