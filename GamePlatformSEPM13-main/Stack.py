from Piece import Piece
from collections import deque

class Stack:
    def __init__(self):
        # Stack of pieces
        self.stack = deque()

    # Push a piece or stack of pieces onto the stack
    def push(self, item):
        # Check if item is a piece or stack
        if isinstance(item, Piece) or isinstance(item, Stack):
            # Check if stack is full
            if len(self.stack) + (len(item.stack) if isinstance(item, Stack) else 1) <= 5:
                # Add piece or stack to the stack
                if isinstance(item, Stack):
                    self.stack.extend(item.stack)
                else:
                    self.stack.append(item)
            else:
                raise ValueError("Stack can only hold up to 5 pieces.")
        else:
            raise TypeError("Only Piece or Stack instances can be added to the stack.")
        
    # Pop a piece or stack of n pieces from the stack
    def pop(self, n=1):
        # Check if stack is empty or n is greater than the number of elements in the stack
        if n > len(self.stack):
            raise IndexError("Pop from an empty stack or not enough elements.")

        # Pop a piece or stack of n pieces from the stack
        if n == 1:
            return self.stack.pop()
        else:
            new_stack = Stack()
            for _ in range(n):
                new_stack.stack.appendleft(self.stack.pop())
            return new_stack
        
    # Check if the stack is empty
    def is_empty(self):
        return len(self.stack) == 0
    
    # Check if the stack is full
    def is_full(self):
        return len(self.stack) == 5
    
    def top(self):
        if self.is_empty():
            return None  # or raise an exception
        return self.stack[-1]
    
    # Get the size of the stack
    def size(self):
        return len(self.stack)
    
    # Representation of the stack
    def __repr__(self):
        pieces_repr = ", ".join([piece.__repr__() for piece in self.stack])
        return f"Stack({pieces_repr})"
    
def main():
    # Create a stack
    stack = Stack()
    
    # Create a piece
    piece = Piece('black')
    
    # Push the piece onto the stack
    stack.push(piece)
    
    # Print the stack
    print(stack)
    
    # Pop the piece from the stack
    popped_piece = stack.pop()
    
    # Print the popped piece
    print(popped_piece)
    
    # Check if the stack is empty
    print(stack.is_empty())
    
    # Check if the stack is full
    print(stack.is_full())
    
    # Check the size of the stack
    print(stack.size())

    new_stack = Stack()

    for _ in range(3):
        new_stack.push(Piece('white'))
    new_stack.push(Piece('black'))

    print(new_stack)

    print(new_stack.top().color)

    print(new_stack.is_empty())

    print(new_stack.is_full())

    print(new_stack.size())

    try:
        new_stack.push(Stack())
    except ValueError as e:
        print(e)

    stack.push(new_stack)

    print(stack)

if __name__ == "__main__":
    main()
