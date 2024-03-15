from .NFA import NFA

class Regex:
    nr_of_states = 0

    @staticmethod
    def add_state():
        Regex.nr_of_states += 1

    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

    def thompson(self) -> NFA[int]:
        Regex.add_state() # the initial state of the crt. NFA
        
        nfa = NFA(set(), set(), Regex.nr_of_states, {}, set())
        
        # Just a symbol or the leaf of the regex tree 
        # (s1) ----- symbol -----> (s2)
        if self.left == None and self.right == None:
            self.make_symbol_nfa(nfa)
            return nfa

        # Geting the left and right nfa 
        nfa_l, nfa_r = self.get_left_and_right_nfas()

        Regex.add_state() # the finall state of the crt. NFA
        self.set_nfa_without_d(nfa, nfa_l, nfa_r)

        if self.val == "con":
            self.construct_d_con(nfa, nfa_l, nfa_r)

        elif self.val == "or":
            self.construct_d_or(nfa, nfa_l, nfa_r)

        elif self.val == '*':
            self.construct_d_star(nfa, nfa_r)

        elif self.val == "?":
            self.construct_d_question(nfa, nfa_l, nfa_r)

        return nfa

    # Constructs the NFA for a single symbol
    # or a syntactic sugar
    def make_symbol_nfa(self, nfa):
        Regex.add_state() 

        nfa.K = {Regex.nr_of_states, nfa.q0} # seting the states
        
        # Adding transitions for syntactic sugars [0-9], [a-z], [A-Z]
        # and updating the alphabet
        if '[' in self.val:
            for i in range(ord(self.val[1]), ord(self.val[3]) + 1):
                    nfa.S.update({str(chr(i))})
            
                    nfa.d[(nfa.q0, chr(i))] = {Regex.nr_of_states}

        # Adding the transition for symple symbol
        else:
            # In case there was an operator and had '\\' in front
            if '\\' in self.val:
                self.val = self.val[1:]

            nfa.S = {str(self.val)}
                
            nfa.d[(nfa.q0, self.val)] = {Regex.nr_of_states}

        nfa.F = {Regex.nr_of_states} # adding the finall state

    # Adding transitions for concatenation of two NFA
    def construct_d_con(self, nfa, nfa_l, nfa_r):
        nfa.d[nfa.q0, ''] = {nfa_l.q0}
        
        nfa.d.update(nfa_l.d)
        nfa.d[nfa_l.F.pop(), ''] = {nfa_r.q0}
        nfa.d.update(nfa_r.d)
        
        nfa.d[nfa_r.F.pop(), ''] = {Regex.nr_of_states}

    # Adding transitions for or operation of two NFA
    def construct_d_or(self, nfa, nfa_l, nfa_r):
        nfa.d[(nfa.q0, '')] = {nfa_l.q0, nfa_r.q0}

        nfa.d.update(nfa_l.d)
        nfa.d.update(nfa_r.d)
            
        nfa.d[(nfa_l.F.pop(), '')] = {Regex.nr_of_states}
        nfa.d[(nfa_r.F.pop(), '')] = {Regex.nr_of_states}

    # Adding transitions for star operation of two NFA
    def construct_d_star(self, nfa, nfa_r):
        nfa.d[(nfa.q0, '')] = {nfa_r.q0, Regex.nr_of_states}
        nfa.d.update(nfa_r.d)
        nfa.d[(nfa_r.F.pop(), '')] = {nfa_r.q0, Regex.nr_of_states}

    # Adding transitions for question operation of two NFA
    def construct_d_question(self, nfa, nfa_l, nfa_r):
        nfa.d[(nfa.q0, '')] = {nfa_r.q0, Regex.nr_of_states}

        nfa.d.update(nfa_l.d)
        nfa.d.update(nfa_r.d)
            
        nfa.d[(nfa_r.F.pop(), '')] = {Regex.nr_of_states}

    # Sets the NFA data beside the transition function
    # returns the NFA of the right and left side 
    def set_nfa_without_d(self, nfa, nfa_l, nfa_r):
        nfa.S = nfa_r.S | nfa_l.S # updating the alphabet 

        # Updating the set of states
        nfa.K = {nfa.q0, Regex.nr_of_states} | nfa_l.K | nfa_r.K
            
        nfa.F = {Regex.nr_of_states} # the final state of the crt. NF

    # Returns the left and right nfas
    def get_left_and_right_nfas(self):
        # For the star, plus and question operation
        # the NFA that they are apllied to one NFA 
        # witch is placed on the right sife so
        # (nfa.left).thompson() does not work
        if self.left == None:
            nfa_l = NFA(set(), set(), None, {}, set()) 
        else :
            nfa_l = (self.left).thompson()

        nfa_r = (self.right).thompson()

        # The right and left NFA are ussed to construct
        # the transition fucntion
        return nfa_l,nfa_r

operators = ['*' , '+', '?']

# Retunrs all the srintgs inside and outside 
# the first pharanteses groups
def surrounded_by_parentheses(s):
    count = 0
    count_ss = 0
    token = ''
    tokens = []
    ant = None

    for char in s:
        token += char

        if ant != '\\':
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
            elif char == '[':
                count_ss += 1
            elif char ==']':
                count_ss -= 1

        # When a closeed group is found (...) or an open one )...(
        if count == 0 and count_ss == 0:
            # Adding special characters            
            if ant == '\\':
                tokens.append(ant + char)

            # In the current token an operator is possible be taken
            # so we need to put it back to the last token in tokens
            elif token[0] in operators and len(tokens) != 0:
                tokens[-1] += token[0]

                # Appending the token without the operator to tokens
                if(len(token[1:]) > 0):
                    tokens.append(token[1:])
            
            elif char != '\\':
                tokens.append(token)
            
            # Reseting the token 
            token = ''
        
        ant = char

    # In the case where <space> comes with '\' it needs
    # to remain in the list as '\\<space>', the algorithm keeps
    # '<space>' also so it needs to be removed
    tokens = [r for r in tokens if r not in [' ']]

    # In casse of <regex>+ it simpler to work with (<regex><regex>*)
    tokens = ['(' + s[:-1] + s[:-1] + '*' + ')' if s[-1] == '+' and s[-2] != '\\' else s for s in tokens]
    return tokens # for saffety

# When working trough the regex string when adding concatenations or 
# 'or' operation always at the end remains an concatenation op
# 
#           ...                  
#         /                     ...
#     __con__       =>        /
#    /       \              sym
#  sym       con
def remove_useless_last_op(ant):
    aux = ant.left
    ant.val = aux.val
    ant.left = aux.left
    ant.right = aux.right

def parse_regex(regex: str) -> Regex:    
    regexes = surrounded_by_parentheses(regex)

    root = Regex('con')
    ant = None

    # The root will be changed trough the procees, ret keeps
    # the pointer to the root that needs to be returned
    ret = root 
    for reg in regexes:
        # In case we find an or operation
        if reg == '|' :
            # We need a new root with the or operation
            new_root = Regex('or')
            
            # To the left of the new root we add the old root
            new_root.left = ret
            ret = new_root  

            # There is an uselles operation in the end and
            # it needs to be removed
            remove_useless_last_op(ant)
        
            # It is possible that there will be more concatenations,
            # we add the operation, if it is uselles, it
            # will be removed at the end of the function 
            new_root.right = Regex('con')
            root = new_root.right
            continue
        
        # Check if the regex is surounded by pharantes 
        # with or without an operation
        if reg[0] == '(':
            # Without operation
            if reg[-1] == ')':
                root.left = parse_regex(reg[1:-1])
                
            # With an operation
            if reg[-2] == ')' and reg[-1] in operators:
                root.left = Regex(reg[-1])
                root.left.right = parse_regex(reg[1:-2])
    
        # Parssing a simple regex just concatenations 
        # and simple operators
        if (len(reg) == 2 and reg[0] != '\\' or reg[0] == '[') and reg[-1] in operators:
            root.left = Regex(reg[-1])
            root.left.right = Regex(reg[0:-1])

        elif (len(reg) == 1 and reg != '|') or reg[0] in ['[', '\\']:
            root.left = Regex(reg)

        root.right = Regex('con')
        ant = root
        root = root.right

    remove_useless_last_op(ant)
    return ret