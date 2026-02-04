# game_logic.py

class Game:
    def __init__(self):
        self.score = 0
        self.is_over = False

    def play_turn(self, player_choice):
        # Implement game logic here
        pass

    def evaluate(self):
        # Implement evaluation logic here
        return self.score

    def end_game(self):
        self.is_over = True
        print('Game Over! Your score is:', self.score)

# Example of usage
if __name__ == '__main__':
    game = Game()
    # Add game loop and logic here.