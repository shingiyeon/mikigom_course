# EMPTY is a meta symbol to mean an empty string.

parse:
    translation_unit EOF

translation_unit:
    translation_unit external_declaration
    external_declaration

external_declaration:
    function_definition

function_definition:
    int identifier ( parameter_type_list_opt ) compound_statement

parameter_type_list_opt:
    parameter_type_list
    EMPTY

parameter_type_list:
    parameter_type_list ,  parameter_type
    parameter_type

parameter_type:
    int identifier

compound_statement:
    { declaration_list_opt statement_list_opt }

declaration_list_opt:
    declaration_list_opt declaration
    EMPTY

statement_list_opt:
    statement_list_opt statment
    EMPTY

declaration:
    int identifier ;

statement:
    iteration_statement
    selection_statement
    expression_statement
    jump_statement
    compound_statement

iteration_statement:
    while ( expression ) statement

selection_statement:
    if ( expression ) statement 
    if ( expression ) statement else statement

expression_statement:
    identifier = expression ;
    ;

jump_statement:
    return ;
    return expression ;

expression:
    equality_expression

equality_expression:
    relational_expression
    equality_expression == relational_expression
    equality_expression != relational_expression

relational_expression:
    additive_expression
    relational_expression < additive_expression
    relational_expression > additive_expression
    relational_expression <= additive_expression
    relational_expression >= additive_expression

additive_expression:
    multiplicative_expression
    additive_expression + multiplicative_expression
    additive_expression - multiplicative_expression

multiplicative_expression:
    primary_expression
    multiplicative_expression *  primary_expression
    multiplicative_expression /  primary_expression
    multiplicative_expression %  primary_expression

primary_expression:
    identifier
    identifier ( argument_expression_list_opt )
    integer_constant
    ( expression )

argument_expression_list_opt:
    argument_expression_list
    EMPTY

argument_expression_list:
    expression
    argument_expression_list , expression
