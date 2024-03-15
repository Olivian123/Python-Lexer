from src.DFA import DFA
from src.NFA import NFA
from src.Regex import Regex
from src.Regex import parse_regex

class Lexer:
    token_names: {}
    dfa: DFA

    def __init__(self, spec: list[tuple[str, str]]) -> None:
        # initialization should convert the specification to a DFA which will be used in the lex method
        # the specification is a list of pairs (TOKEN_NAME:REGEX)
        nfa_list = [(name, parse_regex(regex).thompson()) for (name, regex) in spec]

        reg = Regex(None)
        final_nfa = NFA(set(), {0}, 0, {}, set())
        final_nfa.d[(final_nfa.q0, '')] = set()

        # Iterate through the list and constructing the final nfa
        for (_, nfa) in nfa_list:
            final_nfa.S.update(nfa.S)
            final_nfa.K.update(nfa.K)

            final_nfa.d[(final_nfa.q0, '')].add(nfa.q0)
            final_nfa.d.update(nfa.d)

            final_nfa.F.update(nfa.F)

        self.token_names = {nfa.F.pop(): name for name, nfa in nfa_list}
        self.dfa = final_nfa.subset_construction()
    
    def get_token_name(self, token):
    
        min_key = Regex.nr_of_states
        final_state = self.dfa.accept_f(token)

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

        while token != "":
            if len(token) == 1 and token[0] not in self.dfa.S:
                crt_char -= 1

            if not self.dfa.accept(token):
                token = token[:-1]
                continue

            crt_char += len(token)

            if "\n" in token:
                crt_line += 1
                crt_char = 1

            tokens_list.append((self.get_token_name(token), token))

            index = word.find(token)
            word = word[:index] + word[index + len(token):]
            token = word

        if len(word) == 1 and word[0] in self.dfa.S:
             return [("", "No viable alternative at character EOF, line " + str(crt_line))]

        if word != "":
            return [("", "No viable alternative at character " + str(crt_char) + ", line " + str(crt_line))]

        return tokens_list
    
spec = [
        ("SPACE", "\\ "),
        ("NEWLINE", "\n"),
        ("ABC", "a(b+)c"),
        ("AS", "a+"),
        ("BCS", "(bc)+"),
        ("DORC", "(d|c)+")
    ]

lexer = Lexer(spec)

print(lexer.lex("dccbcbcaaaa abbcf"))


