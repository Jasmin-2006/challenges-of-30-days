
import random

class Token:
    def __init__(self, token_id, color):
        self.id = token_id
        self.color = color
        self.position = -1  # -1 means in the yard (home base)
        self.is_home = False

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.tokens = [Token(i + 1, color) for i in range(4)]

    def has_won(self):
        return all(token.is_home for token in self.tokens)

class LudoGame:
    BOARD_LIMIT = 57  # Steps required to reach the final home coordinate

    def __init__(self, player_info):
        # player_info is a list of tuples: (name, color)
        self.players = [Player(name, color) for name, color in player_info]
        self.current_turn = 0

    def roll_die(self):
        return random.randint(1, 6)

    def display_status(self):
        print("\n--- CURRENT BOARD STATUS ---")
        for player in self.players:
            token_status = []
            for t in player.tokens:
                if t.is_home:
                    status = "Finished"
                elif t.position == -1:
                    status = "Yard"
                else:
                    status = f"Step {t.position}"
                token_status.append(f"T{t.id}({status})")
            print(f"{player.name} ({player.color}): {', '.join(token_status)}")
        print("----------------------------\n")

    def handle_knockout(self, moving_player, target_position):
        """Simulates sending an opponent's token back to the yard if landed on."""
        for player in self.players:
            if player == moving_player:
                continue
            for token in player.tokens:
                # Basic global position alignment estimation
                if token.position == target_position and token.position > 0:
                    print(f"💥 BOOM! {moving_player.name} knocked out {player.name}'s Token {token.id}!")
                    token.position = -1

    def play_turn(self):
        player = self.players[self.current_turn]
        print(f"\n📢 It's {player.name}'s ({player.color}) turn.")
        input("Press Enter to roll the die... ")
        
        die = self.roll_die()
        print(f"🎲 {player.name} rolled a {die}!")

        # Filter actionable choices
        movable_tokens = []
        for token in player.tokens:
            if token.is_home:
                continue
            if token.position == -1 and die == 6:
                movable_tokens.append(token)
            elif token.position >= 0 and (token.position + die) <= self.BOARD_LIMIT:
                movable_tokens.append(token)

        if not movable_tokens:
            print("❌ No valid moves possible with this roll.")
            self.current_turn = (self.current_turn + 1) % len(self.players)
            return

        # Prompt player choice
        print("Available moves:")
        for idx, token in enumerate(movable_tokens):
            loc = "Yard" if token.position == -1 else f"Step {token.position}"
            print(f"[{idx}] Move Token {token.id} (Currently at {loc})")

        while True:
            try:
                choice = int(input(f"Select token index (0-{len(movable_tokens)-1}): "))
                if 0 <= choice < len(movable_tokens):
                    selected_token = movable_tokens[choice]
                    break
                print("Invalid index selection.")
            except ValueError:
                print("Please enter a valid numeric value.")

        # Update board mechanics
        if selected_token.position == -1:
            selected_token.position = 0
            print(f"🚀 Token {selected_token.id} entered the track!")
        else:
            selected_token.position += die
            print(f"🏃 Token {selected_token.id} advanced to step {selected_token.position}.")
            if selected_token.position == self.BOARD_LIMIT:
                selected_token.is_home = True
                print(f"🎉 Token {selected_token.id} reached Home safely!")

        # Execute landing mechanics
        self.handle_knockout(player, selected_token.position)

        # Game rules: Getting a 6 grants an extra turn
        if die == 6:
            print("🎁 Rolled a 6! You earn an extra turn.")
        else:
            self.current_turn = (self.current_turn + 1) % len(self.players)

    def start_game(self):
        print("================================")
        print("   WELCOME TO PYTHON LUDO CORE  ")
        print("================================")
        
        while True:
            self.display_status()
            self.play_turn()
            
            # Check win criteria
            for player in self.players:
                if player.has_won():
                    print(f"\n🏆👑🏆 GAME OVER! {player.name} WINS THE GAME! 🏆👑🏆")
                    return

if __name__ == "__main__":
    # Setup for a quick 2-player configuration (supports up to 4)
    setup = [
        ("Alice", "Red"),
        ("Bob", "Green")
    ]
    
    game = LudoGame(setup)
    game.start_game()
