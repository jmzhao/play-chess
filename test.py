# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 19:59:51 2016

@author: jzhao
"""

import tictactoe as ttt
import mover

s = ttt.TicTacToeState()
print(s)
print(*s.legal_moves())
print(*[hash(m) for m in s.legal_moves()])
mr = mover.UniformRandomMover(s)
d = {}
for _ in range(100) :
    m = mr.next_move()
    d[m] = d.get(m, 0) + 1
print(d)