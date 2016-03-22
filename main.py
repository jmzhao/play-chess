# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 14:21:52 2016

@author: jzhao
"""

import mcts
import mover
import tictactoe as ttt

class ScreenInputMover (mover.NaiveMover) :
    def next_move(self) :
        print("Your move? ('<row> <col>', e.g. '1 1')")
        r, c = [int(x) for x in input().split()]
        move = ttt.TicTacToeMove(state.next_moving_party(), 
                                 ttt.TicTacToe.Board.sub2ind((r, c)))
        return move

state = ttt.TicTacToeState()
#m1 = ScreenInputMover(state)
m1 = mcts.MCTSMover(state, mover.UniformRandomMover)
#m2 = ScreenInputMover(state)
m2 = mcts.MCTSMover(state, mover.UniformRandomMover)

while not state.is_final() :
    print(str(state))
    move = m1.next_move()
    print(str(move))
    m1.make_move(move)
    m2.make_move(move)
    s1 = m1.get_current_state()
    s2 = m2.get_current_state()
    assert s1._play_seq == s2._play_seq
    state = s1.copy()
    m1, m2 = m2, m1
 
print(str(state))   
print('Game finished.')
d = state.winning_parties_dict()
print('Result:', ', '.join(
    ttt.TicTacToe.party_symbol[party]+':'+str(score) for party, score in d.items()))
    
    
    