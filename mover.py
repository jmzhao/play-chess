# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:48:33 2016

@author: jzhao
"""
import random

class MoverException (Exception) :
    pass


class Mover :
    def __init__(self, state) :
        self._state = state.copy()
    def next_move(self, party) :
        raise MoverException('Mover method "%s" is not implemented'%('next_move'))
    def make_move(self, move) :
        raise MoverException('Mover method "%s" is not implemented'%('make_move'))
    def get_current_state(self) :
        raise MoverException('Mover method "%s" is not implemented'%('get_current_state'))

class NaiveMover (Mover) :
    def next_move(self, party=None) :
        return list(self.state.legal_moves(party))[0]
    def make_move(self, move) :
        self._state.make_move(move)
    def get_current_state(self) :
        return self._state

class SimpleRandomMover (NaiveMover) :
    def __init__(self, state, random_picker) :
        super().__init__(state)
        self.random_picker = random_picker
    def next_move(self, party=None) :
        return self.random_picker(self._state.legal_moves(party))

class UniformRandomMover (SimpleRandomMover) :
    def __init__(self, state) :
        super().__init__(state, random_picker=lambda seq : random.choice(list(seq)))