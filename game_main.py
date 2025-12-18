"""
Game Main Module
Main program to run the Video Game Scoring System
"""

import pandas as pd
from score_manager import Leaderboard, ScoreValidator
from player_class import Player


class GameSession:
    """
    Class to manage a game session
    """
    def __init__(self):
        """Initialize game session"""
        self.leaderboard = Leaderboard()
        self.running = True
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "╔" + "="*58 + "╗")
        print("║" + " VIDEO GAME SCORING SYSTEM ".center(58) + "║")
        print("╚" + "="*58 + "╝")
        print("\n1. Add New Score")
        print("2. View Leaderboard")
        print("3. View Player Statistics")
        print("4. View Data Analysis (Pandas)")
        print("5. Add Sample Data")
        print("6. Exit")
        print("-" * 60)
    
    def add_sample_data(self):
        """Add sample players for demonstration"""
        sample_players = [
            ("Alice", 8500),
            ("Bob", 7200),
            ("Charlie", 9100),
            ("Diana", 6800),
            ("Eve", 8900),
            ("Frank", 7500),
            ("Grace", 8200),
            ("Henry", 6500)
        ]
        
        print("\n Adding sample data...")
        for name, score in sample_players:
            self.leaderboard.add_score(name, score)
        
        print("\n Sample data added successfully!")
    
    def view_pandas_analysis(self):
        """Display data analysis using Pandas"""
        if not self.leaderboard.players:
            print("\n No data available for analysis!")
            return
        
        # Prepare data for DataFrame
        data = []
        for player in self.leaderboard.players.values():
            data.append({
                'Player Name': player.name,
                'Current Score': player.score,
                'Best Score': player.best_score,
                'Games Played': player.games_played,
                'Average Score': round(player.get_average_score(), 2)
            })
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Sort by Current Score (descending)
        df = df.sort_values('Current Score', ascending=False).reset_index(drop=True)
        df.index += 1  # Start index from 1
        df.index.name = 'Rank'
        
        print("\n" + "="*80)
        print(" DATA ANALYSIS WITH PANDAS ".center(80))
        print("="*80)
        print("\n COMPLETE PLAYER RANKINGS:")
        print(df.to_string())
        
        # Statistical Summary
        print("\n" + "="*80)
        print(" STATISTICAL SUMMARY:")
        print("-" * 80)
        print(f"Total Players: {len(df)}")
        print(f"Average Score: {df['Current Score'].mean():.2f}")
        print(f"Highest Score: {df['Current Score'].max()}")
        print(f"Lowest Score: {df['Current Score'].min()}")
        print(f"Score Range: {df['Current Score'].max() - df['Current Score'].min()}")
        print(f"Median Score: {df['Current Score'].median():.2f}")
        print("="*80 + "\n")
    
    def run(self):
        """Main game loop"""
        print("\n Welcome to the Video Game Scoring System! ")
        
        while self.running:
            self.show_menu()
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                # Add new score
                print("\n ADD NEW SCORE")
                print("-" * 60)
                name = input("Enter player name: ").strip()
                score = input("Enter score: ").strip()
                self.leaderboard.add_score(name, score)
            
            elif choice == '2':
                # View leaderboard
                self.leaderboard.display_leaderboard()
            
            elif choice == '3':
                # View player statistics
                print("\n PLAYER STATISTICS")
                print("-" * 60)
                name = input("Enter player name: ").strip()
                stats = self.leaderboard.get_player_stats(name)
                
                if stats:
                    print(f"\n{'='*60}")
                    print(f"Player: {stats['name']}")
                    print(f"{'='*60}")
                    print(f"Current Score: {stats['current_score']}")
                    print(f"Best Score: {stats['best_score']}")
                    print(f"Games Played: {stats['games_played']}")
                    print(f"Average Score: {stats['average_score']:.2f}")
                    print(f"Current Streak: {stats['current_streak']}")
                    print(f"Score History: {stats['score_history']}")
                    print(f"{'='*60}\n")
            
            elif choice == '4':
                # View Pandas analysis
                self.view_pandas_analysis()
            
            elif choice == '5':
                # Add sample data
                self.add_sample_data()
            
            elif choice == '6':
                # Exit
                print("\n Thank you for using the Video Game Scoring System!")
                print(" All data has been saved. Goodbye! \n")
                self.running = False
            
            else:
                print("\n Invalid choice! Please enter 1-6.")


def main():
    """
    Main function to start the game
    """
    game = GameSession()
    game.run()


if __name__ == "__main__":
    main()
    