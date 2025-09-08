from ai import converter, AI, Difficulty, Color
from Board import Board as OtherBoard
from Player import Player as OtherPlayer
from Piece import Piece
from Stack import Stack


def setup_test_game():
    other_board = OtherBoard()

    player_black = OtherPlayer("black")
    player_white = OtherPlayer("white")

    stack = Stack()
    stack.push(Piece("white", standing=False))
    other_board.place_piece(4, 1, stack)

    current_turn = 10

    return other_board, player_black, player_white, current_turn


board_size = 6
other_board, player_black, player_white, current_turn = setup_test_game()
ai_game_state = converter(
    other_board, player_black, player_white, current_turn, board_size
)
ai = AI(
    difficulty=Difficulty.EASY,
    player=Color.BLACK,
    grid_rows=6,
    grid_columns=6,
    max_height=5,
)
ai_move = ai.get_best_move(ai_game_state)
if ai_move.is_placement:
    move_type = "place"
    piece_type = "vertical" if ai_move.piece.is_vertical else "flat"
    print(
        f"AI choose {move_type} piece to ({ai_move.x}, {ai_move.y}), Type: {piece_type}"
    )
else:
    move_type = "move"
    print(
        f"AI choose {move_type} piece from ({ai_move.x}, {ai_move.y}) to ({ai_move.to_x}, {ai_move.to_y}), Count:{ai_move.count}"
    )
    