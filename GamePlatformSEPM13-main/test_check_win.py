import unittest
from Board import Board
from Piece import Piece


class TestCheckWinningCondition(unittest.TestCase):
   
   
   def put_line(self, b, coords, color, standing=False):
       for x, y in coords:
           b.place_piece(x, y, Piece(color, standing=standing))


   def test_empty_board_no_win(self):
       b = Board()
       self.assertFalse(b.check_winning_condition('white'))
       self.assertFalse(b.check_winning_condition('black'))


   def test_scattered_no_connection(self):
       b = Board()
       self.put_line(b, [(0,0),(2,1),(4,2)], 'white')
       self.assertFalse(b.check_winning_condition('white'))


   def test_white_left_right_win(self):
       b = Board()
       self.put_line(b, [(x,0) for x in range(6)], 'white')
       self.assertTrue(b.check_winning_condition('white'))
       self.assertFalse(b.check_winning_condition('black'))


   def test_black_top_bottom_win(self):
       b = Board()
       self.put_line(b, [(2,y) for y in range(6)], 'black')
       self.assertTrue(b.check_winning_condition('black'))
       self.assertFalse(b.check_winning_condition('white'))


   def test_standing_blocks_path_even_same_color(self):
       b = Board()
       self.put_line(b, [(x,0) for x in range(6)], 'white')
       b.place_piece(3, 0, Piece('white', standing=True))
       self.assertFalse(b.check_winning_condition('white'))


   def test_only_top_piece_counts(self):
       b = Board()
       self.put_line(b, [(x,0) for x in range(6)], 'white')
       b.place_piece(2, 0, Piece('black', standing=False))
       self.assertFalse(b.check_winning_condition('white'))
       self.assertFalse(b.check_winning_condition('black'))


   def test_diagonal_is_not_connected(self):
       b = Board()
       self.put_line(b, [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)], 'white')
       self.assertFalse(b.check_winning_condition('white'))


   def test_multiple_starts_work(self):
       b = Board()
       self.put_line(b, [(0,0), (0,2)], 'white')
       self.put_line(b, [(1,2),(2,2),(3,2),(4,2),(5,2)], 'white')
       self.assertTrue(b.check_winning_condition('white'))


   def test_boundaries_interior_neighbors(self):
       b = Board()
       self.put_line(b, [(x,0) for x in range(6)], 'white')
       self.assertTrue(b.check_winning_condition('white'))


   def test_interrupted_by_gap(self):
       b = Board()
       coords = [(0,0),(1,0),(2,0),(4,0),(5,0)]
       self.put_line(b, coords, 'white')
       self.assertFalse(b.check_winning_condition('white'))


   def test_path_turns_are_allowed(self):
       b = Board()
       self.put_line(b, [(2,0),(2,1),(2,2),(2,3)], 'black')
       self.put_line(b, [(3,3),(4,3),(5,3)], 'black')
       self.put_line(b, [(5,4),(5,5)], 'black')
       self.assertTrue(b.check_winning_condition('black'))


if __name__ == '__main__':
   unittest.main(verbosity=2)