from enum import Enum
import random
from typing import Dict, List
import math
from Board import Board as OtherBoard
from Player import Player as OtherPlayer

""" How to use the AI?
Step 1: You need file "ai.py" and then import as follows
from ai import converter, AI, Difficulty, Color

Step 2: Create the AI object with parameters like this:
ai = AI(difficulty=ai_difficulty, player=ai_color, grid_rows=board_size, grid_columns=board_size, max_height=stack_max_height)

Step 3: Use the AI
# first, we need to create the input parameter:
ai_game_state = converter(
    other_board, player_black, player_white, current_turn, board_size
)

# Then, call the API:
ai_move = ai.get_best_move(ai_game_state)

# Then, get the AI's decision, there are 2 cases, 1 for place and 1 for move:
if ai_move.is_placement:    # for place
    # the destination is (ai_move.x, ai_move.y), and the piece to be placed is (ai_move.piece)
else:                       # for move
    # from (ai_move.x, ai_move.y) move (ai_move.count) pieces to (ai_move.to_x, ai_move.to_y)
"""


class Color(Enum):
    BLACK = 0
    WHITE = 1


class AIPiece:
    def __init__(self, color: Color, is_vertical: bool) -> None:
        self.color = color
        self.is_vertical = is_vertical


class Winner(Enum):
    BLACK_WIN = 0
    WHITE_WIN = 1
    DRAW = 2
    ONGOING = 3


class Field:
    def __init__(self) -> None:
        self.pieces: List[AIPiece] = []

    def add_piece(self, pieces: List[AIPiece]) -> None:
        self.pieces.extend(pieces)

    def remove_piece(self, count: int = 1) -> List[AIPiece]:
        removed = []
        if count > len(self.pieces):
            count = len(self.pieces)
        for _ in range(count):
            removed.insert(0, self.pieces.pop())
        return removed

    def get_piece(self, count: int = 1) -> List[AIPiece]:
        if count > len(self.pieces):
            return self.pieces.copy()
        return self.pieces[-count:]

    def get_piece_count(self) -> int:
        return len(self.pieces)

    def is_empty(self) -> bool:
        return len(self.pieces) == 0


class AIBoard:
    def __init__(self, size: int = 5) -> None:
        self.size = size
        self.fields: List[List[Field]] = [
            [Field() for _ in range(size)] for _ in range(size)
        ]

    def place_piece(self, x: int, y: int, pieces: List[AIPiece]) -> None:
        if 0 <= x < self.size and 0 <= y < self.size:
            self.fields[x][y].add_piece(pieces)

    def move_piece(
        self, x: int, y: int, new_x: int, new_y: int, count: int = 1
    ) -> List[AIPiece]:
        if (
            0 <= x < self.size
            and 0 <= y < self.size
            and 0 <= new_x < self.size
            and 0 <= new_y < self.size
        ):
            pieces_to_move = self.fields[x][y].remove_piece(count)
            self.fields[new_x][new_y].add_piece(pieces_to_move)
            return pieces_to_move
        return []

    def undo_move_piece(
        self, x: int, y: int, new_x: int, new_y: int, count: int
    ) -> None:
        pieces_to_move_back = self.fields[new_x][new_y].remove_piece(count)
        self.fields[x][y].add_piece(pieces_to_move_back)

    def get_field(self, x: int, y: int) -> Field:
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.fields[x][y]
        return None

    def is_field_full(self, x: int, y: int, max_height: int) -> bool:
        field = self.get_field(x, y)
        return field.get_piece_count() >= max_height if field else False

    def display(self) -> None:
        fixed_width = 6
        print("  ", end="")
        for x in range(self.size):
            print(f"{x:^{fixed_width}}", end="")
        print()

        for y in range(self.size):
            print(f"{y} ", end="")
            for x in range(self.size):
                field = self.fields[x][y]
                if field.get_piece_count() > 0:
                    pieces = field.get_piece(field.get_piece_count())
                    piece_display = "|".join(
                        f"{'B' if piece.color == Color.BLACK else 'W'}{'H' if not piece.is_vertical else 'V'}"
                        for piece in pieces
                    )
                    print(f"{piece_display:^{fixed_width}}", end="")
                else:
                    print(f"{'.':^{fixed_width}}", end="")
            print()

    def check_winner(self, turn: int, max_turn: int) -> Winner:
        black_wins = self.check_full_path(Color.BLACK)
        white_wins = self.check_full_path(Color.WHITE)

        if black_wins and white_wins:
            return Winner.DRAW

        if black_wins:
            return Winner.BLACK_WIN
        if white_wins:
            return Winner.WHITE_WIN
        if turn >= max_turn:
            return self.check_draw()
        if self.is_full():
            return self.check_draw()
        return Winner.ONGOING

    def check_draw(self) -> Winner:
        black_horizontal_count = 0
        white_horizontal_count = 0
        for row in self.fields:
            for field in row:
                if field.get_piece_count() > 0:
                    top_piece = field.get_piece(1)[0]
                    if not top_piece.is_vertical:  # only consider flat piece
                        if top_piece.color == Color.BLACK:
                            black_horizontal_count += 1
                        elif top_piece.color == Color.WHITE:
                            white_horizontal_count += 1

        if black_horizontal_count > white_horizontal_count:
            return Winner.BLACK_WIN
        elif white_horizontal_count > black_horizontal_count:
            return Winner.WHITE_WIN
        else:
            return Winner.DRAW

    def is_full(self) -> bool:
        for row in self.fields:
            for field in row:
                if field.is_empty():
                    return False
        return True

    def dfs(
        self, x: int, y: int, player_color: Color, visited: set, direction: str
    ) -> bool:
        if direction == "horizontal" and y == self.size - 1:  # 水平连接到最后一列
            return True
        if direction == "vertical" and x == self.size - 1:  # 垂直连接到最后一行
            return True

        visited.add((x, y))

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in visited:
                field = self.fields[nx][ny]
                if (
                    field.get_piece_count() > 0
                    and field.get_piece(1)[0].color.value == player_color.value
                    and not field.get_piece(1)[0].is_vertical
                ):
                    if self.dfs(nx, ny, player_color, visited, direction):
                        return True
        return False

    def check_full_path(self, player_color: Color) -> bool:
        # From left to right
        for x in range(self.size):
            if (
                self.fields[x][0].get_piece_count() > 0
                and self.fields[x][0].get_piece(1)[0].color.value == player_color.value
            ):
                if self.dfs(x, 0, player_color, set(), "horizontal"):
                    return True

        # From up to bottom
        for y in range(self.size):
            if (
                self.fields[0][y].get_piece_count() > 0
                and self.fields[0][y].get_piece(1)[0].color.value == player_color.value
            ):
                if self.dfs(0, y, player_color, set(), "vertical"):
                    return True

        return False


class Move:
    def __init__(
        self,
        x: int,
        y: int,
        is_placement: bool,
        to_x: int = -1,
        to_y: int = -1,
        piece: AIPiece = None,
        count: int = 1,
    ) -> None:
        self.x = x
        self.y = y
        self.is_placement = is_placement
        self.to_x = to_x  # ignore this when placing piece
        self.to_y = to_y  # ignore this when placing piece
        self.piece = piece  # ignore this when moving piece
        self.count = count


class Difficulty(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2


depth_mapping: Dict[Difficulty, int] = {
    Difficulty.EASY: 1,
    Difficulty.MEDIUM: 2,
    Difficulty.HARD: 3,
}


class GameState:
    def __init__(
        self,
        board: AIBoard,
        num_black_piece: int,
        num_white_piece: int,
        turn: int = 0,
        max_turn: int = 200,
    ) -> None:
        self.board = board
        self.num_black_piece = num_black_piece  # how many black pieces available
        self.num_white_piece = num_white_piece  # how many white pieces available
        self.turn = turn
        self.max_turn = max_turn

    def apply_move(self, move: Move, player: Color) -> None:
        if move.is_placement:
            self.board.place_piece(move.x, move.y, [move.piece])
            if player == Color.BLACK:
                self.num_black_piece -= 1
            else:
                self.num_white_piece -= 1
        else:
            self.board.move_piece(move.x, move.y, move.to_x, move.to_y, move.count)
        self.turn += 1

    def undo_move(self, move: Move, player: Color) -> None:
        if move.is_placement:
            self.board.fields[move.x][move.y].remove_piece(1)
            if player == Color.BLACK:
                self.num_black_piece += 1
            else:
                self.num_white_piece += 1
        else:
            self.board.undo_move_piece(move.x, move.y, move.to_x, move.to_y, move.count)
        self.turn -= 1


def map_color(color_str: str) -> "Color":
    if color_str.lower() == "black":
        return Color.BLACK
    elif color_str.lower() == "white":
        return Color.WHITE
    else:
        raise ValueError(f"Unknown color: {color_str}")


def converter(
    other_board: OtherBoard,
    player1: OtherPlayer,
    player2: OtherPlayer,
    turn: int,
    max_turn: int = 200,
    board_size: int = 6,
) -> GameState:

    ai_board = AIBoard(size=board_size)

    for y in range(board_size):
        for x in range(board_size):
            stack = other_board.get_stack(x, y)
            if stack and not stack.is_empty():
                ai_pieces = [
                    AIPiece(color=map_color(piece.color), is_vertical=piece.standing)
                    for piece in stack.stack
                ]
                ai_board.fields[x][y].add_piece(ai_pieces)

    num_black_piece = player1.pieces_in_hand
    num_white_piece = player2.pieces_in_hand

    game_state = GameState(
        board=ai_board,
        num_black_piece=num_black_piece,
        num_white_piece=num_white_piece,
        turn=turn,
        max_turn=max_turn,
    )

    return game_state


class AI:
    def __init__(
        self,
        difficulty: Difficulty,
        player: Color,
        grid_rows: int,
        grid_columns: int,
        max_height: int = 5,
    ) -> None:
        self.difficulty = difficulty
        self.player = player
        self.opponent = Color.WHITE if player == Color.BLACK else Color.BLACK
        self.max_depth = depth_mapping.get(self.difficulty)
        self.rows = grid_rows
        self.columns = grid_columns
        self.max_height = max_height  # max stack height for field

    def get_best_move(self, game_state: GameState) -> Move:
        all_moves = self.generate_all_moves(game_state, self.player)
        if self.difficulty == Difficulty.EASY:
            return random.choice(all_moves)
        best_score = -math.inf
        best_move = None
        for move in all_moves:
            game_state.apply_move(move, self.player)
            score = self.minimax(
                game_state,
                self.max_depth - 1,
                False,
                -math.inf,
                math.inf,
                game_state.turn,
                game_state.max_turn,
            )
            game_state.undo_move(move, self.player)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(
        self,
        game_state: GameState,
        depth: int,
        is_maximizing: bool,
        alpha: float,
        beta: float,
        turn: int,
        max_turn: int,
    ) -> float:
        winner = game_state.board.check_winner(turn, max_turn)
        if winner == Winner.BLACK_WIN:
            if self.player == Color.BLACK:
                return 1000
            else:
                return -1000
        elif winner == Winner.WHITE_WIN:
            if self.player == Color.WHITE:
                return 1000
            else:
                return -1000
        elif winner == Winner.DRAW:
            return 0

        if depth == 0:
            return self.evaluate(game_state)

        if is_maximizing:
            max_eval = -math.inf
            for move in self.generate_all_moves(game_state, self.player):
                game_state.apply_move(move, self.player)
                eval = self.minimax(
                    game_state,
                    depth - 1,
                    False,
                    alpha,
                    beta,
                    game_state.turn,
                    game_state.max_turn,
                )
                game_state.undo_move(move, self.player)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in self.generate_all_moves(game_state, self.opponent):
                game_state.apply_move(move, self.opponent)
                eval = self.minimax(
                    game_state,
                    depth - 1,
                    True,
                    alpha,
                    beta,
                    game_state.turn,
                    game_state.max_turn,
                )
                game_state.undo_move(move, self.opponent)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate(self, game_state: GameState) -> float:
        """The number of our flat pieces - number of other player's flat pieces"""
        own_count = self.count_horizontal_pieces(game_state, self.player)
        opp_count = self.count_horizontal_pieces(game_state, self.opponent)
        return own_count - opp_count

    def count_horizontal_pieces(self, game_state: GameState, player: Color) -> int:
        count = 0
        board = game_state.board
        for x in range(board.size):
            for y in range(board.size):
                field = board.get_field(x, y)
                if field and not field.is_empty():
                    top_piece = field.get_piece(1)[0]
                    if not top_piece.is_vertical and top_piece.color == player:
                        count += 1
        return count

    def generate_all_moves(self, game_state: GameState, player: Color) -> List[Move]:
        moves = []
        board = game_state.board

        # Place
        for x in range(self.columns):
            for y in range(self.rows):
                field = board.get_field(x, y)
                if not board.is_field_full(x, y, self.max_height):
                    # cannot place upon vertical
                    if field.is_empty() or (
                        field.get_piece_count() > 0
                        and not field.get_piece(1)[0].is_vertical
                    ):
                        # player still has piece
                        if (
                            player == Color.BLACK and game_state.num_black_piece > 0
                        ) or (player == Color.WHITE and game_state.num_white_piece > 0):
                            # place flat piece
                            piece = AIPiece(player, is_vertical=False)
                            move = Move(x, y, True, piece=piece)
                            moves.append(move)
                            # place vertical piece
                            piece = AIPiece(player, is_vertical=True)
                            move = Move(x, y, True, piece=piece)
                            moves.append(move)

        # Move
        for x in range(self.columns):
            for y in range(self.rows):
                field = board.get_field(x, y)
                if not field.is_empty():
                    top_piece = field.get_piece(1)[0]
                    if top_piece.color.value == player.value:
                        max_movable = field.get_piece_count()
                        for count in range(1, max_movable + 1):
                            for direction in ["up", "down", "left", "right"]:
                                new_x, new_y = self.calculate_new_position(
                                    x, y, direction
                                )
                                if (
                                    self.is_within_bounds(new_x, new_y)
                                    and (
                                        board.get_field(new_x, new_y).get_piece_count()
                                        + count
                                    )
                                    <= self.max_height
                                ):
                                    move = Move(
                                        x, y, False, to_x=new_x, to_y=new_y, count=count
                                    )
                                    moves.append(move)
        return moves

    def calculate_new_position(self, x: int, y: int, direction: str) -> (int, int):
        if direction == "up":
            return x, y - 1
        elif direction == "down":
            return x, y + 1
        elif direction == "left":
            return x - 1, y
        elif direction == "right":
            return x + 1, y
        else:
            return x, y

    def is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.columns and 0 <= y < self.rows
