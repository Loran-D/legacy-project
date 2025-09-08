from Piece import Piece

class Player:
    def __init__(self, color):

        # Player color
        self.color = color
        # Player starts with 15 pieces
        self.pieces_in_hand = 21
        # Player starts with 0 standing pieces
        self.standing_pieces = 0
        # Amount of flat pieces placed
        self.flat_pieces_placed = 0
        # Turn status       
        self.turn = False         

    #Player places piece
    def place_piece(self, standing: bool) -> bool:
        if self.pieces_in_hand > 0:
            self.pieces_in_hand -= 1
            if standing:
                self.standing_pieces += 1
            else:
                self.flat_pieces_placed += 1
            piece = Piece(self.color,standing=standing)
            return piece
        else:
            print(f"{self.color} player has no pieces left to place")
            return None

    #Toggle the turn
    def toggle_turn(self):
        self.turn = not self.turn

    #Representation of the player
    def __repr__(self):
        return (f"Player(Color={self.color}, pieces_in_hand={self.pieces_in_hand},flat_pieces_placed={self.flat_pieces_placed},"
                f"standing_pieces_placed={self.standing_pieces}, turn={self.turn})")

# Test the Player class
def test_game_scenario(player1, player2, total_moves=32):
    # Initial state
    print(player1)
    print(player2)

    # Black player starts
    player1.toggle_turn()
    print("Black player always starts")
    print(player1)

    # Game loop where the black player only places flat pieces and the white player only places standing pieces 
    # for testing purposes
    for move in range(total_moves):
        if player1.turn:
            print(f"{player1.color} player's turn")
            piece = player1.place_piece(standing=False)
            if piece:
                print(f"{player1.color} player placed a {piece}! {player1.pieces_in_hand} pieces left.")
            else:
                print(f"{player1.color} player cannot place any more pieces.")
            # Toggle turns
            player1.toggle_turn()
            player2.toggle_turn()
        else:
            print(f"{player2.color} player's turn")
            piece = player2.place_piece(standing=True)
            if piece:
                print(f"{player2.color} player placed a {piece}! {player2.pieces_in_hand} pieces left.")
            else:
                print(f"{player2.color} player cannot place any more pieces.")
            # Toggle turns
            player1.toggle_turn()
            player2.toggle_turn()

    # Final state
    print(player1)
    print(player2)


# Run the game scenario
test_game_scenario(Player('black'), Player('white'))
