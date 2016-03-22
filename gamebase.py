# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 14:32:15 2016

@author: jzhao
"""
import itertools

class Game :
    @classmethod
    def get_parties(cls) :
        return cls.party_list
    @classmethod
    def get_party_playing_iter(cls, start_after) :
        party_iter = itertools.cycle(cls.get_parties())
        next_party = None
        while next_party != start_after :
            next_party = next(party_iter)
        return party_iter
        
class Move :
    def __hash__(self) :
        raise Exception("no implementation")

class State :
    game = None
        
    def copy(self) :
        pass
    
    def next_moving_party(self) :
        pass
    
        
    def legal_moves(self) :
        ''' a sequence of all legal next moves
        
PARAMETER:
    party - the party for which to generate legal moves.
        '''        
        pass
    
    def make_move(self, move) :
        ''' transit the state according to the move
        
PARAMETER:
    move@Move
        '''        
        pass
    
    def is_final(self) :
        pass
    
    def winning_parties_dict(self) :
        pass