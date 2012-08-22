import ply.yacc as yacc
import Lexer
tokens = Lexer.tokens

## @package Parser
#  This contains the definitions for the parser used to parse custom backup conditions
#
#  This is a lex/yacc based system. This file contains the yacc data including
#  precedence, associativity, and productions.
#  Each set of productions has its own function.
#  The basic language described is one of simple boolean statements, but this should
#  be easy to expand as needed.
#  It is a LALR parser
#  @author Barrett Hostetter-Lewis
#  @date 5/28/2012

## @var precedence
#  The precedence chart used by the parser.
#  Each item has the pattern (associativity, list_of_tokens)
#  Their order determines the precedence in decending order.
precedence = (('left', 'OR'),
              ('left', 'AND'),
              ('left', 'EQUAL'),
              ('left', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREAT_EQUAL'),
              ('left', 'PLUS')) 

## Start symbol
#  @pre  None
#  @post A parse tree is built and its value is set to either true or false
#  @param p The token currently being parsed.
#  @brief This function handles the start symbol for the parse tree.
#         All strings are broken into expr OPERATOR expr.
#         Possible operators are ||, &&, <=, >=, <, >, ==, +
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


## Expressions with Parens
#  @pre  None
#  @post An expression with parens has its parens stripped
#        and its "$$" set to the internal expression
#  @param p is the current token
#  @brief This function essentially removes the parenthesis around an expression.
#         But allows an expression to be denoted by what is inside a pair of parens.
#         Basically circumventing precedence. I don't know if this is strictly necessary
#         for the current language, but in the future I think it could be useful.
def p_expr_with_parens(p):
  '''primary : LPAREN expr RPAREN'''
  p[0] = p[2]

## Expressions with operands or parens
#  @pre  None
#  @post expr's main productions, expr->operand and
#        expr->primary (these are expressions with parens)
#  @param p is the current token
#  @brief This is the function that handles expr non terminals.
#         They are either operands or primary (expr with parens)
def p_expr_extra(p):
  '''expr : operand
          | primary'''
  p[0] = p[1]

## Operands that are time frames
#  @pre  None
#  @post The time frame operand will be parsed and returned
#  @param p The current token
#  @brief This is the function that handles an operand that is a time frame
#         and will allow its value to be determined then passed back up to the
#         parent.
def p_operand_time(p):
  '''operand : time'''
  p[0] = p[1]

## Operands that are a keyword
#  @pre  None
#  @post The keyword that was parsed is "returned"
#  @param p The current token
#  @brief This function handles an operand that is a keyword.
def p_operand_key(p):
  '''operand : key'''
  p[0] = p[1]

## Time frames
#  @pre  None
#  @post A time frame is evaluated and returned
#        This involves taking the INT and multiplying it by the frame
#  @param p The current token
#  @brief Multiplies a number of frames by the frame's value
def p_time(p):
  '''time : INT frame'''
  p[0] = p[1] * p[2]

## Frame
#  @pre None
#  @post A frame is convereted into a number of seconds
#  @param p The current token
#  @brief All frames are converted into their second value
#         Possible frames: MONTH, DAY, HOUR, MINUTE
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


## Keyword LastBU
#  @pre  None
#  @post The time (in seconds of the last backup for a file is returned
#  @param p The current token
#  @todo This function hasn't been implemented yet
def p_key_last_backup(p):
  '''key :  LAST_BACKUP'''
  raise NotImplementedError("I havn't implemented this yet")

## Keywords with boolean values
#  @pre  None
#  @post The of the token is evaluated and returned as a bool
#  @param p The current token
#  @brief This function allows for the conversion of the following tokens:
#         True, False, Modified. Modified is a special case that will have to
#         do a diff on the current version and the old version of the file.
#  @todo  Implement the modified function
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

## Parse
#  @pre  The expression should be valid. The expression needs to be a string
#  @post The expression is parsed and its bool value is evaluated
#  @param expression The expression as a string that is to be parsed
#  @retval bool Indicates the result of the evaluated string
#  @brief An expression string is evaluated for its boolean value and
#         then returned. The language is a simple scripting language.
def parse(expression):
  yacc.yacc()
  return bool(yacc.parse(expression))

## Validate
#  @pre  None
#  @post The validity of the expression is returned as a bool
#  @param expression The expression that is to be evaluated
#  @retval bool True indicates a valid expression, false indicates a bad expression
#  @brief  This function allows for the testing of an expression string's validity.
#          It will catch a bad parse and return it to the caller. This can be used
#          however is necessary, but it allows for an extra level of safety
def validate(expression):
  yacc.yacc()
  try:
    yacc.parse(expression)
    return True
  except:
    return False

# interface for testing the system
if __name__ == "__main__":
  exp = "3 days"
  if validate(exp):
    print("result", parse(exp))
  else:
    print("That was an invalid string")
