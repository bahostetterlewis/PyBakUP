import ply.lex as lex
import ply.yacc as yacc

## @package Lexer
#  This is the parser that is used to make custom backup conditions
#
#  This package will use ply(Python Lex and Yacc) to create a method for parsing
#  the user generated backup conditions (hopefully making it easy to extend as desired.
#  It will take a string, parse it, and return a boolean (true or false)
#  which will allow for the program to decide if a backup is necessary
#  
#  @note Tokens have the following attributes: type, value, lexpos
#  @author Barrett Hostetter-Lewis
#  @date 7-29-2012


## @var tokens
#  The tokens the lexer will use
tokens = ['AND',         #&&
          'GREATER',     #>
          'LESS',        #<
          'LESS_EQUAL',  #<=
          'GREAT_EQUAL', #>=
          'EQUAL',       #==
          'PLUS',        #+
          'OR',          #||
          'MONTH',       #mon, month, months
          'DAY',         #d, day, days
          'HOUR',        #h, hour, hours
          'MINUTE',      #min, minute, minutes
          'TRUE',        #True
          'FALSE',       #False
          'LAST_BACKUP', #LastBU
          'MODIFIED',    #Modified
          'LPAREN',      #(
          'RPAREN',      #)
          'INT']         #Any integer

## @var t_ignore
#  Regex for all ignored characters
t_ignore = ' \t'

## And Token
#  @pre none
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
def t_AND(t):
  r'&&'
  t.value = "AND"
  return t

## Greater than token
#  @pre none
#  @post A matching string will tokenized
#  @param t The current token
#  @return The created token object
def t_GREATER(t):
  r'>'
  t.value = "GREATER"
  return t

## Less than token
#  @pre none
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
def t_LESS(t):
  r'<'
  t.value = "LESS"
  return t

## Less than or equal to token
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
def t_LESS_EQUAL(t):
  r'<='
  t.value = "LESS_EQUAL"
  return t

## Greater than or equal to token
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
def t_GREAT_EQUAL(t):
  r'>='
  t.value = "GREAT_EQUAL"
  return t

## Equal token
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
def t_EQUAL(t):
  r'=='
  t.value = "EQUAL"
  return t

## Binary plus token
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
def t_PLUS(t):
  r'\+'
  t.value = "PLUS"
  return t

## Logical or token
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
def t_OR(t):
  r'\|\|'
  t.value = "OR"
  return t

## Month token
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
def t_MONTH(t):
  r'mon(th)?s?'
  t.value = "MONTH"
  return t

## Day token
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
def t_DAY(t):
  r'd((ay)s?)?'
  t.value = "DAY"
  return t

## Hour token
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
def t_HOUR(t):
  r'h((our)s?)?'
  t.value = "HOUR"
  return t

## Minute token
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
def t_MINUTE(t):
  r'min(ute)?s?'
  t.value = "MINUTE"
  return t

## @var t_TRUE 
#  regex for the True token
t_TRUE = r'True'
## @var t_FALSE
#  regex for the False token
t_FALSE =  r'False'

## LastBU token
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
def t_LAST_BACKUP(t):
  r'LastBU'
  t.value = "LAST_BACKUP"
  return t

## Left paren token
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
def t_LPAREN(t):
  r'\('
  t.VALUE = "LPAREN"
  return t

## Right paren token
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
def t_RPAREN(t):
  r'\)'
  t.value = "RPAREN"
  return t

## Modified token
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
t_MODIFIED = r'Modified'

## Int token
#  @post A matching string will be tokenized
#  @param t The current token
#  @return The created token object
#  @note This is the only token that has a custom defined value(a positive number for now)
def t_INT(t):
  r'\d+'
  t.value = int(t.value)
  return t

lex.lex()
