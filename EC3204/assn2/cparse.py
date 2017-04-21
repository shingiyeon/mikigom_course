#!/usr/bin/python3

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

# Token sequences from gcd.c
TOKENS = [
  (              KW_INT,   54,   56, 'int'),
  (          IDENTIFIER,   58,   61, 'main'),
  (       OS_OPEN_PAREN,   62,   62, '('),
  (      OS_CLOSE_PAREN,   63,   63, ')'),
  (       OS_OPEN_BRACE,   65,   65, '{'),
  (              KW_INT,   71,   73, 'int'),
  (          IDENTIFIER,   75,   76, 'g1'),
  (        OS_SEMICOLON,   77,   77, ';'),
  (              KW_INT,   83,   85, 'int'),
  (          IDENTIFIER,   87,   88, 'g2'),
  (        OS_SEMICOLON,   89,   89, ';'),
  (          IDENTIFIER,   96,   97, 'g1'),
  (               OS_EQ,   99,   99, '='),
  (          IDENTIFIER,  101,  103, 'gcd'),
  (       OS_OPEN_PAREN,  104,  104, '('),
  (        CONSTANT_INT,  105,  106, '81'),
  (            OS_COMMA,  107,  107, ','),
  (        CONSTANT_INT,  109,  111, '625'),
  (      OS_CLOSE_PAREN,  112,  112, ')'),
  (        OS_SEMICOLON,  113,  113, ';'),
  (          IDENTIFIER,  119,  120, 'g2'),
  (               OS_EQ,  122,  122, '='),
  (          IDENTIFIER,  124,  127, 'rgcd'),
  (       OS_OPEN_PAREN,  128,  128, '('),
  (        CONSTANT_INT,  129,  131, '815'),
  (            OS_COMMA,  132,  132, ','),
  (        CONSTANT_INT,  134,  136, '625'),
  (      OS_CLOSE_PAREN,  137,  137, ')'),
  (        OS_SEMICOLON,  138,  138, ';'),
  (           KW_RETURN,  149,  154, 'return'),
  (          IDENTIFIER,  156,  157, 'g1'),
  (            OS_EQ_EQ,  159,  160, '=='),
  (          IDENTIFIER,  162,  163, 'g2'),
  (        OS_SEMICOLON,  164,  164, ';'),
  (      OS_CLOSE_BRACE,  166,  166, '}'),
  (              KW_INT,  169,  171, 'int'),
  (          IDENTIFIER,  173,  175, 'gcd'),
  (       OS_OPEN_PAREN,  176,  176, '('),
  (              KW_INT,  177,  179, 'int'),
  (          IDENTIFIER,  181,  181, 'a'),
  (            OS_COMMA,  182,  182, ','),
  (              KW_INT,  184,  186, 'int'),
  (          IDENTIFIER,  188,  188, 'b'),
  (      OS_CLOSE_PAREN,  189,  189, ')'),
  (       OS_OPEN_BRACE,  191,  191, '{'),
  (            KW_WHILE,  197,  201, 'while'),
  (       OS_OPEN_PAREN,  203,  203, '('),
  (          IDENTIFIER,  204,  204, 'a'),
  (           OS_NOT_EQ,  206,  207, '!='),
  (          IDENTIFIER,  209,  209, 'b'),
  (      OS_CLOSE_PAREN,  210,  210, ')'),
  (       OS_OPEN_BRACE,  212,  212, '{'),
  (               KW_IF,  222,  223, 'if'),
  (       OS_OPEN_PAREN,  225,  225, '('),
  (          IDENTIFIER,  226,  226, 'a'),
  (          OS_GREATER,  228,  228, '>'),
  (          IDENTIFIER,  230,  230, 'b'),
  (      OS_CLOSE_PAREN,  231,  231, ')'),
  (          IDENTIFIER,  246,  246, 'a'),
  (               OS_EQ,  248,  248, '='),
  (          IDENTIFIER,  250,  250, 'a'),
  (            OS_MINUS,  252,  252, '-'),
  (          IDENTIFIER,  254,  254, 'b'),
  (        OS_SEMICOLON,  255,  255, ';'),
  (             KW_ELSE,  265,  268, 'else'),
  (          IDENTIFIER,  282,  282, 'b'),
  (               OS_EQ,  284,  284, '='),
  (          IDENTIFIER,  286,  286, 'b'),
  (            OS_MINUS,  288,  288, '-'),
  (          IDENTIFIER,  290,  290, 'a'),
  (        OS_SEMICOLON,  291,  291, ';'),
  (      OS_CLOSE_BRACE,  297,  297, '}'),
  (           KW_RETURN,  303,  308, 'return'),
  (          IDENTIFIER,  310,  310, 'a'),
  (        OS_SEMICOLON,  311,  311, ';'),
  (      OS_CLOSE_BRACE,  313,  313, '}'),
  (              KW_INT,  316,  318, 'int'),
  (          IDENTIFIER,  320,  323, 'rgcd'),
  (       OS_OPEN_PAREN,  324,  324, '('),
  (              KW_INT,  325,  327, 'int'),
  (          IDENTIFIER,  329,  329, 'a'),
  (            OS_COMMA,  330,  330, ','),
  (              KW_INT,  332,  334, 'int'),
  (          IDENTIFIER,  336,  336, 'b'),
  (      OS_CLOSE_PAREN,  337,  337, ')'),
  (       OS_OPEN_BRACE,  339,  339, '{'),
  (               KW_IF,  345,  346, 'if'),
  (       OS_OPEN_PAREN,  348,  348, '('),
  (          IDENTIFIER,  350,  350, 'a'),
  (            OS_EQ_EQ,  352,  353, '=='),
  (          IDENTIFIER,  355,  355, 'b'),
  (      OS_CLOSE_PAREN,  357,  357, ')'),
  (       OS_OPEN_BRACE,  359,  359, '{'),
  (           KW_RETURN,  369,  374, 'return'),
  (          IDENTIFIER,  376,  376, 'a'),
  (        OS_SEMICOLON,  377,  377, ';'),
  (      OS_CLOSE_BRACE,  383,  383, '}'),
  (             KW_ELSE,  385,  388, 'else'),
  (               KW_IF,  390,  391, 'if'),
  (       OS_OPEN_PAREN,  393,  393, '('),
  (          IDENTIFIER,  395,  395, 'a'),
  (          OS_GREATER,  397,  397, '>'),
  (          IDENTIFIER,  399,  399, 'b'),
  (      OS_CLOSE_PAREN,  401,  401, ')'),
  (       OS_OPEN_BRACE,  403,  403, '{'),
  (           KW_RETURN,  413,  418, 'return'),
  (          IDENTIFIER,  420,  423, 'rgcd'),
  (       OS_OPEN_PAREN,  424,  424, '('),
  (          IDENTIFIER,  425,  425, 'a'),
  (            OS_MINUS,  427,  427, '-'),
  (          IDENTIFIER,  429,  429, 'b'),
  (            OS_COMMA,  430,  430, ','),
  (          IDENTIFIER,  432,  432, 'b'),
  (      OS_CLOSE_PAREN,  433,  433, ')'),
  (        OS_SEMICOLON,  434,  434, ';'),
  (      OS_CLOSE_BRACE,  440,  440, '}'),
  (             KW_ELSE,  442,  445, 'else'),
  (       OS_OPEN_BRACE,  447,  447, '{'),
  (           KW_RETURN,  457,  462, 'return'),
  (          IDENTIFIER,  464,  467, 'rgcd'),
  (       OS_OPEN_PAREN,  468,  468, '('),
  (          IDENTIFIER,  469,  469, 'a'),
  (            OS_COMMA,  470,  470, ','),
  (          IDENTIFIER,  472,  472, 'b'),
  (            OS_MINUS,  474,  474, '-'),
  (          IDENTIFIER,  476,  476, 'a'),
  (      OS_CLOSE_PAREN,  477,  477, ')'),
  (        OS_SEMICOLON,  478,  478, ';'),
  (      OS_CLOSE_BRACE,  484,  484, '}'),
  (      OS_CLOSE_BRACE,  486,  486, '}'),
  (EOF, None, None, None),
]

# Definitions for abstract syntax trees.

# Nodes types.
CAST_TRANSLATION_UNIT,\
CAST_FUN_DEFINITION,\
CAST_PAR_TYPE_LIST,\
CAST_PAR_TYPE,\
CAST_VAR_DECLARATION,\
CAST_IF_STMT,\
CAST_WHILE_STMT,\
CAST_RETURN_STMT,\
CAST_COMP_STMT,\
CAST_DECL_LIST, \
CAST_STMT_LIST, \
CAST_EXPR_STMT,\
CAST_EQ_EXPR, \
CAST_NOT_EQ_EXPR, \
CAST_LESS_EXPR, \
CAST_GREATER_EXPR,\
CAST_LESS_EQ_EXPR,\
CAST_GREATER_EQ_EXPR,\
CAST_PLUS_EXPR,\
CAST_MINUS_EXPR,\
CAST_MUL_EXPR,\
CAST_DIV_EXPR,\
CAST_MOD_EXPR,\
CAST_VAR_EXPR,\
CAST_CALL_EXPR,\
CAST_INT_CONST_EXPR,\
CAST_ARG_LIST,\
= range(27)

# String representations of node types.
CAST_NODE_STR={
  CAST_TRANSLATION_UNIT: "CAST_TRANSLATION_UNIT", #0
  CAST_FUN_DEFINITION: "CAST_FUN_DEFINITION", #1
  CAST_PAR_TYPE_LIST: "CAST_PAR_TYPE_LIST", #2
  CAST_PAR_TYPE: "CAST_PAR_TYPE", #3
  CAST_VAR_DECLARATION: "CAST_VAR_DECLARATION", #4
  CAST_IF_STMT: "CAST_IF_STMT", #5
  CAST_WHILE_STMT: "CAST_WHILE_STMT", #6
  CAST_RETURN_STMT: "CAST_RETURN_STMT", #7
  CAST_COMP_STMT: "CAST_COMP_STMT", #8
  CAST_DECL_LIST : "CAST_DECL_LIST", #9
  CAST_STMT_LIST : "CAST_STMT_LIST", #10
  CAST_EXPR_STMT: "CAST_EXPR_STMT", #11
  CAST_EQ_EXPR : "CAST_EQ_EXPR", #12
  CAST_NOT_EQ_EXPR : "CAST_NOT_EQ_EXPR", #13
  CAST_LESS_EXPR : "CAST_LESS_EXPR", #14
  CAST_GREATER_EXPR: "CAST_GREATER_EXPR", #15
  CAST_LESS_EQ_EXPR: "CAST_LESS_EQ_EXPR", #16
  CAST_GREATER_EQ_EXPR: "CAST_GREATER_EQ_EXPR", #17
  CAST_PLUS_EXPR: "CAST_PLUS_EXPR", #18
  CAST_MINUS_EXPR: "CAST_MINUS_EXPR", #19
  CAST_MUL_EXPR: "CAST_MUL_EXPR", #20
  CAST_DIV_EXPR: "CAST_DIV_EXPR", #21
  CAST_MOD_EXPR: "CAST_MOD_EXPR", #22
  CAST_VAR_EXPR: "CAST_VAR_EXPR", #23
  CAST_CALL_EXPR: "CAST_CALL_EXPR", #24
  CAST_INT_CONST_EXPR: "CAST_INT_CONST_EXPR", #25
  CAST_ARG_LIST: "CAST_ARG_LIST", #26
}

# Helper routines for abstract syntax trees.
def cast_new_node(nkind):
    return [nkind, {} ]

def cast_set_attribute(n, aname, value):
    n[1][aname]=value

def cast_get_attribute(n, aname):
    return n[1][aname]

def cast_get_child(n, i):
    return n[2+i]

def cast_get_children(n):
    return n[2:]

# A set of routines for constructing an abstract syntax tree.
def cast_translation_unit(l):
    n=cast_new_node(CAST_TRANSLATION_UNIT)
    return n + l

def cast_function_definition(func_name, par_types, comp_stmt):
    if par_types == None:
        n = cast_new_node(CAST_FUN_DEFINITION) + [cast_new_node(CAST_PAR_TYPE_LIST), comp_stmt]
    else:
        n = cast_new_node(CAST_FUN_DEFINITION) + [ par_types, comp_stmt]
    cast_set_attribute(n, 'id', func_name)
    return n
    
def cast_param_types(param_type_list):
    if param_type_list == None:
        return [CAST_PAR_TYPE_LIST, {} ]
    else:
        return cast_new_node(CAST_PAR_TYPE_LIST) + param_type_list

def cast_par_type(pname):
    n=cast_new_node(CAST_PAR_TYPE)
    cast_set_attribute(n, 'id', pname)
    return n

def cast_comp_stmt(dl, sl):
    return cast_new_node(CAST_COMP_STMT) + [ dl, sl]

def cast_decl_list(l):
    if l == [None]:
        return cast_new_node(CAST_DECL_LIST)
    else:
        return cast_new_node(CAST_DECL_LIST) + l

def cast_var_decl(vname):
    n = cast_new_node(CAST_VAR_DECLARATION)
    cast_set_attribute(n, 'id', vname)
    return n

def cast_stmt_list(l):
    if l == [None]:
        return cast_new_node(CAST_STMT_LIST)
    else:
        return cast_new_node(CAST_STMT_LIST) + l

def cast_while_stmt(cond, stmt):
    return cast_new_node(CAST_WHILE_STMT) + [ cond, stmt]

def cast_if_stmt(cond, true_stmt, false_stmt=None):
    if false_stmt == None:
        return cast_new_node(CAST_IF_STMT) + [cond, true_stmt]
    else:
        return cast_new_node(CAST_IF_STMT) + [cond, true_stmt, false_stmt]

def cast_return_stmt(e):
    return cast_new_node(CAST_RETURN_STMT) + [ e]

def cast_expr_stmt(v, e):
    n = cast_new_node(CAST_EXPR_STMT) + [ e]
    cast_set_attribute(n, 'id', v)
    return n

def cast_bin_expr(opcode, op1, op2):
    if opcode == OS_EQ_EQ:
        opcode = CAST_EQ_EXPR
    elif opcode == OS_NOT_EQ:
        opcode = CAST_NOT_EQ_EXPR
    elif opcode == OS_LESS:
        opcode = CAST_LESS_EXPR
    elif opcode == OS_GREATER:
        opcode = CAST_GREATER_EXPR
    elif opcode == OS_LESS_EQ:
        opcode = CAST_LESS_EQ_EXPR
    elif opcode == OS_GREATER_EQ:
        opcode = CAST_GREATER_EQ_EXPR
    elif opcode == OS_PLUS:
        opcode = CAST_PLUS_EXPR
    elif opcode == OS_MINUS:
        opcode = CAST_MINUS_EXPR
    elif opcode == OS_MUL:
        opcode = CAST_MUL_EXPR
    elif opcode == OS_DIV:
        opcode = CAST_DIV_EXPR
    elif opcode == OS_MOD:
        opcode = CAST_MOD_EXPR
    return cast_new_node(opcode) + [ op1, op2]

def cast_var_expr(vname):
    n = cast_new_node(CAST_VAR_EXPR)
    cast_set_attribute(n, 'id', vname)
    return n

def cast_int_constant_expr(i):
    n = cast_new_node(CAST_INT_CONST_EXPR) 
    cast_set_attribute(n, 'value', i)    
    return n

def cast_call_expr(fname, arg_list):
    n = cast_new_node(CAST_CALL_EXPR) + arg_list
    cast_set_attribute(n, 'fname', fname)
    return n

def cast_argument_list(arg_list):
    return cast_new_node(CAST_ARG_LIST) + arg_list

# Dump an abstract syntax tree into its list representation in Python.
def cast_dump(r):
    s={'depth':-1}
    def depth(): 
        return s['depth']
    def enter(): 
        s['depth'] += 1
    def leave(): 
        s['depth'] -= 1
    def tab():
        s = ""
        for i in range(depth()): 
            s = s + "  "
        return s
    def visit(n):
        enter()
        t=n[0]
        tname = CAST_NODE_STR[t]
        attrs=[]
        for aname in n[1]:
            value=n[1][aname]
            if isinstance(value, str):
                val_str='"%s"' % value
            elif isinstance(value, int):
                val_str='%d' % value
            else:
                assert False, "Unsupported attribute type: %s" % type(value)
            attrs.append("'%s': %s" % (aname, val_str))
        attrs=', '.join(attrs)
        children=n[2:]
        print("%s[%s, {%s}" % (tab(), tname, attrs), end='' if len(children) == 0 else ',\n')
        for c in n[2:]:
            visit(c)
        if len(children) == 0:
            print("],")
        else:
            if n == r:
                print("%s]" % (tab()))
            else:
                print("%s]," % (tab()))
        leave()
    print("AST= \\")
    visit(r)

# Global variables.
tokens=None
current_index=0
source_file=None
line_map=None

def la():
    global tokens, current_index
    return tokens[current_index][0]

def law():
    global tokens, current_index
    return tokens[current_index][3]

def match(tok):
    global tokens, current_index
    if la() != tok:
        error("'%s' is expected, but '%s' appears" %
              (token_kind_to_str(tok), token_kind_to_str(lookahead())))
    current_index = current_index + 1
    return tokens[current_index-1]

def lexam(token):
    return token[3]

def source_location(pos):
    global line_map
    for i in range(len(line_map)):
        if pos >= line_map[i][0] and pos < line_map[i+1][0]:
            sline = line_map[i][1]
            col = pos - line_map[i][0] + 1
            return (sline, col)

def error(msg='No alternative'):
    global source_file, tokens, current_index
    line,col=source_location(tokens[current_index][1])
    print("%s:%d:%d: error: %s" % (source_file, line, col, msg))
    if True:
        assert False
    exit(1)

def main():
    ast=parse()
    cast_dump(ast)

def prepare():
    global source_file, tokens, current_index, line_map
    source_file='gcd.c'
    current_index=0
    tokens=TOKENS
    # Construct a line map to map a character position into a line number.
    with open(source_file, 'r') as f:
        prog = list(f.read())
    prog.append(None)
    line_map=[(0,1)]
    for pos in range(len(prog)):
        if prog[pos] == '\n':
            line_map.append( (pos + 1, line_map[-1][1] + 1))
        elif prog[pos] == None:
            line_map.append( (pos, line_map[-1][1] + 1))

def err():
    assert False, 'to be implemented'

# A set of routines for the recursive descent parser.
def parse():
    prepare()
    ptr = None
    rhs = None

    if la() in [KW_INT]:
        rhs=translation_unit()
        ptr = cast_translation_unit(rhs)
        match(EOF)
    else:
        err()

    return ptr

def translation_unit():
    ptr = None
    rhs = None

    if la() in [KW_INT]:
        ptr = external_declaration()
        while True:
            if la() in [KW_INT]:
                rhs = translation_unit()
            elif la() in [EOF]:
                break
            else:
                err()
    else:
        err()

    if rhs != None:
        return ptr + rhs
    else:
        return ptr

def external_declaration():
    ptr = None

    if la() in [KW_INT]:
        ptr = function_definition()
    else:
        err()

    return ptr

def function_definition():
    ptr = None
    p = None
    c = None

    if la() in [KW_INT]:
        match(KW_INT)
        func_name = law()
        match(IDENTIFIER)
        match(OS_OPEN_PAREN)
        p = parameter_type_list_opt()
        match(OS_CLOSE_PAREN)
        c = compound_statement()
        ptr = cast_function_definition(func_name, p, c)
    else:
        err()

    return [ptr]

def parameter_type_list_opt():
    ptr = None
    rhs = None

    if la() in [KW_INT]:
        rhs = parameter_type_list()
        ptr = cast_param_types(rhs)
    elif la() in [OS_CLOSE_PAREN]:
        pass
    else:
        err()

    return ptr

def parameter_type_list():
    ptr = None
    rhs = None

    if la() in [KW_INT]:
        ptr = parameter_type()
        while True:
            if la() in [OS_COMMA]:
                match(OS_COMMA)
                rhs = parameter_type()
            elif la() in [OS_CLOSE_PAREN]:
                break
            else:
                err()
    else:
        err()

    return [ptr] + [rhs]

def parameter_type():
    ptr = None

    if la() in [KW_INT]:
        match(KW_INT)
        pname = law()
        match(IDENTIFIER)
        ptr = cast_par_type(pname)
    else:
        err()

    return ptr

def compound_statement():
    ptr = None
    dl = None
    sl = None

    if la() in [OS_OPEN_BRACE]:
        match(OS_OPEN_BRACE)
        dl = declaration_list_opt()
        sl = statement_list_opt()
        ptr = cast_comp_stmt(dl, sl)
        match(OS_CLOSE_BRACE)
    else:
        err()

    return ptr

def declaration_list_opt():
    ptr = None
    l = None

    if la() in [KW_INT]:
        ptr = declaration()
        while True:
            if la() in [KW_INT]:
                l = declaration()
            elif la() in [KW_WHILE, KW_IF, IDENTIFIER, CONSTANT_INT, OS_OPEN_PAREN, KW_RETURN, OS_OPEN_BRACE]:
                break
            else:
                error()
    elif la() in [KW_WHILE, KW_IF, IDENTIFIER, CONSTANT_INT, OS_OPEN_PAREN, KW_RETURN, OS_OPEN_BRACE]:
        pass
    else:
        err()

    if l != None:
        return cast_decl_list([ptr]+[l])
    else:
        return cast_decl_list([ptr])

def statement_list_opt():
    ptr = None
    l = None
    k = None

    if la() in [KW_WHILE, KW_IF, IDENTIFIER, CONSTANT_INT, OS_OPEN_PAREN, KW_RETURN, OS_OPEN_BRACE]:
        ptr = statement()
        while True:
            if la() in [KW_WHILE, KW_IF, IDENTIFIER, CONSTANT_INT, OS_OPEN_PAREN, KW_RETURN, OS_OPEN_BRACE]:
                l = statement()
                while True:
                    if la() in [KW_WHILE, KW_IF, IDENTIFIER, CONSTANT_INT, OS_OPEN_PAREN, KW_RETURN, OS_OPEN_BRACE]:
                        k = statement()
                    elif la() in [OS_CLOSE_BRACE]:
                        break
                    else:
                        err()
            elif la() in [OS_CLOSE_BRACE]:
                break
            else:
                err()
    else:
        err()

    if k != None:
        return cast_stmt_list([ptr]+[l]+[k])
    elif l != None:
        return cast_stmt_list([ptr]+[l])
    else:
        return cast_stmt_list([ptr])

def declaration():
    ptr = None

    if la() in [KW_INT]:
        match(KW_INT)
        vname = law()
        match(IDENTIFIER)
        match(OS_SEMICOLON)
        ptr = cast_var_decl(vname)
    else:
        err()

    return ptr

def statement():
    ptr = None

    if la() in [KW_WHILE]:
        ptr = iteration_statement()
    elif la() in [KW_IF]:
        ptr = selection_statement()
    elif la() in [IDENTIFIER, OS_SEMICOLON]:
        ptr = expression_statement()
    elif la() in [KW_RETURN]:
        ptr = jump_statement()
    elif la() in [OS_OPEN_BRACE]:
        ptr = compound_statement()
    else:
        err()

    return ptr

def iteration_statement():
    ptr = None
    cond = None
    stmt = None

    if la() in [KW_WHILE]:
        match(KW_WHILE)
        match(OS_OPEN_PAREN)
        cond = expression()
        match(OS_CLOSE_PAREN)
        stmt = statement()
        ptr = cast_while_stmt(cond, stmt)
    else:
        err()

    return ptr

def selection_statement():
    ptr = None
    cond = None
    true_stmt = None
    false_stmt = None

    if la() in [KW_IF]:
        match(KW_IF)
        match(OS_OPEN_PAREN)
        cond = expression()
        match(OS_CLOSE_PAREN)
        true_stmt = statement()
        if la() in [KW_ELSE]:
            match(KW_ELSE)
            false_stmt = statement()
            ptr = cast_if_stmt(cond, true_stmt, false_stmt)
        elif la() in [OS_CLOSE_BRACE]:
            ptr = cast_if_stmt(cond, true_stmt, false_stmt)
        else:
            err()
    else:
        err()

    return ptr

def expression_statement():
    ptr = None
    v = None
    e = None

    if la() in [IDENTIFIER]:
        v = law()
        match(IDENTIFIER)
        match(OS_EQ)
        e = expression()
        ptr = cast_expr_stmt(v, e)
        match(OS_SEMICOLON)
    elif la() in [OS_SEMICOLON]:
        match(OS_SEMICOLON)
    else:
        err()

    return ptr

def jump_statement():
    ptr = None
    e = None

    if la() in [KW_RETURN]:
        match(KW_RETURN)
        if la() in [IDENTIFIER, CONSTANT_INT, OS_OPEN_PAREN]:
            e = expression()
            ptr = cast_return_stmt(e)
            match(OS_SEMICOLON)
        elif la() in [OS_SEMICOLON]:
            ptr = cast_return_stmt(e)
        else:
            err()
    else:
        err()

    return ptr

def expression():
    ptr = None

    if la() in [IDENTIFIER, CONSTANT_INT, OS_OPEN_PAREN]:
        ptr = equality_expression()
    else:
        err()

    return ptr

def equality_expression():
    ptr = None
    op1 = None
    op2 = None

    if la() in [IDENTIFIER, CONSTANT_INT, OS_OPEN_PAREN]:
        ptr = relational_expression()
        while True:
            if la() in [OS_EQ_EQ]:
                op1 = ptr
                match(OS_EQ_EQ)
                op2 = relational_expression()
                ptr = cast_bin_expr(OS_EQ_EQ, op1, op2)
            elif la() in [OS_NOT_EQ]:
                op1 = ptr 
                match(OS_NOT_EQ)
                op2 = relational_expression()
                ptr = cast_bin_expr(OS_NOT_EQ, op1, op2)
            elif la() in [OS_SEMICOLON, OS_CLOSE_PAREN, OS_COMMA]:
                break
    else:
        err()

    return ptr

def relational_expression():
    ptr = None
    op1 = None
    op2 = None

    if la() in [IDENTIFIER, CONSTANT_INT, OS_OPEN_PAREN]:
        ptr = additive_expression()
        while True:
            if la() in [OS_LESS]:
                op1 = ptr
                match(OS_LESS)
                op2 = additive_expression()
                ptr = cast_bin_expr(OS_LESS, op1, op2)
            elif la() in [OS_GREATER]:
                op1 = ptr
                match(OS_GREATER)
                op2 = additive_expression()
                ptr = cast_bin_expr(OS_GREATER, op1, op2)
            elif la() in [OS_LESS_EQ]:
                op1 = ptr
                match(OS_LESS_EQ)
                op2 = additive_expression()
                ptr = cast_bin_expr(OS_LESS_EQ, op1, op2)
            elif la() in [OS_GREATER_EQ]:
                op1 = ptr
                match(OS_GREATER_EQ)
                op2 = additive_expression()
                ptr = cast_bin_expr(OS_GREATER_EQ, op1, op2)
            elif la() in [OS_EQ_EQ, OS_NOT_EQ, OS_SEMICOLON, OS_CLOSE_PAREN, OS_COMMA]:
                break
            else:
                err()
    else:
        err()

    return ptr

def additive_expression():
    ptr = None
    op1 = None
    op2 = None

    if la() in [IDENTIFIER, CONSTANT_INT, OS_OPEN_PAREN]:
        ptr = multiplicative_expression()
        while True:
            if la() in [OS_PLUS]:
                op1 = ptr
                match(OS_PLUS)
                op2 = multiplicative_expression()
                ptr = cast_bin_expr(OS_PLUS, op1, op2)
            elif la() in [OS_MINUS]:
                op1 = ptr
                match(OS_MINUS)
                op2 = multiplicative_expression()
                ptr = cast_bin_expr(OS_MINUS, op1, op2)
            elif la() in [OS_LESS, OS_GREATER, OS_LESS_EQ, OS_GREATER_EQ, OS_EQ_EQ, OS_NOT_EQ, OS_SEMICOLON, OS_CLOSE_PAREN, OS_COMMA]:
                break
            else:
                err()
    else:
        err()

    return ptr
    
def multiplicative_expression():
    ptr = None
    op1 = None
    op2 = None

    if la() in [IDENTIFIER, CONSTANT_INT, OS_OPEN_PAREN]:
        ptr = primary_expression()
        while True:
            if la() in [OS_MULT]:
                op1 = ptr
                match(OS_MULT)
                op2 = primary_expression()
                ptr = cast_bin_expr(OS_MULT, op1, op2)
            elif la() in [OS_DIV]:
                op1 = ptr
                match(OS_DIV)  
                op2 = primary_expression()
                ptr = cast_bin_expr(OS_DIV, op1, op2)
            elif la() in [OS_MOD]:
                op1 = ptr
                match(OS_MOD)
                op2 = primary_expression()
                ptr = cast_bin_expr(OS_MOD, op1, op2)
            elif la() in [OS_PLUS, OS_MINUS, OS_LESS, OS_GREATER, OS_LESS_EQ, OS_GREATER_EQ, OS_EQ_EQ, OS_NOT_EQ, OS_SEMICOLON, OS_CLOSE_PAREN, OS_COMMA]:
                break
            else:
                err()
    else:
        err()

    return ptr

def primary_expression():
    ptr = None
    arg_list = None

    if la() in [IDENTIFIER]:
        name = law()
        match(IDENTIFIER)
        if la() in [OS_OPEN_PAREN]:
            match(OS_OPEN_PAREN)
            arg_list = argument_expression_list_opt()
            match(OS_CLOSE_PAREN)
            ptr = cast_call_expr(name, arg_list)
        elif la() in [OS_MULT, OS_DIV, OS_MOD, OS_PLUS, OS_MINUS, OS_LESS, OS_GREATER, OS_LESS_EQ, OS_GREATER_EQ, OS_EQ_EQ, OS_NOT_EQ, OS_SEMICOLON, OS_CLOSE_PAREN, OS_COMMA]:
            ptr = cast_var_expr(name)
        else:
            err()
    elif la() in [CONSTANT_INT]:
        i = int(law())
        match(CONSTANT_INT)
        ptr = cast_int_constant_expr(i)
    elif la() in [OS_OPEN_PAREN]:
        match(OS_OPEN_PAREN)
        ptr = expression()
        match(OS_CLOSE_PAREN)
    else:
        err()

    return ptr

def argument_expression_list_opt():
    ptr = None

    if la() in [IDENTIFIER, CONSTANT_INT, OS_OPEN_PAREN]:
        ptr = argument_expression_list()
    elif la() in [OS_CLOSE_PAREN]:
        pass
    else:
        err()

    return ptr

def argument_expression_list():
    ptr = None
    rhs = None

    if la() in [IDENTIFIER, CONSTANT_INT, OS_OPEN_PAREN]:
        ptr = expression()
        while True:
            if la() in [OS_COMMA]:
                match(OS_COMMA)
                rhs = expression()
            elif la() in [OS_CLOSE_PAREN]:
                break
            else:
                err()
    else:
        err()

    return [ptr] + [rhs]

if __name__ == "__main__":
    main()
