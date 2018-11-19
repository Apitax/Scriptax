grammar Ah3;

/***********
PARSER RULES
***********/

prog : script_structure EOF ;

script_structure : global_statements root_level_statements statements ;

global_statements :
      (import_statement TERMINATOR)*
      (sig_statement TERMINATOR)?
      (extends_statement TERMINATOR)?
      (options_statement TERMINATOR)?
      ;

root_level_statements : method_statement* ;

statements : statement* ;

statement : 
      NOT? (
        terminated
        | non_terminated
      );

terminated : 
      (
        each_statement
        | return_statement
        | error_statement
        | delete_statement
        | execute_statement
        | method_call
        | await_statement
        | assignment
        | log
      ) TERMINATOR ;

non_terminated : 
      flow ;

execute_statement : execute
         | async_execute ;

expr :
      labels
      | inject
      | LPAREN expr RPAREN
      | <assoc=right> expr POW expr
      | MINUS expr
      | NOT expr
      | expr (MUL|DIV) expr
      | expr (PLUS|MINUS) expr 
      | expr (GE | LE | GT | LT) expr
      | expr (EQ | NEQ) expr
      | expr AND expr
      | expr OR expr
      | create_instance
      | method_call
      | async_execute
      | execute
      | auth_statement
      | endpoint_statement
      | casting
      | count
      | reflection
      | atom ;

assignment : 
      SET? labels ((
          (SOPEN SCLOSE)? EQUAL 
          | PE
          | ME
          | MUE
          | DE
      ) expr | D_PLUS | D_MINUS);

flow : 
      if_statement
      | while_statement
      | for_statement ;

create_instance : NEW label LPAREN optional_parameters_block RPAREN ; 

method_statement : attribute+ ASYNC? label LPAREN sig_parameter_block RPAREN block ;

method_call : AWAIT? labels LPAREN optional_parameters_block RPAREN callback? ;

if_statement : IF condition block (ELSE IF condition block)* (ELSE block)? ;

while_statement : WHILE condition block ;

for_statement : FOR labels IN expr block ;

each_statement : EACH expr callback ;

condition : LPAREN expr RPAREN ;

block : BLOCKOPEN statements BLOCKCLOSE | statement ;

callback : (LPAREN optional_parameters_block RPAREN ARROW)? callback_block ;

callback_block : EXECUTEOPEN statements EXECUTECLOSE ;

optional_parameters_block : optional_parameter? (COMMA optional_parameter)* ;

sig_parameter_block : sig_parameter? (COMMA sig_parameter)* ;

sig_parameter : labels | optional_parameter ;

call_parameter : expr | optional_parameter ;

optional_parameter : labels EQUAL expr ;

commandtax : 
      ( 
        GET 
        | POST 
        | PUT 
        | PATCH 
        | DELETE 
        | COMMANDTAX 
      ) LPAREN expr (COMMA atom_obj_dict)? (COMMA optional_parameters_block)? RPAREN ;

execute : commandtax callback? ;

async_execute: ASYNC commandtax callback? ; // (labels EQUAL)? 

await_statement: AWAIT labels? ;

labels : label_comp (DOT label_comp)* ;

label_comp : label | inject ;

label : LABEL ;

attribute : API | SCRIPT ; 

extends_statement : EXTENDS LPAREN label (COMMA optional_parameters_block)? RPAREN ;

sig_statement : SIG LPAREN sig_parameter_block RPAREN ;

options_statement : OPTIONS LPAREN optional_parameters_block RPAREN;

delete_statement : DEL LPAREN labels RPAREN;

error_statement : ERROR LPAREN expr? RPAREN;

return_statement : RETURNS expr? ;

auth_statement : AUTH LPAREN optional_parameters_block RPAREN ;

endpoint_statement : ENDPOINT LPAREN expr RPAREN ; 

import_statement : (FROM label)? IMPORT labels (LPAREN optional_parameters_block RPAREN)? (AS label)? ;

casting : 
      (
        TYPE_INT
        | TYPE_DEC
        | TYPE_BOOL
        | TYPE_STR
        | TYPE_LIST
        | TYPE_DICT
      ) LPAREN expr RPAREN ;

log : LOG LPAREN expr RPAREN ;

count : HASH expr ;

reflection : AT labels ;

inject : MUSTACHEOPEN expr MUSTACHECLOSE ;

atom: 
      atom_obj_dict
      | atom_obj_list
      | atom_string
      | atom_number
      | atom_boolean
      | atom_hex
      | atom_none ;

atom_obj_dict : BLOCKOPEN (expr COLON expr)? (COMMA (expr COLON expr)?)* BLOCKCLOSE ;

atom_obj_list : SOPEN expr? (COMMA expr?)* SCLOSE ;

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


/** TYPES **/
//NUMBER : INT | FLOAT ; 
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
MUSTACHEOPEN : '<' ;
MUSTACHECLOSE : '>' ;
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

/** FLOW **/
RETURNS : R E T U R N ;
EACH : E A C H;
IF : I F ;
THEN : T H E N ;
ELSE : E L S E ;
FOR : F O R ;
WHILE : W H I L E ;
ERROR : E R R O R ;

/** HELPER FUNCTIONS **/  // These use ()'s and CAN return values
TYPE_INT : I N T ;
TYPE_DICT : D I C T ;
TYPE_LIST : L I S T ;
TYPE_DEC : D E C ;
TYPE_STR : S T R ;
TYPE_BOOL : B O O L ;
LOG : L O G ;
ENDPOINT : E N D P O I N T ;

/** METHODS **/           // These don't return any values
SIG : S I G ;
OPTIONS : O P T I O N S ;
IMPORT : I M P O R T ;
DEL : D E L ;
URL : U R L ;
AUTH : A U T H ;
EXTENDS : E X T E N D S ;

/** COMMANDTAX METHODS **/
COMMANDTAX : C T ;
GET : G E T ;
POST : P O S T ;
PUT : P U T ;
PATCH : P A T C H ;
DELETE : D E L E T E ;

/** Attributes **/
SCRIPT : S C R I P T ;
API : A P I ;

/** KEYWORDS **/
IN : I N ;
AS : A S ;
FROM : F R O M ;
SET : S E T ;
ASYNC : A S Y N C ;
AWAIT : A W A I T ;
NEW : N E W ;

/** VARIABLES **/
LABEL : VARIABLE_ID? (LETTER | ULINE | DIGIT | INT | FLOAT)+ ;

/** COMMENTS **/
BLOCK_COMMENT : DIV MUL .*? MUL DIV -> skip ;
LINE_COMMENT : DIV DIV ~[\r\n]* -> skip ;

/** NEWLINES AND WHITESPACE **/
NEWLINE : '\r'? '\n' -> skip;
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
