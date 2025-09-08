from Stack import Stack
from Piece import Piece

## Added a few changes to try and implement it with UI // Ludvig

class Board:
    def __init__(self):
        self.grid = [[Stack() for _ in range(6)] for _ in range(6)]
    
    def current_placement(self):
        return [[stack.size() for stack in row] for row in self.grid]
    
    # Place a piece or a stack on the board
    def place_piece(self, x, y, place):
        # Places a piece on the board
        if isinstance(place, Piece) or isinstance(place, Stack):
            self.grid[y][x].push(place)
        else:
            raise TypeError("Invalid type for placing.")
    
    def move_piece(self, x1, y1, x2, y2, count=1):
        if count > self.grid[y1][x1].size():
            raise ValueError("Not enough pieces to move.")
        if x1 == x2 and y1 == y2:
            raise ValueError("Cannot move to the same position.")
        
        # Tries to move piece from one stack to another
        
        moved_stack = self.grid[y1][x1].pop(count)
        
        try:
            self.grid[y2][x2].push(moved_stack)
        except Exception as e:
            self.grid[y1][x1].push(moved_stack)
            raise e
    
    def get_stack(self, x, y):
        return self.grid[y][x]
    
    def check_winning_condition(self, color):
        def dfs(x, y, visited, vertical):
            if (x, y) in visited:
                return False
            visited.add((x, y))

            # Check if we reached the opposite side
            if vertical and y == len(self.grid) - 1:  #len(self.grid) is for rows
                return True
            elif not vertical and x == len(self.grid[0]) - 1:  # len(self.grid[0]) is for columns
                return True

            # Directions: up, down, left, right
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]):
                    stack = self.get_stack(nx, ny)
                    if stack and not stack.is_empty() and stack.top().color == color and not stack.top().is_standing():
                        if dfs(nx, ny, visited, vertical):
                            return True
            return False

        # Check from top to bottom (vertical win condition)
        for x in range(len(self.grid)):  # len(self.grid) for rows
            stack = self.get_stack(x, 0)
            if stack and not stack.is_empty() and stack.top().color == color and not stack.top().is_standing():
                if dfs(x, 0, set(), vertical=True):
                    return True

        # Check from left to right (horizontal win condition)
        for y in range(len(self.grid[0])):  #len(self.grid[0]) for columns
            stack = self.get_stack(0, y)
            if stack and not stack.is_empty() and stack.top().color == color and not stack.top().is_standing():
                if dfs(0, y, set(), vertical=False):
                    return True

        return False
    

    
    def check_flat_win_condition(self):
        flat_counts = {}
        empty_cells = False

        
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                stack = self.get_stack(x, y)

                
                if stack.is_empty():
                    empty_cells = True
                    break  

                
                if not stack.is_empty() and stack.top().color not in flat_counts:
                    flat_counts[stack.top().color] = 0

                if not stack.is_empty() and not stack.top().is_standing():
                    flat_counts[stack.top().color] += 1

            if empty_cells:  
                break

        
        if empty_cells:
            return False

        
        max_flats = -1
        winner = None
        for color, count in flat_counts.items():
            if count > max_flats:
                max_flats = count
                winner = color
            elif count == max_flats:
                return "Draw"

        
        return winner

    def __repr__(self):
        placement = self.current_placement()
        return "\n".join(" ".join(str(size) for size in row) for row in placement)

def main ():
    board = Board()
    stack = Stack()
    piece = Piece('black')
    stack.push(piece)
    board.place_piece(0, 0, stack)
    board.place_piece(0, 1, stack)
    board.place_piece(0, 2, stack)
    board.place_piece(0, 3, stack)
    board.place_piece(0, 4, stack)
    board.place_piece(0, 5, stack)
    print(board)
    print(board.check_winning_condition('black'))
    print(board.check_winning_condition('white'))

    piece = Piece('white')
    stack.push(piece)

    board.place_piece(0, 3, stack)
    board.place_piece(1, 3, stack)
    board.place_piece(2, 3, stack)
    board.place_piece(3, 3, stack)
    board.place_piece(4, 3, stack)
    board.place_piece(5, 3, stack)

    print(board)
    print(board.check_winning_condition('white'))

    board.place_piece(3, 3, Piece('black', standing=True))

    print(board)
    print(board.check_winning_condition('white'))

    board.place_piece(2, 2, Piece('white'))
    board.place_piece(3, 2, Piece('white'))
    board.place_piece(4, 2, Piece('white'))

    print(board)
    print(board.check_winning_condition('white'))

    
    board.place_piece(3, 2, Piece('white', standing=True))

    print(board)
    print(board.check_winning_condition('white'))

if __name__ == "__main__":
    main()
