import os
import re
import sys


def isnonterminal(x):
    return isinstance(x, str) and re.match(r'^<.*>$', x) is not None


def isterminal(x):
    return isinstance(x, str) and not isnonterminal(x)


def read_grammar(filepath):
    
    grammar = []
    current_lhs = None
    
    def make_rule(lhs, rhs):
        if not isnonterminal(lhs):
            raise Exception(f'LHS {lhs} is not a nonterminal')
        if not rhs:
            raise Exception('Empty RHS')
        return (lhs, rhs)
    
    def parse_rhs(lexemes):
        rules = []
        rhs = []
        for lex in lexemes:
            if lex == '|':
                rules.append(make_rule(current_lhs, rhs))
                rhs = []
            else:
                rhs.append(lex)
        rules.append(make_rule(current_lhs, rhs))
        return rules
    
    with open(filepath) as fp:
        for line in fp:
            lexemes = line.split()
            if not lexemes:
                pass
            elif len(lexemes) == 1:
                raise Exception(f'Illegal rule {line}')
            elif isnonterminal(lexemes[0]) and lexemes[1] == '->':
                current_lhs = lexemes[0]
                grammar.extend(parse_rhs(lexemes[2:]))
            elif lexemes[0] == '|':
                grammar.extend(parse_rhs(lexemes[1:]))
            else:
                raise Exception(f'Illegal rule {line}')
    
    return grammar


def print_grammar(grammar):
    for rule in grammar:
        print(f'{rule[0]} -> {" ".join(rule[1])}')


def main():
    
    filepath = sys.argv[1]
    
    if not os.path.isfile(filepath):
        raise Exception(f'File path {filepath} does not exist.')
    
    print(f'Reading grammar from {filepath}')
    grammar = read_grammar(filepath)
    print(grammar)
    print_grammar(grammar)


if __name__ == '__main__':
    main()
