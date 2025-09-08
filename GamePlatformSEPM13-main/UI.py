import pygame
import sys
from Board import Board
from Piece import Piece
from Player import Player
from ai import converter, AI, Difficulty, Color

pygame.init()

SCREEN_SIZE = 750  
SCREEN_HEIGHT = 690
SCREEN_WIDTH = 1100
BOARD_SCREEN_SIZE = 450  
BOARD_SIZE = 6  
TOTAL_MOVES = 0
MAX_MOVES = 200  
CELL_SIZE = BOARD_SCREEN_SIZE // BOARD_SIZE  
LINE_WIDTH = 2  
DIFFICULTY = Difficulty.MEDIUM
TILE_HEIGHT = (CELL_SIZE // 5) - (LINE_WIDTH)  
WHITE = (255, 255, 255)  
GRAY = (200, 200, 200)  
BLACK = (0, 0, 0)  
BORDER_RADIUS = 4  
OFFSET = (SCREEN_SIZE - BOARD_SCREEN_SIZE) // 2  
RED = (255, 0, 0)  
BLUE = (0, 0, 255)  



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('UU Game Group 13')

board = Board()

# Init players
player1 = Player('black')
player2 = Player('white')
player1.toggle_turn()  # Black player starts

selected_row = -1
selected_col = -1
selected_pieces_to_move = 0  # Variable to store the number of pieces to move
error_message = ""  # Global variable to hold error messages

def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Draw cells and cell borders
            rect_border = pygame.Rect(col * CELL_SIZE + OFFSET, OFFSET + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            rect = pygame.Rect(col * CELL_SIZE + OFFSET + LINE_WIDTH, OFFSET + row * CELL_SIZE + LINE_WIDTH, CELL_SIZE - LINE_WIDTH, CELL_SIZE - LINE_WIDTH)
            
            pygame.draw.rect(screen, BLACK, rect_border)
            pygame.draw.rect(screen, GRAY, rect)
            
            # Draw highlighted blue border if cell is selected
            if row == selected_row and col == selected_col:
                pygame.draw.rect(screen, BLUE, rect_border, LINE_WIDTH)
            
            stack = board.get_stack(col, row)
            for i, piece in enumerate(stack.stack):
                stack_piece = pygame.Rect(
                    OFFSET + col * CELL_SIZE + 10,
                    OFFSET + row * CELL_SIZE + CELL_SIZE - (TILE_HEIGHT * (i + 1)) - LINE_WIDTH,
                    CELL_SIZE - 20,
                    TILE_HEIGHT
                )
                standing_piece = pygame.Rect(
                        OFFSET + col * CELL_SIZE + 40,
                        OFFSET + row * CELL_SIZE + CELL_SIZE - (TILE_HEIGHT * (i + 1)) - LINE_WIDTH,
                        CELL_SIZE - 80,
                        TILE_HEIGHT
                    )
                color = WHITE if piece.color == 'white' else BLACK
                # Draw either standing or flat piece
                if piece.standing:
                    pygame.draw.rect(screen, color, standing_piece, border_radius=BORDER_RADIUS)
                else:
                    pygame.draw.rect(screen, color, stack_piece, border_radius=BORDER_RADIUS)
                

def draw_game_info():
    font = pygame.font.Font(None, 24)
    
    if(DIFFICULTY == Difficulty.EASY):
        diff = "Easy"
    elif(DIFFICULTY == Difficulty.MEDIUM):
        diff = "Medium"
    else:
        diff = "Hard"
    player1_text = font.render(f"Black: {player1.pieces_in_hand} in hand", True, BLACK)
    player2_text = font.render(f"White: {player2.pieces_in_hand} in hand", True, BLACK)
    current_player_text = font.render(f"Current Turn: {'Black' if player1.turn else 'White'}", True, BLUE)
    ai_difficulty_text = font.render(f"AI Difficulty: {diff}", True, BLACK)
  
    ai_text_width = ai_difficulty_text.get_width()
    screen.blit(player1_text, (10, 10))
    screen.blit(player2_text, (10, 40))
    screen.blit(current_player_text, (SCREEN_WIDTH - 200, 10))
    screen.blit(ai_difficulty_text, ((SCREEN_WIDTH - ai_text_width) // 2, 20))


def draw_invalid_move_info():
    if error_message:
        font = pygame.font.Font(None, 24)
        invalid_move = font.render(error_message, True, RED)
        screen.blit(invalid_move, (10, SCREEN_HEIGHT - 60))  # Adjust position as needed

def draw_commands_info():
    font = pygame.font.Font(None, 20)  # Same size as rules text
    header_font = pygame.font.Font(None, 28)  # Same size as rules header

    header = header_font.render("Commands:", True, BLACK)
    command1 = font.render("1. Click on a cell to select piece(s) (press 1-5) or place a new one", True, BLACK)
    command2 = font.render("2. Click on another cell to move the selected piece(s)", True, BLACK)
    command3 = font.render("3. Hold Shift to place a standing piece", True, BLACK)
    command4 = font.render("4. Hold Ctrl to stack a new piece on a stack", True, BLACK)
    SCREEN_HEIGHT = 690
    # Positioning commands even higher up
    screen.blit(header, (650, SCREEN_HEIGHT - 440))  # Position header higher up
    screen.blit(command1, (650, SCREEN_HEIGHT - 415))  # First command
    screen.blit(command2, (650, SCREEN_HEIGHT - 390))  # Second command
    screen.blit(command3, (650, SCREEN_HEIGHT - 365))  # Third command
    screen.blit(command4, (650, SCREEN_HEIGHT - 340))  # Fourth command

def draw_surrender_button():
    header_font = pygame.font.Font(None, 40)  # Same size as rules header

    header = header_font.render("SURRENDER", True, BLACK)

    SCREEN_HEIGHT = 690
    button_x = 650
    button_y = SCREEN_HEIGHT - 101
    button_width = 150
    button_height = 50

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Check if the mouse is hovering over the button
    if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
        pygame.draw.rect(screen, (211, 211, 211), (button_x, button_y, button_width, button_height))  # Light gray background
    else:
        pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))  # Default background

    screen.blit(header, (button_x + (button_width - header.get_width()) // 2, button_y + (button_height - header.get_height()) // 2))

def draw_rules_info():
    font = pygame.font.Font(None, 20)  # Same size as command text
    header_font = pygame.font.Font(None, 28)  # Same size as command header
    
    header = header_font.render("Rules:", True, BLACK)
    
    rule1 = font.render("1. Only flat pieces count towards winning", True, BLACK)
    rule2 = font.render("2. Pieces can move in any direction", True, BLACK)
    rule3 = font.render("3. Standing pieces cannot be stacked upon", True, BLACK)
    rule4 = font.render("4. Maximum stack size is 5 pieces", True, BLACK)
    rule5 = font.render("5. Only the top piece of a stack can move", True, BLACK)

    # Set vertical positioning for rules, moving them up
    rules_bottom_offset = 690 - 80  # Adjusted position for rules
    line_height = 25  # Height of each line of text

    # Position rules below the commands
    screen.blit(header, (650, rules_bottom_offset - 200))  # Position header
    screen.blit(rule1, (650, rules_bottom_offset - 175))  # Move rule1 up
    screen.blit(rule2, (650, rules_bottom_offset - 150))  # Move rule2 up
    screen.blit(rule3, (650, rules_bottom_offset - 125))  # Move rule3 up
    screen.blit(rule4, (650, rules_bottom_offset - 100))  # Move rule4 up
    screen.blit(rule5, (650, rules_bottom_offset - 75))   # Move rule5 up



    
# Function to wait for a number between 1 and 5
def wait_for_input_1_to_5():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_3:
                    return 3
                elif event.key == pygame.K_4:
                    return 4
                elif event.key == pygame.K_5:
                    return 5
                else:
                    global error_message
                    error_message = "Please press a number between 1 and 5."
                    # Redraw screen to show error message
                    screen.fill(WHITE)
                    draw_board()
                    draw_game_info()
                    draw_invalid_move_info()
                    draw_commands_info()
                    draw_rules_info()
                    pygame.display.flip()
        
def handle_click(pos):
    global selected_row, selected_col, selected_pieces_to_move, error_message

    
    x, y = pos
    row = (y - OFFSET) // CELL_SIZE
    col = (x - OFFSET) // CELL_SIZE


    button_x = 650        # X position of the button
    button_y = 589        # Y position of the button (SCREEN_HEIGHT - 101)
    button_width = 150     # Approximate width of the "SURRENDER" text
    button_height = 50     # Approximate height of the "SURRENDER" text


    if(button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height):
        show_surrender_overlay()

    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        current_player = player1 if player1.turn else player2
        keys = pygame.key.get_pressed()
        shift_held = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        ctrl_held = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        
        stack = board.get_stack(col, row)
        
        if selected_row == -1 and selected_col == -1:  # No cell selected
            if stack.is_empty() and current_player.pieces_in_hand > 0:
                # Place new piece
                standing = shift_held  # Hold Shift to place standing piece
                piece = current_player.place_piece(standing)
                if piece:
                    board.place_piece(col, row, piece)
                    error_message = ""  # Clear error message
                    switch_turns()
            elif not stack.is_empty():
                if ctrl_held and current_player.pieces_in_hand > 0:
                    # Place new piece on existing stack
                    if stack.is_full():
                        error_message = "Cannot stack more pieces here; stack is full."
                    elif stack.top().standing:
                        error_message = "Cannot stack on a standing piece."
                    else:
                        standing = shift_held  # Can also hold Shift to place standing piece on stack
                        piece = current_player.place_piece(standing)
                        if piece:
                            board.place_piece(col, row, piece)
                            error_message = ""  # Clear error message
                            switch_turns()
                else:
                    top_piece = stack.top()
                    # Allow player to select their own piece, whether it's standing or flat
                    if top_piece.color == current_player.color:
                        # Ask user how many pieces to move
                        pieces_to_move = wait_for_input_1_to_5()
                        if pieces_to_move <= len(stack.stack):
                            selected_row, selected_col, selected_pieces_to_move = row, col, pieces_to_move
                            error_message = ""  # Clear error message
                            print(f"Selected {pieces_to_move} piece(s) at ({row}, {col})")
                        else:
                            error_message = "Not enough pieces to move."
                    else:
                        error_message = "Can't move this piece."
            else:
                error_message = "Invalid action."
        else:  # Cell selected
            try:
                target_stack = board.get_stack(col, row)
                if not target_stack.is_empty() and target_stack.top().standing:
                    error_message = "Cannot move onto standing pieces."
                else:
                    if(abs(selected_row - row) + abs(selected_col - col) == 1):

                        board.move_piece(selected_col, selected_row, col, row, selected_pieces_to_move)
                        error_message = ""  # Clear error message
                        switch_turns()
                    else:
                        error_message = "Invalid move: can only move to adjacent cells (no diagonal moves)."
                selected_row, selected_col = -1, -1
            except ValueError as e:
                error_message = f"Invalid move: {e}"
                selected_row, selected_col = -1, -1
    else:
        error_message = "Clicked outside the board."
    print(f"Clicked on cell {row}, {col}")

def handle_ai_move():
    ai = AI(difficulty=DIFFICULTY, player=Color.WHITE, grid_rows=BOARD_SIZE, grid_columns=BOARD_SIZE, max_height=5) 
    game_state = converter(board, player1, player2, TOTAL_MOVES, BOARD_SIZE)
    ai_move = ai.get_best_move(game_state)

    current_player = player2

    if ai_move.is_placement:
        piece = current_player.place_piece(ai_move.piece.is_vertical)
        if piece:
            board.place_piece(ai_move.x, ai_move.y, piece)
            switch_turns()
    else:
        board.move_piece(ai_move.x, ai_move.y, ai_move.to_x, ai_move.to_y, ai_move.count)
        switch_turns()

def switch_turns():
    """Switch turns and check for win/draw conditions."""
    global TOTAL_MOVES
    player1.toggle_turn()
    player2.toggle_turn()
    if player2.turn:
        handle_ai_move() #Call ai move function here instead of player2 
    TOTAL_MOVES += 1  # Increment the move counter
    check_win()  # Check if anyone has won
    check_draw()  # Check for the draw condition

    flat_winner = board.check_flat_win_condition()
    if flat_winner == "Draw":
        show_draw_overlay()
    elif flat_winner:
        show_flat_win_overlay(flat_winner)

def show_winner_overlay(winner):
    font = pygame.font.Font(None, 60)
    sub_font = pygame.font.Font(None, 36)
    winner_text = font.render(f"{winner} Wins!", True, BLUE)
    restart_text = sub_font.render("Press R to restart", True, BLACK)
    quit_text = sub_font.render("Press Q to quit", True, BLACK)
    
    # background
    overlay_rect = pygame.Rect(OFFSET // 2, SCREEN_SIZE // 4, SCREEN_SIZE - OFFSET, 400)
    pygame.draw.rect(screen, GRAY, overlay_rect)
    
    # display text
    screen.blit(winner_text, (SCREEN_SIZE // 2 - winner_text.get_width() // 2, SCREEN_SIZE // 3))
    screen.blit(restart_text, (SCREEN_SIZE // 2 - restart_text.get_width() // 2, SCREEN_SIZE // 2))
    screen.blit(quit_text, (SCREEN_SIZE // 2 - quit_text.get_width() // 2, SCREEN_SIZE // 2 + 40))
    pygame.display.flip()
    
    # handle restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # restarts
                    reset_game()
                    return
                elif event.key == pygame.K_q:  # quits
                    pygame.quit()
                    sys.exit()
                    


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def show_difficulty_selection():
    global DIFFICULTY
    font = pygame.font.SysFont(None, 55)
    running = True

    while running:
        screen.fill(WHITE)
        
        popup_width = 600
        popup_height = 400
        popup_x = (SCREEN_WIDTH - popup_width) // 2
        popup_y = (SCREEN_HEIGHT - popup_height) // 2

        pygame.draw.rect(screen, GRAY, (popup_x, popup_y, popup_width, popup_height), border_radius=BORDER_RADIUS)
        
        draw_text("Select AI Difficulty", font, BLACK, screen, SCREEN_WIDTH // 2, popup_y + 60)
        draw_text("EASY", font, BLACK, screen, SCREEN_WIDTH // 2, popup_y + 150)
        draw_text("MEDIUM", font, BLACK, screen, SCREEN_WIDTH // 2, popup_y + 225)
        draw_text("HARD", font, BLACK, screen, SCREEN_WIDTH // 2, popup_y + 300)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if popup_x + 100 < mouse_x < popup_x + popup_width - 100:
                    if popup_y + 125 < mouse_y < popup_y + 175:
                        DIFFICULTY = Difficulty.EASY
                        running = False
                    elif popup_y + 200 < mouse_y < popup_y + 250:
                        DIFFICULTY = Difficulty.MEDIUM
                        running = False
                    elif popup_y + 275 < mouse_y < popup_y + 325:
                        DIFFICULTY = Difficulty.HARD
                        running = False

        pygame.display.update()

def show_flat_win_overlay(winner):
    font = pygame.font.Font(None, 60)
    sub_font = pygame.font.Font(None, 36)
    winner_text = font.render(f"{winner} Flat Win!", True, BLUE)
    restart_text = sub_font.render("Press R to restart", True, BLACK)
    quit_text = sub_font.render("Press Q to quit", True, BLACK)
    
    # background
    overlay_rect = pygame.Rect(OFFSET // 2, SCREEN_SIZE // 4, SCREEN_SIZE - OFFSET, 400)
    pygame.draw.rect(screen, GRAY, overlay_rect)
    
    # display text
    screen.blit(winner_text, (SCREEN_SIZE // 2 - winner_text.get_width() // 2, SCREEN_SIZE // 3))
    screen.blit(restart_text, (SCREEN_SIZE // 2 - restart_text.get_width() // 2, SCREEN_SIZE // 2))
    screen.blit(quit_text, (SCREEN_SIZE // 2 - quit_text.get_width() // 2, SCREEN_SIZE // 2 + 40))
    pygame.display.flip()

    # handle restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # restarts
                    reset_game()
                    return
                elif event.key == pygame.K_q:  # quits
                    pygame.quit()
                    sys.exit()

def show_draw_overlay():
    font = pygame.font.Font(None, 60)
    sub_font = pygame.font.Font(None, 36)
    draw_text = font.render("Game Drawn!", True, BLUE)
    restart_text = sub_font.render("Press R to restart", True, BLACK)
    quit_text = sub_font.render("Press Q to quit", True, BLACK)

    # background
    overlay_rect = pygame.Rect(OFFSET // 2, SCREEN_SIZE // 4, SCREEN_SIZE - OFFSET, 400)
    pygame.draw.rect(screen, GRAY, overlay_rect)

    # display text
    screen.blit(draw_text, (SCREEN_SIZE // 2 - draw_text.get_width() // 2, SCREEN_SIZE // 3))
    screen.blit(restart_text, (SCREEN_SIZE // 2 - restart_text.get_width() // 2, SCREEN_SIZE // 2))
    screen.blit(quit_text, (SCREEN_SIZE // 2 - quit_text.get_width() // 2, SCREEN_SIZE // 2 + 40))
    pygame.display.flip()

    # handle restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # restarts
                    reset_game()
                    return
                elif event.key == pygame.K_q:  # quits
                    pygame.quit()
                    sys.exit()

def show_surrender_overlay():
    font = pygame.font.Font(None, 60)
    sub_font = pygame.font.Font(None, 36)
    draw_text = font.render("Surrendered", True, BLUE)
    restart_text = sub_font.render("Press R to restart", True, BLACK)
    quit_text = sub_font.render("Press Q to quit", True, BLACK)

    # background
    overlay_rect = pygame.Rect(OFFSET // 2, SCREEN_SIZE // 4, SCREEN_SIZE - OFFSET, 400)
    pygame.draw.rect(screen, GRAY, overlay_rect)

    # display text
    screen.blit(draw_text, (SCREEN_SIZE // 2 - draw_text.get_width() // 2, SCREEN_SIZE // 3))
    screen.blit(restart_text, (SCREEN_SIZE // 2 - restart_text.get_width() // 2, SCREEN_SIZE // 2))
    screen.blit(quit_text, (SCREEN_SIZE // 2 - quit_text.get_width() // 2, SCREEN_SIZE // 2 + 40))
    pygame.display.flip()

    # handle restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # restarts
                    reset_game()
                    return
                elif event.key == pygame.K_q:  # quits
                    pygame.quit()
                    sys.exit()


def check_win():
    if board.check_winning_condition(player1.color):
        show_winner_overlay("Black")
    elif board.check_winning_condition(player2.color):
        show_winner_overlay("White")

def check_draw():
    #Check if the game has reached the maximum number of moves for a draw.
    if TOTAL_MOVES >= MAX_MOVES:
        show_draw_overlay()  # Display draw overlay

    

def reset_game():
    # Restarts the game
    global board, player1, player2, selected_row, selected_col, selected_pieces_to_move, error_message, TOTAL_MOVES
    board = Board()  
    player1 = Player('black') 
    player2 = Player('white')  
    player1.toggle_turn()  
    selected_row, selected_col = -1, -1
    selected_pieces_to_move = 0
    error_message = "" 
    TOTAL_MOVES = 0


def main_game():
    show_difficulty_selection()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(pygame.mouse.get_pos())
        
        screen.fill(WHITE)
        draw_board()
        draw_game_info()
        draw_invalid_move_info() 
        draw_commands_info()
        draw_surrender_button()
        draw_rules_info()
        pygame.display.flip()

    pygame.quit()
    sys.exit()
    

if __name__ == '__main__':
    main_game()
