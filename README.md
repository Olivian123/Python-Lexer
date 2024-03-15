# Python Lexer
This Lexer module is implemented in Python and provides functionality to tokenize input strings based on a set of specifications. The specifications define lexemes, which are substrings of characters classified into tokens. This lexer utilizes principles of Deterministic Finite Automaton (DFA) and Non-deterministic Finite Automaton (NFA) for efficient lexical analysis.

Overview
The lexer operates by first constructing a DFA from the provided regular expressions, which represent the token specifications. Then, it applies the DFA to the input string to identify and tokenize the lexemes according to the defined specifications.

Components
DFA
The DFA (Deterministic Finite Automaton) class represents a deterministic finite automaton. It contains states, alphabet symbols, transition function, initial state, and set of accepting states. The DFA is used to efficiently recognize tokens in the input string.

NFA
The NFA (Non-deterministic Finite Automaton) class represents a non-deterministic finite automaton. It contains states, alphabet symbols, transition function, initial state, and set of accepting states. The NFA is utilized in the process of constructing the DFA from regular expressions.

Regex
The Regex class provides functionality to parse regular expressions and convert them into NFAs. It supports various operations such as concatenation, alternation (OR), Kleene star (*), and optional (?).

Usage
Specify Token Definitions: Define token specifications by providing tuples containing token names and corresponding regular expressions.

Tokenize Input: Use the lex method to tokenize input strings.
lexer = Lexer([
    ("INTEGER", r"\d+"),
    ("PLUS", r"\+"),
    ("MINUS", r"\-"),
    ("MULTIPLY", r"\*"),
    ("DIVIDE", r"\/"),
])

tokens = lexer.lex("3 + 5 * 2")
print(tokens)
# Output: [('INTEGER', '3'), ('PLUS', '+'), ('INTEGER', '5'), ('MULTIPLY', '*'), ('INTEGER', '2')]

Features
Subset Construction: The lexer utilizes the subset construction algorithm to convert NFAs generated from regular expressions into a DFA, which efficiently recognizes tokens.
Efficient Lexing: By leveraging DFA, the lexer ensures efficient and deterministic tokenization of input strings.
Support for Regular Expressions: Regular expressions with operations like concatenation, alternation, Kleene star, and optional are supported for defining token specifications.
For any further questions or issues, please refer to the documentation or contact the module maintainer.
