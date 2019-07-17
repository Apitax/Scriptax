grammar Ah5;

/***********
PARSER RULES
***********/

prog : script_structure EOF ;

script_structure : global_statements statements ;

global_statements :
      (import_statement TERMINATOR)*
      (extends_statement TERMINATOR)?
      (ahoptions_statement TERMINATOR)?
      ;

statements : statement* ;

statement :
      NOT? (
        terminated
        | non_terminated
      );

expr :
      labels
      | inject
      | LPAREN expr RPAREN
      | <assoc=right> expr POW expr
      | MINUS expr
      | NOT expr
      | expr (MUL|DIV|PERCENT) expr
      | expr (PLUS|MINUS) expr
      | expr (GE | LE | GT | LT) expr
      | expr (EQ | NEQ) expr
      | expr AND expr
      | expr OR expr
      | atom_create_instance
      | runnable_statements
      | casting
      | count
      | typing
      | reflection
      | atom ;

atom:
      atom_obj_dict
      | atom_obj_list
      | atom_obj_enum
      | atom_string
      | atom_number
      | atom_boolean
      | atom_hex
      | atom_none
      | atom_callback
      | method_def_atom
      | atom_create_instance ;

terminated :
      (
        log_statement
        | each_statement
        | return_statement
        | done_statement
        | continue_statement
        | error_statement
        | delete_statement
        | await_statement
        | assignment_statement
        | runnable_statements
      ) TERMINATOR ;

runnable_statements : AWAIT?
      (
        method_call_statement
        | os_statement
      ) atom_callback? ;

non_terminated : flow | method_def_statement ;

// Seperation between big chunks and callback blocks

method_call_statement : (SUPER)? labels LPAREN optional_parameters_block RPAREN (DOT method_call_statement)* ;

each_statement : EACH (expr | LPAREN expr RPAREN) atom_callback ; // each loops are threaded

atom_callback : (LPAREN optional_parameters_block RPAREN ARROW)? callback_block ;

callback_block : EXECUTEOPEN statements EXECUTECLOSE ;

// seperataition between callback blocks and regular blocks

method_def_atom : symbol_type? LPAREN flexible_parameter_block RPAREN ARROW block ;

method_def_statement : attributes symbol_type? label LPAREN flexible_parameter_block RPAREN block ;

flow :
      if_statement
      | while_statement
      | for_statement
      | until_statement
      | switch_statement ;

if_statement : IF condition block (ELSE IF condition block)* (ELSE block)? ;

for_statement : FOR
        (
            labels (COMMA labels)? IN (expr | range_function) (COMMA expr)? |
            LPAREN labels (COMMA labels)? IN (expr | range_function) (COMMA expr)? RPAREN
        )
        block ;

until_statement: UNTIL condition (COMMA expr)? (COMMA expr)? block ;

while_statement : WHILE condition block ;

switch_statement : SWITCH BLOCKOPEN case_statement* default_statement? BLOCKCLOSE ;

case_statement : CASE condition block ;

default_statement : DEFAULT block ;

range_function : RANGE LPAREN expr (COMMA expr)? (COMMA expr)? RPAREN ;

block : BLOCKOPEN statements BLOCKCLOSE | statement ;

done_statement : DONE ;

continue_statement : CONTINUE ;

// statements

os_statement : OS LPAREN expr COMMA expr (COMMA optional_parameters_block)? RPAREN ;

log_statement : LOG LPAREN expr RPAREN ;

flexible_parameter_block : flexible_parameter? (COMMA flexible_parameter)* ; // used to be sig

flexible_parameter : symbol_type? (required_parameter | optional_parameter) ;

import_statement : (FROM label)? IMPORT labels (AS label)? ;

extends_statement : EXTEND 
      (
        label (WITH label (COMMA label)*) 
        | label 
        | (WITH label (COMMA label)*)
      ) ;

atom_create_instance : NEW label LPAREN optional_parameters_block RPAREN (DOT method_call_statement)? ;

ahoptions_statement : AHOPTIONS LPAREN atom_obj_dict RPAREN;

optional_parameters_block : (dict_signal | optional_parameter)? (COMMA (dict_signal | optional_parameter))* ;

optional_parameter : labels EQUAL expr ;

dict_signal : SIGNAL (atom_obj_dict | labels) ;

casting : symbol_type LPAREN expr RPAREN ;

assignment_statement :
      symbol_type? labels ((
        (SOPEN SCLOSE)? EQUAL
        | PE
        | ME
        | MUE
        | DE
      ) expr | D_PLUS | D_MINUS);

symbol_type :
    TYPE_INT
    | TYPE_DEC
    | TYPE_BOOL
    | TYPE_HEX
    | TYPE_NONE
    | TYPE_THREAD
    | TYPE_METHOD
    | TYPE_INSTANCE
    | TYPE_PYTHONIC
    | TYPE_ANY
    | TYPE_STR
    | TYPE_LIST
    | TYPE_DICT ;

atom_obj_dict : BLOCKOPEN ((label | expr) COLON expr)? (COMMA ((label | expr) COLON expr)?)* BLOCKCLOSE ;

atom_obj_list : SOPEN expr? (COMMA expr?)* SCLOSE ;

atom_obj_enum : LPAREN ((label ARROW expr (COMMA (label ARROW expr)?)*) | (label (COMMA label?)*))? RPAREN ;

error_statement : ERROR LPAREN expr? RPAREN;

inject : LT BAR expr GT ;

condition : LPAREN expr RPAREN | expr;

return_statement : RETURNS expr? ;

typing : TYPE LPAREN expr RPAREN ;

count : HASH expr ;

// expr

delete_statement : DEL LPAREN labels RPAREN;

await_statement: AWAIT labels? ;

reflection : AT labels ;

required_parameter : labels ;

labels : label_comp (DOT label_comp)* ;

label_comp : label (SOPEN (expr | expr COLON | COLON expr | expr COLON expr) SCLOSE)? | inject ;

label : LABEL ;

attributes : (SCRIPT | STATIC | ASYNC)+ ;

atom_string : STRING ;

atom_number : INT | FLOAT ;

atom_boolean : TRUE | FALSE ;

atom_hex : HEX ;

atom_none : NONE ;


/**********
LEXER RULES
**********/

/** KEYWORD COMBINATORS **/
AND : A N D | SAND ;
OR : O R | SOR ;


/** CONDITIONAL EXPRESSIONS **/
GT :   '>'  ;
LT :   '<'  ;
GE :   '>=' ;
LE :   '<=' ;
EQ :   '==' ;
NEQ :  '!=' ;
SAND : '&&' ;
SOR :  '||' ;


/** ASSIGNMENTS **/
D_PLUS :  '++' ;
D_MINUS : '--' ;
PE :      '+=' ;
ME :      '-=' ;
MUE :     '*=' ;
DE :      '/=' ;
EQUAL :   '='  ;


/** OPERATORS **/
PLUS :    '+' ;
MINUS :   '-' ;
MUL :     '*' ;
DIV :     '/' ;
POW :     '^' ;
NOT :     '!' ;
ULINE :   '_' ;
DOT :     '.' ;
COLON :   ':' ;
PERCENT : '%' ;
COMMA :   ',' ;
BAR :     '|' ;


/** TYPES **/
INT : '-'?DIGIT+ ;
FLOAT : '-'? DIGIT* DOT DIGIT+ ;
FALSE : F A L S E ;
TRUE : T R U E ;
STRING : QUOTE (ESC|~["\r\n])*? QUOTE | SQUOTE (ESC|~['\r\n])*? SQUOTE ;
HEX : ('0x'|'0X')(DIGIT|A|B|C|D|E|F)+;
NONE : N O N E | N U L L ;


/** BLOCKS AND ENCLOSURES **/
EXECUTEOPEN : '{%' ;
EXECUTECLOSE : '%}' ;
BLOCKOPEN : '{';
BLOCKCLOSE : '}';
LPAREN : '(';
RPAREN : ')';
SOPEN : '[';
SCLOSE : ']';


/** KEY SYMBOLS **/
VARIABLE_ID : '$' ;
TERMINATOR : ';' ;
HASH : '#' ;
ARROW : '->' ;
AT : '@' ;
SIGNAL : '..' ;


/** BLOCK FLOW **/
IF : I F ;
ELSE : E L S E ;
FOR : F O R ;
EACH : E A C H;
WHILE : W H I L E ;
UNTIL : U N T I L ;
SWITCH : S W I T C H ;
CASE : C A S E ;


/** STATEMENT FLOW **/
RETURNS : R E T U R N ;
CONTINUE : C O N T I N U E ;
DONE : D O N E ;
DEFAULT : D E F A U L T ;


/** TYPES **/
TYPE_INT : I N T ;
TYPE_DICT : D I C T ;
TYPE_LIST : L I S T ;
TYPE_DEC : D E C ;
TYPE_STR : S T R ;
TYPE_BOOL : B O O L ;
TYPE_HEX : H E X ;
TYPE_NONE : N O N E ;
TYPE_THREAD : T H R E A D ;
TYPE_METHOD : M E T H O D ;
TYPE_INSTANCE : I N S T A N C E ;
TYPE_PYTHONIC : P Y T H O N I C ;
TYPE_ANY : A N Y ;


/** METHODS **/
AHOPTIONS : A H O P T I O N S ;
IMPORT : I M P O R T ;
EXTEND : E X T E N D ;
DEL : D E L ;
OS : O S ;
LOG : L O G ;
ERROR : E R R O R ;
TYPE : T Y P E ;


/** Attributes **/
SCRIPT : S C R I P T ;
STATIC : S T A T I C ;
ASYNC : A S Y N C ;


/** MODIFIERS **/
IN : I N ;
AS : A S ;
FROM : F R O M ;
WITH: W I T H ;
AWAIT : A W A I T ;
NEW : N E W ;
SUPER : S U P E R ;
RANGE : R A N G E ;


/** VARIABLES **/
LABEL : VARIABLE_ID? (LETTER | ULINE | DIGIT | INT | FLOAT)+ ;


/** COMMENTS **/
BLOCK_COMMENT : DIV MUL .*? MUL DIV -> skip ;
LINE_COMMENT : DIV DIV ~[\r\n]* -> skip ;


/** NEWLINES AND WHITESPACE **/
NEWLINE : '\r'? '\n' -> skip ;
WS : (' ' | '\t')+ -> skip ;


/********
FRAGMENTS
********/
fragment ESC : '\\"' | '\\\'' | '\\\\' ; // 2-char sequences \" and \\

fragment LETTER : A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z ;

fragment A:'A'|'a';    fragment B:'B'|'b';    fragment C:'C'|'c';    fragment D:'D'|'d';
fragment E:'E'|'e';    fragment F:'F'|'f';    fragment G:'G'|'g';    fragment H:'H'|'h';
fragment I:'I'|'i';    fragment J:'J'|'j';    fragment K:'K'|'k';    fragment L:'L'|'l';
fragment M:'M'|'m';    fragment N:'N'|'n';    fragment O:'O'|'o';    fragment P:'P'|'p';
fragment Q:'Q'|'q';    fragment R:'R'|'r';    fragment S:'S'|'s';    fragment T:'T'|'t';
fragment U:'U'|'u';    fragment V:'V'|'v';    fragment W:'W'|'w';    fragment X:'X'|'x';
fragment Y:'Y'|'y';    fragment Z:'Z'|'z';

fragment LOWERCASE : [a-z] ;
fragment UPPERCASE : [A-Z] ;

fragment DIGIT : [0-9] ;

fragment QUOTE : '"' ;
fragment SQUOTE : '\'' ;
