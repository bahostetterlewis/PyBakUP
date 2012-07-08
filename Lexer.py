import ply.lex as lex
import ply.yacc as yacc

## @package Parser
#  This is the parser that is used to make custom backup conditions
#
#  This package will use ply(Python Lex and Yacc) to create a method for parsing
#  the user generated backup conditions (hopefully making it easy to extend as desired.
#  It will take a string, parse it, and return a boolean (true or false)
#  which will allow for the program to decide if a backup is necessary
#  
#  @note Tokens have the following attributes: type, value, lexpos


## @var tokens
#  The tokens our lexer will use
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
          'INT']         #Any integer


t_ignore = ' \t'
def t_AND(t):
  r'&&'
  t.value = "AND"
  return t
def t_GREATER(t):
  r'>'
  t.value = "GREATER"
  return t
def t_LESS(t):
  r'<'
  t.value = "LESS"
  return t
def t_LESS_EQUAL(t):
  r'<='
  t.value = "LESS_EQUAL"
  return t
def t_GREAT_EQUAL(t):
  r'>='
  t.value = "GREAT_EQUAL"
  return t
def t_EQUAL(t):
  r'=='
  t.value = "EQUAL"
  return t
def t_PLUS(t):
  r'\+'
  t.value = "PLUS"
  return t
def t_OR(t):
  r'\|\|'
  t.value = "OR"
  return t
def t_MONTH(t):
  r'mon(th)?s?'
  t.value = "MONTH"
  return t
def t_DAY(t):
  r'd((ay)s?)?'
  t.value = "DAY"
  return t
def t_HOUR(t):
  r'h((our)s?)?'
  t.value = "HOUR"
  return t
def t_MINUTE(t):
  r'min(ute)?s?'
  t.value = "MINUTE"
  return t
t_TRUE = r'True'
t_FALSE =  r'False'
def t_LAST_BACKUP(t):
  r'LastBU'
  t.value = "LAST_BACKUP"
  return t
t_MODIFIED = r'Modified'

def t_INT(t):
  r'\d+'
  t.value = int(t.value)
  return t

lex.lex()
