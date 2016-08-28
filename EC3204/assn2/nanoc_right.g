# EMPTY is a meta symbol to mean an empty string.

parse:
    translation_unit EOF

translation_unit:
    external_declaration translation_unit_external_declaration

translation_unit_external_declaration:
    external_declaration translation_unit_external_declaration
    EMPTY

external_declaration:
    function_definition

function_definition:
    int identifier ( parameter_type_list_opt ) compound_statement

parameter_type_list_opt:
    parameter_type_list
    EMPTY

parameter_type_list:
    parameter_type parameter_type_list_parameter_type

parameter_type_list_parameter_type:
    , parameter_type parameter_type_list_parameter_type
    EMPTY

parameter_type:
    int identifier

compound_statement:
    { declaration_list_opt statement_list_opt }

declaration_list_opt:
    declaration_list_opt_declaration

declaration_list_opt_declaration
    declaration declaration_list_opt_declaration
    EMPTY

statement_list_opt:
    statement_list_opt_statement

statement_list_opt_statement:
    statement statement_list_opt_statement
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
    if ( expression ) statement else_selection_statement

else_selection_statement:
    else statement
    EMPTY

expression_statement:
    identifier = expression ;
    ;

jump_statement:
    return expression_jump_statement

expression_jump_statement:
    expression ;
    ;

expression:
    equality_expression

equality_expression:
    relational_expression equality_expression_relational_expression

equaltiy_expression_relational_expression
    == relational_expression equality_expression_relational_expression
    != relational_expression equality_expression_relational_expression
    EMPTY

relational_expression:
    additive_expression relational_expression_additive_expression

relational_expression_additive_expression:
    < additive_expression relational_expression_additive_expression
    > additive_expression relational_expression_additive_expression
    <= additive_expression relational_expression_additive_expression
    >= additive_expression relational_expression_additive_expression
    EMPTY

additive_expression:
    multiplicative_expression additive_expression_multiplicative_expression

additive_expression_multiplicative_expression:
    + multiplicative_expression additive_expression_multiplicative_expression
    - multiplicative_expression additive_expression_multiplicative_expression
    EMPTY

multiplicative_expression:
    primary_expression multiplicative_expression_primary_expression

multiplicative_expression_primary_expression:
    * primary_expression multiplicative_expression_primary_expression
    / primary_expression multiplicative_expression_primary_expression
    % primary_expression multiplicative_expression_primary_expression
    EMPTY

primary_expression:
    identifier argument_expression_list_opt_primary_expression
    integer_constant
    ( expression )

argument_expression_list_opt_primary_expression:
    ( argument_expression_list_opt )
    EMPTY

argument_expression_list_opt:
    argument_expression_list
    EMPTY

argument_expression_list:
    expression argument_expression_list_expression

argument_expression_list_expression
    , expression argument_expression_list_expression
    EMPTY
