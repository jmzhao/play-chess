# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 14:23:31 2016

@author: jzhao
"""
import gamebase as gb

class TicTacToe (gb.Game) :
    class Parties :
        def __init__(self) :
            self.CIRCLE = 0
            self.CROSS = 1
    party = Parties()
    party_list = party.__dict__.values()
    first_moving_party = party.CIRCLE
    party_symbol = {0:'O', 1:'X'}
    
    class Board :
        n_col = 3
        n_row = 3
        
        @staticmethod
        def sub2ind(pos) :
            row, col = pos
            return row * TicTacToe.Board.n_col + col
        @staticmethod
        def ind2sub(ind) :
            return (ind // TicTacToe.Board.n_col, ind % TicTacToe.Board.n_col)
        

class TicTacToeMove (gb.Move) :
    game = TicTacToe
    n_party = len(game.party_list)
    def __init__(self, party, pos) :
        self.party = party
        self.pos = pos ## ind
    def __hash__(self) :
        return self.pos * self.n_party + self.party
    def __eq__(self, other) :
        return hash(self) == hash(other)
    def __str__(self) :
        return (self.game.party_symbol[self.party] 
            + '@' + str(self.game.Board.ind2sub(self.pos)))
    __repr__ = __str__

class TicTacToeState (gb.State) :
    game = TicTacToe
    n_grid = game.Board.n_col * game.Board.n_row
    lines = [(0,1,2), (3,4,5), (6,7,8),
             (0,3,6), (1,4,7), (2,5,8),
             (0,4,8), (2,4,6)]
    
    def __init__(self, party=game.first_moving_party, seq=list()) :
        self._play_seq = list(seq)
        self._party_iter = self.game.get_party_playing_iter(start_after=party)
        self._next_party = party
        
    def copy(self) :
        s = type(self)(self._next_party, self._play_seq)
        return s
    
    def next_moving_party(self) :
        return self._next_party
    
        
    def legal_moves(self, party=None) :
        ''' a sequence of all legal next moves
        
PARAMETER:
    party - the party for which to generate legal moves.
        '''    
        s = set(m.pos for m in self._play_seq)
        for i in range(self.n_grid) :
            if i not in s :
                yield TicTacToeMove(self._next_party, i)
    
    def make_move(self, move) :
        ''' transit the state according to the move
        
PARAMETER:
    move@TicTacToeMove
        '''        
        assert (move.party == self.next_moving_party())
        self._play_seq.append(move)
        self._next_party = next(self._party_iter)
    
    def is_final(self) :
        if len(self._play_seq) >= self.n_grid :
            self._score = dict.fromkeys(self.game.party_list, 1/len(self.game.party_list))
            return True
        
        for party in self.game.party_list :
            s = set(m.pos for m in self._play_seq if m.party == party)
            for line in self.lines :
                if all(ind in s for ind in line) :
                    self._score = {party:1}
                    return True
        return False
    
    def winning_parties_dict(self) :
        return self._score
        
    def __str__(self) :
        l = [['_' for j in range(self.game.Board.n_col)] 
            for i in range(self.game.Board.n_row)]
        for m in self._play_seq :
            r, c = self.game.Board.ind2sub(m.pos)
            l[r][c] = self.game.party_symbol[m.party]
        return '\n'.join(''.join(li) for li in l)