import pygame
from .constants import RED, SQUARE_SIZE, WHITE, BLUE
from checkers.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    # This function is private so that way no one else can call it, 
    # they would have to call the reset method
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        # Directory of valid moves
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            # If we already have something selected, let's try to move it to whatever else we just pressed
            result = self._move(row, col)
            # If that doesn't work or if a move doesn't make sense, we get a false back
            if not result:
                # Get rid of our current selection
                self.selected = None
                # Reselect something else (aka. call this method again)
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        # If we're not selecting an empty piece and the piece selected is the proper color 
        # in relation to the player's turn (aka. the selection was valid)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        # If the selection was invalid, we return false
        return False

    # This function is private so that way no one else can call it,
    # they would have to call the select method
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        # If we selected something and the piece that we selected is 0
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            # We will move the currently selected piece to the row and column
            # that was passed to us here
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        
        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
