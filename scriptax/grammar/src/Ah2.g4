grammar Ah210;

//options { tokenVocab=AhLex210; }

/***********
PARSER RULES
***********/

prog : statements EOF ;

statements : statement* ;

statement : 
      NOT? (
        terminated
        | non_terminated 
      );

terminated : 
      (
        each_statement
        | params_statement
        | options_statement
        | return_statement
        | error_statement
        | delete_statement
        | await
        | executers
        | assignment
        | scoping
        | log
        | auth
        | url
      ) TERMINATOR ;

non_terminated : 
      flow ;

executers : execute
         | async_execute ;

expr :
      REQUEST? labels
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
      | async_execute
      | execute
      | login_statement
      | endpoint_statement
      | casting
      | count
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
      
if_statement : IF condition block (ELSE IF condition block)* (ELSE block)? ;

while_statement : WHILE condition block ;

for_statement : FOR labels IN expr block ;

each_statement : EACH expr callback ;

condition : LPAREN expr RPAREN ;

block : BLOCKOPEN statements BLOCKCLOSE | statement ;

callback : (LPAREN optional_parameters_block RPAREN ARROW)? callback_block ;

callback_block : EXECUTEOPEN statements EXECUTECLOSE ;

optional_parameters_block : optional_parameter? (COMMA optional_parameter)* ;

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
        | SCRIPT 
        | CUSTOM
      ) LPAREN expr (COMMA obj_dict)? (COMMA optional_parameter)* RPAREN ;

execute : commandtax callback? ;

async_execute: ASYNC commandtax callback? ; // (labels EQUAL)? 

await: AWAIT labels? ;

labels : label_comp (DOT label_comp)* ;

label_comp : LABEL | inject ;

params_statement : SIG sig_parameter (COMMA sig_parameter)* ;

options_statement : OPTIONS expr ;

delete_statement : DEL labels ;

error_statement : ERROR expr? ;

return_statement : RETURNS expr? ;

login_statement : LOGIN LPAREN optional_parameters_block RPAREN ;

endpoint_statement : ENDPOINT LPAREN expr RPAREN ; 

scoping : imports | exports | name ;

name : NAME expr;

exports : EXPORT (labels | execute);

imports : IMPORT execute ;

casting : 
      (
        TYPE_INT
        | TYPE_DEC
        | TYPE_BOOL
        | TYPE_STR
        | TYPE_LIST
        | TYPE_DICT
      ) LPAREN expr RPAREN ;

auth : AUTH expr ;

url : URL expr ;

log : LOG LPAREN expr RPAREN ;

count : HASH expr ;

inject : MUSTACHEOPEN expr MUSTACHECLOSE ;

atom: 
      obj_dict
      | obj_list
      | string
      | number
      | boolean ;

obj_dict : BLOCKOPEN (expr COLON expr)? (COMMA (expr COLON expr)?)* BLOCKCLOSE ; 

obj_list : SOPEN expr? (COMMA expr?)* SCLOSE ;

string : STRING ;

number : INT | FLOAT ;

boolean : TRUE | FALSE ;


/**********
LEXER RULES
**********/


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
HEX : ('0x'|'0X')(HEXDIGIT)HEXDIGIT*;
/** BLOCKS AND ENCLOSURES **/
EXECUTEOPEN : '{%' ;
EXECUTECLOSE : '%}' ;
MUSTACHEOPEN : '{{' ;
MUSTACHECLOSE : '}}' ;
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
/** KEYWORD COMBINATORS **/
AND : A N D | SAND ;
OR : O R | SOR ;
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
LOGIN : L O G I N ;
LOG : L O G ;
ENDPOINT : E N D P O I N T ;
/** METHODS **/           // These don't use ()'s and they do NOT return any values
SIG : S I G ;
OPTIONS : O P T I O N S ;
NAME : N A M E ;
IMPORT : I M P O R T ;
EXPORT : E X P O R T ;
DEL : D E L ;
URL : U R L ;
AUTH : A U T H ;
/** COMMANDTAX METHODS **/
COMMANDTAX : C T ;
SCRIPT : S C R I P T ;
CUSTOM : C U S T O M ;
GET : G E T ;
POST : P O S T ;
PUT : P U T ;
PATCH : P A T C H ;
DELETE : D E L E T E ;
/** KEYWORDS **/
IN : I N ;
SET : S E T ;
ASYNC : A S Y N C ;
AWAIT : A W A I T ;
/** KEYCHANGERS **/
REQUEST : R COLON ;
/** VARIABLES **/
LABEL : VARIABLE_ID? (LETTER | ULINE | DIGIT | INT | FLOAT)+ ;
/** COMMENTS **/
BLOCK_COMMENT : DIV MUL .*? MUL DIV -> channel(HIDDEN) ;
LINE_COMMENT : DIV DIV ~[\r\n]* -> channel(HIDDEN) ;
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

fragment HEXDIGIT : '0..9'|'a..f'|'A'..'F' ;