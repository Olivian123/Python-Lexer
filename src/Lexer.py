from src.DFA import DFA
from src.NFA import NFA
from src.Regex import Regex
from src.Regex import parse_regex

class Lexer:
    token_names: {} # type: ignore
    dfa: DFA

    def __init__(self, spec: list[tuple[str, str]]) -> None:
        # initialization should convert the specification to a DFA which will be used in the lex method
        # the specification is a list of pairs (TOKEN_NAME:REGEX)

        # Make a NFA out of all the regexes provided
        nfa_list = [(name, parse_regex(regex).thompson()) for (name, regex) in spec]

        final_nfa = NFA(set(), {0}, 0, {}, set()) # the final nfa
        
        # Set the transition from final_nfa.q0 to all initiall
        # states of all the other nfas
        final_nfa.d[(final_nfa.q0, '')] = set()

        # Iterate through the list and constructing the final nfa
        for (_, nfa) in nfa_list:
            # Updating the alphabet and states
            final_nfa.S.update(nfa.S)
            final_nfa.K.update(nfa.K)

            # adding the transition to the initial state of the crt. nfa
            final_nfa.d[(final_nfa.q0, '')].add(nfa.q0)
            final_nfa.d.update(nfa.d)

            # adding the final state of the nfa
            final_nfa.F.update(nfa.F)

        # Making a dicitionary that for the final state given returns
        # the name of the token
        self.token_names = {nfa.F.pop(): name for name, nfa in nfa_list}
        # Setting the DFA of the lexer
        self.dfa = final_nfa.subset_construction()
    
    def get_token_name(self, token):
        # Returns the name of the token bassed on the crt token
        min_key = Regex.nr_of_states
        final_state = self.dfa.accept_f(token)

        # The finall states of the DFA may not contain just the final
        # state of the nfa, but more states. In the case that more nfas
        # accept the same token the DFA final state will contain all the
        # final states of those nfas, so the token with the smallest 
        # final state number is chosen.
        for nfa_state in final_state:
            if nfa_state in self.token_names and nfa_state < min_key:
                min_key = nfa_state

        return self.token_names[min_key]

    def lex(self, word: str) -> list[tuple[str, str]] | None:
        # this method splits the lexer into tokens based on the specification and the rules described in the lecture
        # the result is a list of tokens in the form (TOKEN_NAME:MATCHED_STRING)

        # if an error occurs and the lexing fails, you should return none # todo: maybe add error messages as a task
        tokens_list = []
        token = word

        crt_char = 1
        crt_line = 0

        # In orrder to find the maximal match we are going from
        # the end of the word to the start tring to match the
        # longest word
        while token != "":
            if len(token) == 1 and token[0] not in self.dfa.S:
                crt_char -= 1

            if not self.dfa.accept(token):
                token = token[:-1]
                continue
            
            # If we passed the previous if it means that we found a 
            # maximal match so we add the length of the fond token
            # to crt_char
            crt_char += len(token)

            # In case we fond a new line we start with crt_char from 0
            if "\n" in token:
                crt_line += 1
                crt_char = 1

            tokens_list.append((self.get_token_name(token), token))

            # "Subtracting" the token from the word, for example: 
            # word = "upload" and token = "up", word - token = "load"
            word = word[len(token):]
            token = word

        if len(word) == 1 and word[0] in self.dfa.S:
             return [("", "No viable alternative at character EOF, line " + str(crt_line))]

        if word != "":
            return [("", "No viable alternative at character " + str(crt_char) + ", line " + str(crt_line))]

        return tokens_list