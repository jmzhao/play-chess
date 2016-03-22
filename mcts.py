# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 10:47:48 2016

@author: jzhao
"""
import mover
import warnings

class MCTSException(Exception) :
    pass
class MCTSWarning(Warning) :
    pass

class TreeNodeWithIndexedChildren :
    def __init__(self, data) :
        self._children = dict()
        self._parent = None
        self.data = data
    def is_leaf(self) :
        return len(self._children) == 0
    def is_root(self) :
        return self._parent == None
    def set_child(self, key, data) :
        node = type(self)(data=data)
        node._parent = self
        self._children[key] = node
        return node
    def get_child(self, key) :
        return self._children[(key)]
    def has_child(self, key) :
        return key in self._children
    def set_default_child(self, key, default_data) :
        if self.has_child(key) :
            return self.get_child(key)
        else :
            return self.set_child(key, default_data)
    def get_children(self) :
        return self._children
    def __str__(self) :
        return 'data='+str(self.data)

class MCTSMover(mover.Mover) :
    ''' Mover using Monte Carlo Tree Search
    
    Internal Data Structure:
      Tree children indexed by move@Move
      Tree node data: data@{<game.party>:<# of winning>}
    '''
    def __init__(self, state, EasyMover, Tree=TreeNodeWithIndexedChildren) :
        super().__init__(state)
        self._Mover = EasyMover
        self._tree = Tree(data=self._gen_data(self._state))
    def get_current_state(self) :
        return self._state
    def next_move(self) :
        for _ in range(1000) :
            self.search_once(easy_mover=self._Mover(self.get_current_state()), 
                             node=self._tree)
            if min(sum(node.data.values()) 
                for node in self._tree.get_children().values()) > 99 :
                break
#        print(*[(str(move), str(node)) for move, node in self._tree._children.items()], 
#              sep='\n', flush=True) ##DEBUG
        party = self.get_current_state().next_moving_party()
        d_move_node = self._tree.get_children()
        try :
            l = list((node.data[party]/sum(node.data.values()), i, move) 
                for i, (move, node) in enumerate(d_move_node.items())
                if sum(node.data.values()) > 10)
            print(*sorted(l), sep='\n', flush=True) ##DEBUG ##LOG
            _, _, move = max(l)
        except ValueError :
            warnings.warn(MCTSWarning("no confidence for any moves, using EasyMover"))
            return self._Mover(self.get_current_state()).next_move()
        return move
    def make_move(self, move) :
        self._state.make_move(move)
        self._tree = self._tree.set_default_child(
            move, default_data=self._gen_data(self._state))
    @staticmethod
    def search_once(easy_mover, node) :
        state = easy_mover.get_current_state()
        if state.is_final() : ## or some other condition to stop deeper search/simulation            
            incremental_result = state.winning_parties_dict()
        else :
            move = easy_mover.next_move()
            easy_mover.make_move(move)
            nstate = easy_mover.get_current_state()
            nnode = node.set_default_child(
                move, default_data=MCTSMover._gen_data(nstate))
            incremental_result = MCTSMover.search_once(easy_mover, nnode)
        updated_data = dict((party, n_winning + node.data.get(party))
            for party, n_winning in incremental_result.items())
        node.data.update(updated_data)
        return incremental_result
    @staticmethod
    def _gen_data(state) :
        return dict.fromkeys(state.game.get_parties(),0)