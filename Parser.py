import ply.yacc as yacc
import Lexer
tokens = Lexer.tokens

precedence = (('left', 'OR'),
              ('left', 'AND'),
              ('left', 'EQUAL'),
              ('left', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREAT_EQUAL'),
              ('left', 'PLUS')) 

def p_expr(p):
  '''expr : operand
          | expr OR expr
          | expr AND expr
          | expr LESS_EQUAL expr
          | expr LESS expr
          | expr GREAT_EQUAL expr
          | expr GREATER expr
          | expr EQUAL expr
          | expr PLUS expr'''


def p_operand(p):
  '''operand : time
             | key'''

def p_time(p):
  '''time : INT frame'''

def p_frame(p):
  '''frame : MONTH
           | DAY
           | HOUR
           | MINUTE'''

def p_key(p):
  '''key :  LAST_BACKUP 
         |  MODIFIED
         |  TRUE
         |  FALSE'''

yacc.yacc()
