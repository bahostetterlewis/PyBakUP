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


t_ignore =       ' \t'
t_AND =          r'&&'
t_GREATER =      r'>'
t_LESS =         r'<'
t_LESS_EQUAL =   r'<='
t_GREAT_EQUAL =  r'>='
t_EQUAL =        r'=='
t_PLUS =         r'\+'
t_OR =           r'\|\|'
t_MONTH =        r'mon(th)?s?'
t_DAY =          r'd((ay)s?)?'
t_HOUR =         r'h((our)s?)?'
t_MINUTE =       r'min(ute)?s?'
t_TRUE =         r'True'
t_FALSE =        r'False'
t_LAST_BACKUP =  r'LastBU'
t_MODIFIED =     r'Modified'

def t_INT(t):
  r'\d+'
  t.value = int(t.value)
  return t

lex.lex()
