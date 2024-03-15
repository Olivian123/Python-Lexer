from .DFA import DFA

from dataclasses import dataclass
from collections.abc import Callable

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs


@dataclass
class NFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], set[STATE]]
    F: set[STATE]

    def epsilon_closure_set(self, state: STATE, states: set):
        states.add(state)

        if (state, '') not in self.d:
            return
        
        # adding to the set only the states that did not appear
        [self.epsilon_closure_set(next, states) for next in self.d[(state, EPSILON)] if next not in states]

    def epsilon_closure(self, state: STATE) -> set[STATE]:
        # compute the epsilon closure of a state (you will need this for subset construction)
        # see the EPSILON definition at the top of this file
        closure_set = set()
        self.epsilon_closure_set(state, closure_set)
        return closure_set
    
    def get_next_states(self, d, state, k):
        # returns for all characters in the alphabet and a state the next state

        # geting just the states that have a transition with a character in the nfa
        pairs = [(x, y) for x in state for y in self.S]
        pairs = list(filter(lambda pair: pair, pairs)) # am modificat aici

        # initialization of transition function
        for pair in pairs :
            d[(frozenset(state), pair[1])] = frozenset()

        # for each next transition geting the epsilon closure and adding it to the new state
        for pair in pairs:
            all_next_states = [self.epsilon_closure(next_state) for next_state in self.d[pair]]
            next = set.union(*all_next_states)

            d[(frozenset(state), pair[1])] =  frozenset(d[(frozenset(state), pair[1])].union(next))

        # adding the new states
        for pair in pairs :
            if d[(frozenset(state), pair[1])] not in k:
                k.append(d[(frozenset(state), pair[1])])
    
    def add_sink_state(self, d, k):
        pairs = [(frozenset(x), y) for x in k for y in self.S]
        pairs = filter(lambda pair: pair not in d, pairs)

        # if all states have a transition on all the characters
        # there is no need to add sink state
        if pairs != []:
            # add sink state to states
            k.append(frozenset('_')) 
            
            # add transition to sink state for each state that needs it
            [d.update({pair : frozenset('_')}) for pair in pairs]

            # for each character in the alphabet add transition fro sink state to itself
            [d.update({(frozenset('_'), x): frozenset('_')}) for x in self.S]


    def subset_construction(self) -> DFA[frozenset[STATE]]:
        # convert this nfa to a dfa using the subset construction algorithm
        d = {} # transition function

        initial = self.epsilon_closure(self.q0)
        k = [initial] # list of states, will be made in set of frozenstets

        # new states get added in k for each iteration untill
        # there are no more new states to come
        for state in k:
            self.get_next_states(d, state, k)

        self.add_sink_state(d, k)

        # create set of final states
        F = set()
        for state in k:
            if any(sub_state in state for sub_state in self.F):
                F.add(frozenset(state))

        # make k from list of sets to set of frozensets
        k = set([frozenset(state) for state in k])

        # make result of function also frozenset
        map(lambda x : frozenset(x), d)

        return DFA(self.S, k, frozenset(initial), d, F)

    def remap_states[OTHER_STATE](self, f: 'Callable[[STATE], OTHER_STATE]') -> 'NFA[OTHER_STATE]':
        # optional, but may be useful for the second stage of the project. Works similarly to 'remap_states'
        # from the DFA class. See the comments there for more details.
        pass
