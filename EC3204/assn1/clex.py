#!/usr/bin/python3
import sys

# Definitions of kinds of tokens in C
WHITE_SPACE, \
COMMENT, \
IDENTIFIER, \
KW_AUTO, KW_DOUBLE, KW_INT, KW_STRUCT, \
KW_BREAK, KW_ELSE, KW_LONG, KW_SWITCH, \
KW_CASE, KW_ENUM, KW_REGISTER, KW_TYPEDEF, \
KW_CHAR, KW_EXTERN, KW_RETURN, KW_UNION, \
KW_CONST, KW_FLOAT, KW_SHORT, KW_UNSIGNED, \
KW_CONTINUE, KW_FOR, KW_SIGNED, KW_VOID, \
KW_DEFAULT, KW_GOTO, KW_SIZEOF, KW_VOLATILE, \
KW_DO, KW_IF, KW_STATIC, KW_WHILE, \
OS_COMMA, OS_SEMICOLON, OS_OPEN_BRACE, OS_CLOSE_BRACE, OS_COLON,  \
OS_OPEN_SQUARE, OS_CLOSE_SQUARE, OS_OPEN_PAREN, OS_CLOSE_PAREN, \
OS_PLUS_EQ, OS_MINUS_EQ, OS_MULT_EQ, OS_DIV_EQ, OS_MOD_EQ,  \
OS_LSHIFT_EQ, OS_RSHIFT_EQ, OS_XOR_EQ, OS_OR_EQ, OS_AND_EQ, \
OS_PLUS, OS_MINUS, OS_MULT, OS_DIV, OS_MOD,  \
OS_LSHIFT, OS_RSHIFT, OS_XOR, OS_OR, OS_AND, \
OS_NOT, OS_AND_AND, OS_OR_OR, OS_EQ, \
OS_EQ_EQ, \
OS_NOT_EQ, OS_GREATER, OS_LESS, OS_LESS_EQ, OS_GREATER_EQ, \
OS_COMPL, OS_DOT, OS_DEREF, OS_PLUS_PLUS, OS_MINUS_MINUS, \
OS_QUERY, \
OS_ELLIPSIS, \
CONSTANT_INT, \
CONSTANT_CHAR, \
STRING_LITERAL, \
CONSTANT_FLOATING, \
EOF = range(86)

KEYWORDS = {
    'auto': KW_AUTO,
    'double': KW_DOUBLE,
    'int': KW_INT,
    'struct': KW_STRUCT,
    'break': KW_BREAK,
    'else': KW_ELSE,
    'long': KW_LONG,
    'switch': KW_SWITCH,
    'case': KW_CASE,
    'enum': KW_ENUM,
    'register': KW_REGISTER,
    'typedef': KW_TYPEDEF,
    'char': KW_CHAR,
    'extern': KW_EXTERN,
    'return': KW_RETURN,
    'union': KW_UNION,
    'const': KW_CONST,
    'float': KW_FLOAT,
    'short': KW_SHORT,
    'unsigned': KW_UNSIGNED,
    'continue': KW_CONTINUE,
    'for': KW_FOR,
    'signed': KW_SIGNED,
    'void': KW_VOID,
    'default': KW_DEFAULT,
    'goto': KW_GOTO,
    'sizeof': KW_SIZEOF,
    'volatile': KW_VOLATILE,
    'do': KW_DO,
    'if': KW_IF,
    'static': KW_STATIC,
    'while': KW_WHILE,
}

TOKEN_STR = {
    WHITE_SPACE: 'WHITE_SPACE',
    COMMENT: 'COMMENT',
    IDENTIFIER: 'IDENTIFIER',
    KW_AUTO: 'KW_AUTO',
    KW_DOUBLE: 'KW_DOUBLE',
    KW_INT: 'KW_INT',
    KW_STRUCT: 'KW_STRUCT',
    KW_BREAK: 'KW_BREAK',
    KW_ELSE: 'KW_ELSE',
    KW_LONG: 'KW_LONG',
    KW_SWITCH: 'KW_SWITCH',
    KW_CASE: 'KW_CASE',
    KW_ENUM: 'KW_ENUM',
    KW_REGISTER: 'KW_REGISTER',
    KW_TYPEDEF: 'KW_TYPEDEF',
    KW_CHAR: 'KW_CHAR',
    KW_EXTERN: 'KW_EXTERN',
    KW_RETURN: 'KW_RETURN',
    KW_UNION: 'KW_UNION',
    KW_CONST: 'KW_CONST',
    KW_FLOAT: 'KW_FLOAT',
    KW_SHORT: 'KW_SHORT',
    KW_UNSIGNED: 'KW_UNSIGNED',
    KW_CONTINUE: 'KW_CONTINUE',
    KW_FOR: 'KW_FOR',
    KW_SIGNED: 'KW_SIGNED',
    KW_VOID: 'KW_VOID',
    KW_DEFAULT: 'KW_DEFAULT',
    KW_GOTO: 'KW_GOTO',
    KW_SIZEOF: 'KW_SIZEOF',
    KW_VOLATILE: 'KW_VOLATILE',
    KW_DO: 'KW_DO',
    KW_IF: 'KW_IF',
    KW_STATIC: 'KW_STATIC',
    KW_WHILE: 'KW_WHILE',
    OS_COMMA: 'OS_COMMA',
    OS_SEMICOLON: 'OS_SEMICOLON',
    OS_OPEN_BRACE: 'OS_OPEN_BRACE',
    OS_CLOSE_BRACE: 'OS_CLOSE_BRACE',
    OS_COLON: 'OS_COLON',
    OS_OPEN_SQUARE: 'OS_OPEN_SQUARE',
    OS_CLOSE_SQUARE: 'OS_CLOSE_SQUARE',
    OS_OPEN_PAREN: 'OS_OPEN_PAREN',
    OS_CLOSE_PAREN: 'OS_CLOSE_PAREN',
    OS_PLUS_EQ: 'OS_PLUS_EQ',
    OS_MINUS_EQ: 'OS_MINUS_EQ',
    OS_MULT_EQ: 'OS_MULT_EQ',
    OS_DIV_EQ: 'OS_DIV_EQ',
    OS_MOD_EQ: 'OS_MOD_EQ',
    OS_LSHIFT_EQ: 'OS_LSHIFT_EQ',
    OS_RSHIFT_EQ: 'OS_RSHIFT_EQ',
    OS_XOR_EQ: 'OS_XOR_EQ',
    OS_AND_EQ: 'OS_AND_EQ',
    OS_OR_EQ: 'OS_OR_EQ',
    OS_PLUS: 'OS_PLUS',
    OS_MINUS: 'OS_MINUS',
    OS_MULT: 'OS_MULT',
    OS_DIV: 'OS_DIV',
    OS_MOD: 'OS_MOD',
    OS_LSHIFT: 'OS_LSHIFT',
    OS_RSHIFT: 'OS_RSHIFT',
    OS_XOR: 'OS_XOR',
    OS_OR: 'OS_OR',
    OS_AND: 'OS_AND',
    OS_NOT: 'OS_NOT',
    OS_AND_AND: 'OS_AND_AND',
    OS_OR_OR: 'OS_OR_OR',
    OS_EQ: 'OS_EQ',
    OS_EQ_EQ: 'OS_EQ_EQ',
    OS_NOT_EQ: 'OS_NOT_EQ',
    OS_GREATER: 'OS_GREATER',
    OS_LESS: 'OS_LESS',
    OS_LESS_EQ: 'OS_LESS_EQ',
    OS_GREATER_EQ: 'OS_GREATER_EQ',
    OS_COMPL: 'OS_COMPL',
    OS_DOT: 'OS_DOT',
    OS_DEREF: 'OS_DEREF',
    OS_PLUS_PLUS: 'OS_PLUS_PLUS',
    OS_MINUS_MINUS: 'OS_MINUS_MINUS',
    OS_QUERY: 'OS_QUERY',
    OS_ELLIPSIS: 'OS_ELLIPSIS',
    CONSTANT_INT: 'CONSTANT_INT',
    CONSTANT_CHAR: 'CONSTANT_CHAR',
    STRING_LITERAL: 'STRING_LITERAL',
    CONSTANT_FLOATING: 'CONSTANT_FLOATING',
    EOF: 'EOF',
}

# Return a string representation of the kind of a token.
def token_kind_to_str(kind):
    return TOKEN_STR[kind]

# Print a line of token's content.
def print_token(p, token):
    if token[0] == EOF:
        print("%20s\n" % token_kind_to_str(token[0]), end='')
        return
    print("%20s  %3d   \"" % (token_kind_to_str(token[0]), token[2] - token[1] + 1), end= '')
    for i in range(token[1], token[2]+1):
        c=p[i]
        # see http://www.asciitable.com
        if c == '"':
            sys.stdout.write('\\"')
        elif c >= ' ' and c <= '~':
            sys.stdout.write(c),
        elif c == '\n':
            sys.stdout.write("\\n")
        elif c == '\t':
            sys.stdout.write("\\t")
        elif c == '"':
            sys.stdout.write("\\\"")
        elif c == '\\':
            sys.stdout.write("\\\\")
        elif c == '\r':
            sys.stdout.write("\\r")
        else:
            assert False, "Unreachable"
    print('"')

def new_token(kind, begin, end):
   return (kind, begin, end)

# The "main" entry point
def main(argv):
    if len(argv) <= 1:
        print("usage: clex.py [input file]")
        exit(1)
    filename=argv[1]
    with open(filename, 'r') as f:
        prog = list(f.read())
    prog.append(None)
    cur=0
    while True:
        token = get_token(prog, cur)
        print_token(prog, token)
        if token[0] == EOF:
            break
        cur = token[2] + 1

# Print error message and exit the program.
def error(message, p, index):
    print("error: %s" % message)
    print("The error begins from:")
    cur=index
    maxlen=50
    while cur < len(p) and maxlen > 0 and p[index] != None:
        sys.stdout.write(p[cur])
        cur = cur + 1
        maxlen = maxlen - 1
    sys.stdout.write('\n')
    assert False

# Complete your own scanner for C language
# Find out the ending index of the token from "begin."
# "p" is the array of the entire C program that ends with the "None" value
# "begin" is the beginning index of the token.
def get_token(p, begin):
    num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    octa = ['0', '1', '2', '3', '4', '5', '6', '7']
    hexa = ['0', '1', '2', '3', '4', '5', '6', '7' ,'8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'F']
    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numalbar = ['_', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    cur=begin
    if p[cur] == None:
        return new_token(EOF, cur, cur)
    elif p[cur] in [' ', '\t', '\n', '\v', '\f', '\r']:
        while p[cur] in [' ', '\t', '\n', '\v', '\f', '\r'] and cur < len(p):
            cur = cur + 1
        return new_token(WHITE_SPACE, begin, cur - 1)
    elif p[cur] == '/':
        cur = cur + 1
        if p[cur] == '*':
            cur = cur + 1
            while cur < len(p):
                if (cur + 1) < len(p) and p[cur] == '*' and p[cur+1] == '/':
                    return new_token(COMMENT, begin, cur + 1)
                cur = cur + 1
            error('The comment does not end with "*/"', p, begin)
        elif p[cur] == '=':
            return new_token(OS_DIV_EQ, begin, cur)
        else:
            return new_token(OS_DIV, begin, begin)

    elif p[cur] == '"':
        cur = cur + 1
        while cur < len(p):
            if (cur + 1) < len(p) and p[cur+1] == '"':
                if p[cur] == '\\' and p[cur+2] == ')':
                    return new_token(STRING_LITERAL, begin, cur+1)
                if p[cur] == '\\' and p[cur+2] != ')':
                    cur=cur+1
                    continue
                return new_token(STRING_LITERAL, begin, cur + 1)
            cur = cur + 1
        error('The string literal does not end with "', p, begin)
#String Literals

    elif p[cur] == '<':
        if p[cur+1] == '<':
            if p[cur + 2] == '=':
                return new_token(OS_LSHIFT_EQ, begin, begin+2)
            else:
                return new_token(OS_LSHIFT, begin, begin+1)
        elif p[cur+1] == '=':
            return new_token(OS_LESS_EQ, begin, begin+1)
        else:
            return new_token(OS_LESS, begin, begin)

    elif p[cur] == '>':
        if p[cur+1] == '>':
            if p[cur + 2] == '=':
                return new_token(OS_RSHIFT_EQ, begin, begin+2)
            else:
                return new_token(OS_RSHIFT, begin, begin+1)
        elif p[cur+1] == '=':
            return new_token(OS_GREATER_EQ, begin, begin+1)
        else:
            return new_token(OS_GREATER, begin, begin)

    elif p[cur] == '+':
        if p[cur+1] == '+':
            return new_token(OS_PLUS_PLUS, begin, begin+1)
        elif p[cur+1] == '=':
            return new_token(OS_PLUS_EQ, begin, begin+1)
        else:
            return new_token(OS_PLUS, begin, begin)
    elif p[cur] == '&':
        if p[cur+1] == '&':
            return new_token(OS_AND_AND, begin, begin+1)
        elif p[cur+1] == '=':
            return new_token(OS_AND_EQ, begin, begin+1)
        else:
            return new_token(OS_AND, begin, begin)
    elif p[cur] == '|':
        if p[cur+1] == '|':
            return new_token(OS_OR_OR, begin, begin+1)
        elif p[cur+1] == '=':
            return new_token(OS_OR_EQ, begin, begin+1)
        else:
            return new_token(OS_OR, begin, begin)

    elif p[cur] == '-':
        if p[cur+1] == '-':
            return new_token(OS_MINUS_MINUS, begin, begin+1)
        elif p[cur+1] == '>':
            return new_token(OS_DEREF, begin, begin+1)
        elif p[cur+1] == '=':
            return new_token(OS_MINUS_EQ, begin, begin+1)
        else:
            return new_token(OS_MINUS, begin, begin)

    elif p[cur] == '*':
        if p[cur+1] == '=':
            return new_token(OS_MULT_EQ, begin, begin+1)
        else:
            return new_token(OS_MULT, begin, begin)

    elif p[cur] == '%':
        if p[cur+1] == '=':
            return new_token(OS_MOD_EQ, begin, begin+1)
        else:
            return new_token(OS_MOD, begin, begin)
    elif p[cur] == '=':
        if p[cur+1] == '=':
            return new_token(OS_EQ_EQ, begin, begin+1)
        else:
            return new_token(OS_EQ, begin, begin)
    elif p[cur] == '!':
        if p[cur+1] == '=':
            return new_token(OS_NOT_EQ, begin, begin+1)
        else:
            return new_token(OS_NOT, begin, begin)
    elif p[cur] == '^':
        if p[cur+1] == '=':
            return new_token(OS_XOR_EQ, begin, begin+1)
        else:
            return new_token(OS_XOR, begin, begin)

    elif p[cur] == ',':
        return new_token(OS_COMMA, begin, begin)
    elif p[cur] == ';':
        return new_token(OS_SEMICOLON, begin, begin)
    elif p[cur] == '{':
        return new_token(OS_OPEN_BRACE, begin, begin)
    elif p[cur] == '}':
        return new_token(OS_CLOSE_BRACE, begin, begin)
    elif p[cur] == ':':
        return new_token(OS_COLON, begin, begin)
    elif p[cur] == '[':
        return new_token(OS_OPEN_SQUARE, begin, begin)
    elif p[cur] == ']':
        return new_token(OS_CLOSE_SQUARE, begin, begin)
    elif p[cur] == '(':
        return new_token(OS_OPEN_PAREN, begin, begin)
    elif p[cur] == ')':
        return new_token(OS_CLOSE_PAREN, begin, begin)
    elif p[cur] == '~':
        return new_token(OS_COMPL, begin, begin)

    elif p[cur] == '.':
        if p[cur+1] == '.':
            if p[cur+2] == '.':
                return new_token(OS_ELLIPSIS, begin, begin+2)
        if not(ord(p[cur+1])>47 and ord(p[cur+1])<58):
            return new_token(OS_DOT, begin, begin)
        cur = cur + 1
        while cur < len(p):
            if (cur + 1) < len(p) and ord(p[cur])>47 and ord(p[cur])<58 and not(ord(p[cur+1])>47 and ord(p[cur+1])<58):
                return new_token(CONSTANT_FLOATING, begin, cur)
            cur = cur + 1
        error('DOT is used not for both floating notation or OS', p, begin)

#Until here, OS and WS and Comments, and String Literal are processed

    if p[cur] == 'a':
        if p[cur+1] == 'u':
            if p[cur+2] == 't':
                if p[cur+3] == 'o':
                    if p[cur+4] not in numalbar:
                        return new_token(KW_AUTO, begin, begin+3)

    if p[cur] == 'd':
        if p[cur+1] == 'o':
            if p[cur+2] == 'u':
                if p[cur+3] == 'b':
                    if p[cur+4] == 'l':
                        if p[cur+5] == 'e':
                            if p[cur+6] not in numalbar:
                                return new_token(KW_DOUBLE, begin, begin+5)

    if p[cur] == 'i':
        if p[cur+1] == 'n':
            if p[cur+2] == 't':
                if p[cur+3] not in numalbar:
                    return new_token(KW_INT, begin, begin+2)

    if p[cur] == 'f':
        if p[cur+1] == 'o':
            if p[cur+2] == 'r':
                if p[cur+3] not in numalbar:
                    return new_token(KW_FOR, begin, begin+2)

    if p[cur] == 's':
        if p[cur+1] == 't':
            if p[cur+2] == 'r':
                if p[cur+3] == 'u':
                    if p[cur+4] == 'c':
                        if p[cur+5] == 't':
                            if p[cur+6] not in numalbar:
                                return new_token(KW_STRUCT, begin, begin+5)

    if p[cur] == 'b':
        if p[cur+1] == 'r':
            if p[cur+2] == 'e':
                if p[cur+3] == 'a':
                    if p[cur+4] == 'k':
                        if p[cur+5] not in numalbar:
                            return new_token(KW_BREAK, begin, begin+4)

    if p[cur] == 'u':
        if p[cur+1] == 'n':
            if p[cur+2] == 'i':
                if p[cur+3] == 'o':
                    if p[cur+4] == 'n':
                        if p[cur+5] not in numalbar:
                            return new_token(KW_UNION, begin, begin+4)

    if p[cur] == 'c':
        if p[cur+1] == 'o':
            if p[cur+2] == 'n':
                if p[cur+3] == 's':
                    if p[cur+4] == 't':
                        if p[cur+5] not in numalbar:
                            return new_token(KW_CONST, begin, begin+4)

    if p[cur] == 'f':
        if p[cur+1] == 'l':
            if p[cur+2] == 'o':
                if p[cur+3] == 'a':
                    if p[cur+4] == 't':
                        if p[cur+5] not in numalbar:
                            return new_token(KW_FLOAT, begin, begin+4)

    if p[cur] == 's':
        if p[cur+1] == 'h':
            if p[cur+2] == 'o':
                if p[cur+3] == 'r':
                    if p[cur+4] == 't':
                        if p[cur+5] not in numalbar:
                            return new_token(KW_SHORT, begin, begin+4)

    if p[cur] == 'w':
        if p[cur+1] == 'h':
            if p[cur+2] == 'i':
                if p[cur+3] == 'l':
                    if p[cur+4] == 'e':
                        if p[cur+5] not in numalbar:
                            return new_token(KW_WHILE, begin, begin+4)

    if p[cur] == 'e':
        if p[cur+1] == 'l':
            if p[cur+2] == 's':
                if p[cur+3] == 'e':
                    if p[cur+4] not in numalbar:
                        return new_token(KW_ELSE, begin, begin+3)

    if p[cur] == 'l':
        if p[cur+1] == 'o':
            if p[cur+2] == 'n':
                if p[cur+3] == 'g':
                    if p[cur+4] not in numalbar:
                        return new_token(KW_LONG, begin, begin+3)

    if p[cur] == 's':
        if p[cur+1] == 'w':
            if p[cur+2] == 'i':
                if p[cur+3] == 't':
                    if p[cur+4] == 'c':
                        if p[cur+5] == 'h':
                            if p[cur+6] not in numalbar:
                                return new_token(KW_SWITCH, begin, begin+5)

    if p[cur] == 'e':
        if p[cur+1] == 'x':
            if p[cur+2] == 't':
                if p[cur+3] == 'e':
                    if p[cur+4] == 'r':
                        if p[cur+5] == 'n':
                            if p[cur+6] not in numalbar:
                                return new_token(KW_EXTERN, begin, begin+5)

    if p[cur] == 's':
        if p[cur+1] == 'i':
            if p[cur+2] == 'g':
                if p[cur+3] == 'n':
                    if p[cur+4] == 'e':
                        if p[cur+5] == 'd':
                            if p[cur+6] not in numalbar:
                                return new_token(KW_SIGNED, begin, begin+5)

    if p[cur] == 'r':
        if p[cur+1] == 'e':
            if p[cur+2] == 't':
                if p[cur+3] == 'u':
                    if p[cur+4] == 'r':
                        if p[cur+5] == 'n':
                            if p[cur+6] not in numalbar:
                                return new_token(KW_RETURN, begin, begin+5)

    if p[cur] == 's':
        if p[cur+1] == 'i':
            if p[cur+2] == 'z':
                if p[cur+3] == 'e':
                    if p[cur+4] == 'o':
                        if p[cur+5] == 'f':
                            if p[cur+6] not in numalbar:
                                return new_token(KW_SIZEOF, begin, begin+5)

    if p[cur] == 's':
        if p[cur+1] == 't':
            if p[cur+2] == 'a':
                if p[cur+3] == 't':
                    if p[cur+4] == 'i':
                        if p[cur+5] == 'c':
                            if p[cur+6] not in numalbar:
                                return new_token(KW_STATIC, begin, begin+5)

    if p[cur] == 't':
        if p[cur+1] == 'y':
            if p[cur+2] == 'p':
                if p[cur+3] == 'e':
                    if p[cur+4] == 'd':
                        if p[cur+5] == 'e':
                            if p[cur+6] == 'f':
                                if p[cur+7] not in numalbar:
                                    return new_token(KW_TYPEDEF, begin, begin+6)

    if p[cur] == 'd':
        if p[cur+1] == 'e':
            if p[cur+2] == 'f':
                if p[cur+3] == 'a':
                    if p[cur+4] == 'u':
                        if p[cur+5] == 'l':
                            if p[cur+6] == 't':
                                if p[cur+7] not in numalbar:
                                    return new_token(KW_DEFAULT, begin, begin+6)

    if p[cur] == 'r':
        if p[cur+1] == 'e':
            if p[cur+2] == 'g':
                if p[cur+3] == 'i':
                    if p[cur+4] == 's':
                        if p[cur+5] == 't':
                            if p[cur+6] == 'e':
                                if p[cur+7] == 'r':
                                    if p[cur+8] not in numalbar:
                                        return new_token(KW_REGISTER, begin, begin+7)

    if p[cur] == 'u':
        if p[cur+1] == 'n':
            if p[cur+2] == 's':
                if p[cur+3] == 'i':
                    if p[cur+4] == 'g':
                        if p[cur+5] == 'n':
                            if p[cur+6] == 'e':
                                if p[cur+7] == 'd':
                                    if p[cur+8] not in numalbar:
                                        return new_token(KW_UNSIGNED, begin, begin+7)

    if p[cur] == 'c':
        if p[cur+1] == 'o':
            if p[cur+2] == 'n':
                if p[cur+3] == 't':
                    if p[cur+4] == 'i':
                        if p[cur+5] == 'n':
                            if p[cur+6] == 'u':
                                if p[cur+7] == 'e':
                                    if p[cur+8] not in numalbar:
                                        return new_token(KW_CONTINUE, begin, begin+7)

    if p[cur] == 'v':
        if p[cur+1] == 'o':
            if p[cur+2] == 'l':
                if p[cur+3] == 'a':
                    if p[cur+4] == 't':
                        if p[cur+5] == 'i':
                            if p[cur+6] == 'l':
                                if p[cur+7] == 'e':
                                    if p[cur+8] not in numalbar:
                                        return new_token(KW_VOLATILE, begin, begin+7)

    if p[cur] == 'c':
        if p[cur+1] == 'a':
            if p[cur+2] == 's':
                if p[cur+3] == 'e':
                    if p[cur+4] not in numalbar:
                        return new_token(KW_CASE, begin, begin+3)

    if p[cur] == 'e':
        if p[cur+1] == 'n':
            if p[cur+2] == 'u':
                if p[cur+3] == 'm':
                    if p[cur+4] not in numalbar:
                        return new_token(KW_ENUM, begin, begin+3)

    if p[cur] == 'c':
        if p[cur+1] == 'h':
            if p[cur+2] == 'a':
                if p[cur+3] == 'r':
                    if p[cur+4] not in numalbar:
                        return new_token(KW_CHAR, begin, begin+3)

    if p[cur] == 'v':
        if p[cur+1] == 'o':
            if p[cur+2] == 'i':
                if p[cur+3] == 'd':
                    if p[cur+4] not in numalbar:
                        return new_token(KW_VOID, begin, begin+3)

    if p[cur] == 'g':
        if p[cur+1] == 'o':
            if p[cur+2] == 't':
                if p[cur+3] == 'o':
                    if p[cur+4] not in numalbar:
                        return new_token(KW_GOTO, begin, begin+3)

    if p[cur] == 'd':
        if p[cur+1] == 'o':
            if p[cur+2] not in numalbar:
                return new_token(KW_DO, begin, begin+1)

    if p[cur] == 'i':
        if p[cur+1] == 'f':
            if p[cur+2] not in numalbar:
                return new_token(KW_IF, begin, begin+1)

    if p[cur] in alpha:
        while cur < len(p):
            if ((cur + 1) < len(p)) and (p[cur+1] in numalbar):
                cur = cur + 1
            else:
                return new_token(IDENTIFIER, begin, cur)

    if p[cur] in num:
        float_switch=False
        if p[cur] == '0' and p[cur] != 'x': #8
            cur = cur + 1
            while cur < len(p):
                if p[cur]=='.':
                    float_switch=True
                if ((cur+1)<len(p)) and (p[cur+1] in octa):
                    cur = cur + 1
                else:
                    if float_switch==True:
                        return new_token(CONSTANT_FLOATING, begin, cur-1)
                    else:
                        return new_token(CONSTANT_INT, begin, cur-1)
        if p[cur] == '0' and p[cur] == 'x': #16
            cur = cur + 1
            while cur < len(p):
                if p[cur] == '.':
                    cur=cur+1
                    float_switch=True
                if (cur<len(p)) and p[cur] in hexa:
                    cur = cur + 1
                else:
                    if float_switch==True:
                        return new_token(CONSTANT_FLOATING, begin, cur-1)
                    else:
                        return new_token(CONSTANT_INT, begin, cur-1)

        if p[cur] != '0': #10
            cur=cur+1
            while cur < len(p):
                if p[cur] == '.':
                    cur=cur+1
                    float_switch=True
                if cur<len(p) and p[cur] in num:
                    cur=cur+1
                else:
                    if float_switch==True:
                        return new_token(CONSTANT_FLOATING, begin, cur-1)
                    else:
                        return new_token(CONSTANT_INT, begin, cur-1)
#identifier
    if p[cur] == "'":
        if p[cur+2] == "'":
            return new_token(CONSTANT_CHAR, begin, cur+2)
        elif p[cur+3] == "'":
            if p[cur+1] == '\\':
                return new_token(CONSTANT_CHAR, begin, cur+3)
            else:
                error("Too long", p, cur)
        else:
            error("close of char does not exist", p, cur)

    else:
        error("not implemented", p, cur)

# execute the main routine
main(sys.argv)
