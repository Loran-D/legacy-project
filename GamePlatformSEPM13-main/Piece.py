class Piece:
    def __init__(self, color, standing: bool = False):
        self.color = color
        self.standing = standing  

    def is_standing(self):
        return self.standing
    
    # Representation of the piece
    def __repr__(self):
        piece_type = 'flat' if not self.standing else 'standing'
        return f"{piece_type} piece"
