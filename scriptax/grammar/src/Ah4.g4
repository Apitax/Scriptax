grammar Ah4;

/***********
PARSER RULES
***********/

prog : script_structure EOF ;

script_structure : global_statements root_level_statements statements ;

global_statements :
      (import_statement TERMINATOR)*
      (extends_statement TERMINATOR)?
      (ahoptions_statement TERMINATOR)?
      ;

root_level_statements : method_def_atom* ;

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
      | create_instance
      | runnable_statements
      | casting
      | count
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
      | method_def_atom ;

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
        | commandtax_statement
      ) atom_callback? ;

method_call_statement : labels LPAREN optional_parameters_block RPAREN ;

commandtax_statement : COMMANDTAX LPAREN expr RPAREN ;

os_statement : OS LPAREN expr RPAREN ;

each_statement : EACH expr atom_callback ;

atom_callback : (LPAREN optional_parameters_block RPAREN ARROW)? callback_block ;

callback_block : EXECUTEOPEN statements EXECUTECLOSE ;

// seperataition between callback blocks and regular blocks

method_def_atom : attributes label LPAREN flexible_parameter_block RPAREN block ;

non_terminated : flow ;

flow :
      if_statement
      | while_statement
      | for_statement
      | switch_statement ;

if_statement : IF condition block (ELSE IF condition block)* (ELSE block)? ;

for_statement : FOR labels IN expr block ;

while_statement : WHILE condition block ;

switch_statement : SWITCH BLOCKOPEN case_statement* default_statement? BLOCKCLOSE ;

case_statement : CASE condition block ;

default_statement : DEFAULT block ;

block : BLOCKOPEN statements BLOCKCLOSE | statement ;

done_statement : DONE ;

continue_statement : CONTINUE ;

// statements

log_statement : LOG LPAREN expr RPAREN ;

flexible_parameter_block : flexible_parameter? (COMMA flexible_parameter)* ; // used to be sig

flexible_parameter : required_parameter | optional_parameter ;

import_statement : (FROM label)? IMPORT labels (AS label)? ;

extends_statement : EXTEND 
      (
        label (WITH label (COMMA label)*) 
        | label 
        | (WITH label (COMMA label)*)
      ) ;

create_instance : NEW label LPAREN optional_parameters_block RPAREN ;

ahoptions_statement : AHOPTIONS LPAREN atom_obj_dict RPAREN;

optional_parameters_block : (dict_signal | optional_parameter)? (COMMA (dict_signal | optional_parameter))* ;

optional_parameter : labels EQUAL expr ;

dict_signal : SIGNAL (atom_obj_dict | labels) ;

casting :
      (
        TYPE_INT
        | TYPE_DEC
        | TYPE_BOOL
        | TYPE_STR
        | TYPE_LIST
        | TYPE_DICT
      ) LPAREN expr RPAREN ;

atom_obj_dict : BLOCKOPEN (expr COLON expr)? (COMMA (expr COLON expr)?)* BLOCKCLOSE ;

assignment_statement :
      labels ((
        (SOPEN SCLOSE)? EQUAL
        | PE
        | ME
        | MUE
        | DE
      ) expr | D_PLUS | D_MINUS);

atom_obj_list : SOPEN expr? (COMMA expr?)* SCLOSE ;

atom_obj_enum : LPAREN ((label ARROW expr (COMMA (label ARROW expr)?)*) | (label (COMMA label?)*))? RPAREN ;

error_statement : ERROR LPAREN expr? RPAREN;

inject : LT BAR expr GT ;

condition : LPAREN expr RPAREN ;

return_statement : RETURNS expr? ;

count : HASH expr ;

// expr

delete_statement : DEL LPAREN labels RPAREN;

await_statement: AWAIT labels? ;

reflection : AT labels ;

required_parameter : labels ;

labels : label_comp (DOT label_comp)* ;

label_comp : label (SOPEN (expr COLON | COLON expr | expr COLON expr) SCLOSE)? | inject ;

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
SIGNAL : '...' ;


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


/** CASTING **/
TYPE_INT : I N T ;
TYPE_DICT : D I C T ;
TYPE_LIST : L I S T ;
TYPE_DEC : D E C ;
TYPE_STR : S T R ;
TYPE_BOOL : B O O L ;


/** METHODS **/
AHOPTIONS : A H O P T I O N S ;
IMPORT : I M P O R T ;
EXTEND : E X T E N D ;
DEL : D E L ;
OS : O S ;
COMMANDTAX : C T ;
LOG : L O G ;
ERROR : E R R O R ;


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
