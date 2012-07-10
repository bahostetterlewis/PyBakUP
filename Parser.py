import ply.yacc as yacc
import Lexer
tokens = Lexer.tokens

precedence = (('left', 'OR'),
              ('left', 'AND'),
              ('left', 'EQUAL'),
              ('left', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREAT_EQUAL'),
              ('left', 'PLUS')) 

def p_expr_operator(p):
  '''expr : expr OR expr
          | expr AND expr
          | expr LESS_EQUAL expr
          | expr LESS expr
          | expr GREAT_EQUAL expr
          | expr GREATER expr
          | expr EQUAL expr
          | expr PLUS expr'''

  if p[2] == "OR":
    p[0] = p[1] or p[3]
  elif p[2] == "AND":
    p[0] = p[1] and p[3]
  elif p[2] == "LESS_EQUAL":
    p[0] = p[1] <= p[3]
  elif p[2] == "LESS":
    p[0] = p[1] < p[3]
  elif p[2] == "GREAT_EQUAL":
    p[0] = p[1] >= p[3]
  elif p[2] == "GREATER":
    p[0] = p[1] > p[3]
  elif p[2] == "EQUAL":
    p[0] = p[1] == p[3]
  elif p[2] == "PLUS":
    p[0] = p[1] + p[3]


def p_expr_with_parens(p):
  '''primary : LPAREN expr RPAREN'''
  p[0] = p[2]

def p_expr_extra(p):
  '''expr : operand
          | primary'''
  p[0] = p[1]

def p_operand_time(p):
  '''operand : time'''
  p[0] = p[1]

def p_operand_key(p):
  '''operand : key'''
  p[0] = p[1]

def p_time(p):
  '''time : INT frame'''
  p[0] = p[1] * p[2]

def p_frame(p):
  '''frame : MONTH
           | DAY
           | HOUR
           | MINUTE'''

  if p[1] == "MONTH":
    p[0] = 2629743
  elif p[1] == "DAY":
    p[0] = 86400
  elif p[1] == "HOUR":
    p[0] = 3600
  elif p[1] == "MINUTE":
    p[0] = 60


def p_key_last_backup(p):
  '''key :  LAST_BACKUP'''
  raise NotImplementedError("I havn't implemented this yet")

def p_key_booleon(p):
  '''key :  MODIFIED
         |  TRUE
         |  FALSE'''
  if p[1] == "Modified":
    raise NotImplementedError("I havn't implemented this yet")
  elif p[1] == "True":
    p[0] = True
  elif p[1] == "False":
    p[0] = False

yacc.yacc()
result = yacc.parse('2 hours + 3 mins && True')
print ("result", result)
