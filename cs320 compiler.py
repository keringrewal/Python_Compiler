
# Token Categories -- slightly different than in HW01 and HW 02

ident = 'id'          # used in token as (indent, <string> )    
integer = 'int'       #  (integer, <value> )
floating = 'float'    #  (floating, <value> )  
trueTok = 'True'
falseTok = 'False'
noneTok = "None"
plus = '+'            #  (plus,)    rest as this one, no attribute necessary
minus = '-'          
mult = '*'
div = '/' 
mod = '%'
exp = '**'
lparen = '('
rparen = ')'
lbrace = '['
rbrace = ']'
equals = '=='
assign = '='
colon = ':'
lt = '<'
gt = '>'
ge = '>='
le = '<='
ne = '!='
andTok = '&&'
orTok = '||'
notTok = '!'
defTok = 'def'
semicolon = ';'
comma = ','
let = 'let'
inTok = 'in'
ifTok = 'if'
thenTok = 'then'
elseTok = 'else'
lambdaTok = 'lambda'
apply = 'apply'
returnTok = 'return'
breakTok = 'break'
continueTok = 'continue'
nil = 'nil'
cons = 'cons'
first = 'first'
rest = 'rest'
whileTok = 'while'
leftCurlyBrace = '{'
rightCurlyBrace = '}'
returnTok = 'return'
printTok = 'print'
error = 'error'       #  (error, <string> )     gives spelling of token that caused the lexical error

token_list = [trueTok,
falseTok,
noneTok,
plus,
minus,       
mult,
div,
mod,
exp ,
lparen ,
rparen ,
lbrace ,
rbrace ,
equals ,
assign ,
colon ,
lt ,
gt ,
ge ,
le ,
ne ,
andTok ,
orTok ,
notTok ,
defTok ,
semicolon ,
comma ,
let ,
inTok ,
ifTok ,
thenTok ,
elseTok ,
lambdaTok ,
apply ,
returnTok ,
breakTok,
continueTok,
nil ,
cons ,
first ,
rest ,
whileTok ,
leftCurlyBrace ,
rightCurlyBrace ,
returnTok ,
printTok ,
error  ]

# special token for end of input

end_of_input = '$'       # (end_of_input,) will be pretty-printed as ($,)


def tokenToString(t):
    if t == None:
        return str(t)
    elif t[0] in ['int','float','id']:
        return '(' + t[0] + ',' + str(t[1]) + ')'
    else:
        return '(' + t[0] + ',)'
        
def tokenListToString(lst):
    res = '[ '
    for t in lst[:-1]:
        res = res + tokenToString(t) + ', '
    res = res + tokenToString(lst[-1]) + ' ]'
    return res


# Code for lexer

# put white space between each separator or operator token and split into words

def splitTokens(s):
    for t in ['+','-','*','/','(',')','[',']','{', '}',';',',','<', '&', '|',':', '>', '=', '!','%']:
        s = s.replace(t,' ' + t + ' ')
    # now repair two-character tokens
    s = s.replace('<  =','<=')
    s = s.replace('>  =','>=')
    s = s.replace('=  =','==')
    s = s.replace('!  =','!=')
    s = s.replace('*  *','**')
    s = s.replace('&  &','&&')
    s = s.replace('|  |','||')
    return s.split()

def isLetter(c):
    return 'a' <= c <= 'z' or 'A' <= c <= 'Z'

def isDigit(c):
    return '0' <= c <= '9' 

def isIdToken(s):
    state = 1
    for ch in s:
        if state == 1:
            if isLetter(ch) or ch == '_':
                state = 2
            else:
                return False
        elif state == 2:
            if isLetter(ch) or isDigit(ch) or ch == '_':
                state = 2
            else:
                return False
    return (state == 2)

                        
def isIntToken(s):
    if s == '0':
        return True
    state = 1
    for ch in s:
        if state == 1:
            if isDigit(ch) and ch != '0':
                state = 2
            else:
                return False
        elif state == 2:
            if isDigit(ch):
                state = 2
            else:
                return False
    return (state == 2)
    
def isFloatToken(s):
    state = 1
    finalStates = [4,6]
    for ch in s:
        if state == 1:
            if isDigit(ch) and ch != '0':
                state = 2
            elif ch == '0':
                state = 3
            elif ch == '.':
                state = 5
            else:
                return False
        elif state == 2:
            if isDigit(ch):
                state = 2
            elif ch == '.':
                state = 4
            else:
                return False
        elif state == 3:
            if ch == '.':
                state = 4
            else:
                return False
        elif state == 4:
            if isDigit(ch):
                state = 4
            else:
                return False
        elif state == 5:
            if isDigit(ch):
                state = 6
            else:
                return False
        elif state == 6:
            if isDigit(ch):
                state = 6
            else:
                return False                
                
    return (state in finalStates)   

def stringToToken(t):
    if t in token_list:
        return (t,)
    elif isIdToken(t):
        return (ident,t)
    elif isIntToken(t):
        return (integer,int(t)) 
    elif isFloatToken(t):
        return (floating,float(t)) 

    else:
        return (error,)

def lexer(s):
    return [stringToToken(t) for t in splitTokens(s)]

# Utilities for grammars

def rule_to_string(r):
    s = r[0][0] + ' := '
    for t in r[1]:
        s = s + t[0] + ' '
    return s
                          
def pprint_grammar(G): 
    for k in range(len(G)):
        print(str(k) + ": " + rule_to_string(G[k])) 
  
Grammar_HW07 =    [(('S',),(('Stmts',),)),          # program is a list of statements
         (('Stmts',),(('Stmt',),(';',), ('Stmts',))),    
         (('Stmts',),(('Stmt',),(';',))),
         (('Stmts',),(('Block',), ('Stmts',))),    
         (('Stmts',),(('Block',),)), 
         (('Stmt',),(('id',),('=',),('E',))),
         (('Stmt',),(('return',),('E',))), 
         (('Stmt',),(('print' ,),('E',))),
         (('Stmt',),(('break' ,),)),
         (('Stmt',),(('continue',),)),
         (('Stmt',),(('E',),)),
         (('Block',),(('Def',),('Block',))),   
         (('Def',),(('def',),('id',),('(',),(')',))),    
         (('Def',),(('def',),('id',),('(',),('id',),(')',))),  
         (('Def',),(('def',),('id',),('(',),('id',),(',',),('id',),(')',))), 
         (('Block',),(('{',),('Stmts',),('}',))), 
         (('Block',),(('While',),('WhileExpr',),('Block',))),
         (('WhileExpr',),(('(',),('Expr',),(')',))),
         (('While',),(('while',),)),
         (('Block',),(('IfHeader',),('Block',))),
         (('IfHeader',),(('if',),('(',),('Expr',),(')',))),
         (('Block',),(('IfHeader',),('Block',),('Else',),('Block',))), 
         (('Else',),(('else',),)),      
         (('Expr',),(('Bor',),)), 
         (('Bor',),(('BorBarBar',),('Band',))), 
         (('BorBarBar',),(('Bor',),('||',))), 
         (('Bor',),(('Band',),)),                   
         (('Band',),(('BandAmpAmp',),('Bnot',))),
         (('BandAmpAmp',),(('Band',),('&&',))),
         (('Band',),(('Bnot',),)),                 
         (('Bnot',),(('!',),('Bnot',))),          
         (('Bnot',),(('C',),)), 
         (('Bnot',),(('(',),('Bor',),(')',))),          
         (('C',),(('E',),('==',),('E',))),          
         (('C',),(('E',),('!=',),('E',))),          
         (('C',),(('E',),('<',),('E',))),            
         (('C',),(('E',),('<=',),('E',))),          
         (('C',),(('E',),('>',),('E',))),            
         (('C',),(('E',),('>=',),('E',))),                                  
         (('E',),(('E',),('+',),('T',))),           
         (('E',),(('E',),('-',),('T',))),           
         (('E',),(('T',),)),                       
         (('T',),(('T',),('*',),('F',))),          
         (('T',),(('T',),('/',),('F',))),          
         (('T',),(('T',),('%',),('F',))),          
         (('T',),(('F',),)),                       
         (('F',),(('-',),('F',))),                                                                                                                            
         (('F',),(('id',), ('(',),(')',),) ),
         (('F',),(('id',), ('(',), ('E',), (')',),) ),
         (('F',),(('id',), ('(',), ('E',), (',',),('E',), (')',),) ),
         (('F',),(('id',), ('(',), ('E',), (',',),('E',), (',',),('E',), (')',),) ),
         (('F',),(('id',),)),                      
         (('F',),(('int',),)),                    
         (('F',),(('float',),)),                    
         (('F',),(('(',),('E',),(')',))) ]        

# The parser DFA will tell you what to do when the stack is
# in a given configuration.  A positive number gives the
# state transition, a non-positive number k is a reduction by the
# rule -k, i.e., -4 means a reduction by rule 4 with no
# advance in the input string.  None is an error and
# 0 is accept. 

err = None
accept = 0

table = {
  0:{'else': None, '!': None, 'S': None, 'Stmt': 1, 'IfHeader': 2, '{': 3, 'break': 4, 'print': 6, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 7, 'Expr': None, 'id': 8, 'Def': 9, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': 12, 'Block': 13, 'continue': 14, 'if': 15, 'return': 16, 'float': 17, '<=': None, 'def': 18, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': 20, '&&': None, 'While': 21, ',': None, '>': None, '(': 22, '=': None},
  1:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': 23, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  2:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': 2, '{': 3, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': 9, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': 24, 'continue': None, 'if': 15, 'return': None, 'float': None, '<=': None, 'def': 18, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': 20, '&&': None, 'While': 21, ',': None, '>': None, '(': None, '=': None},
  3:{'else': None, '!': None, 'S': None, 'Stmt': 1, 'IfHeader': 2, '{': 3, 'break': 4, 'print': 6, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 7, 'Expr': None, 'id': 8, 'Def': 9, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': 25, 'Block': 13, 'continue': 14, 'if': 15, 'return': 16, 'float': 17, '<=': None, 'def': 18, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': 20, '&&': None, 'While': 21, ',': None, '>': None, '(': 22, '=': None},
  4:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': -8, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  5:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': 28, ';': -41, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': 27, '||': -41, '==': -41, '-': -41, '<': -41, 'Bnot': None, 'Bor': None, '+': -41, 'Band': None, '>=': -41, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -41, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': 26, 'int': None, 'C': None, '!=': -41, ')': -41, 'while': None, '&&': -41, 'While': None, ',': -41, '>': -41, '(': None, '=': None},
  6:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 29, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  7:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': -10, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 31, '<': None, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  8:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': -51, ';': -51, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': -51, '||': -51, '==': -51, '-': -51, '<': -51, 'Bnot': None, 'Bor': None, '+': -51, 'Band': None, '>=': -51, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -51, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': -51, 'int': None, 'C': None, '!=': -51, ')': -51, 'while': None, '&&': -51, 'While': None, ',': -51, '>': -51, '(': 33, '=': 34},
  9:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': 2, '{': 3, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': 9, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': 35, 'continue': None, 'if': 15, 'return': None, 'float': None, '<=': None, 'def': 18, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': 20, '&&': None, 'While': 21, ',': None, '>': None, '(': None, '=': None},
  10:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 36, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  11:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': -45, ';': -45, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': -45, '||': -45, '==': -45, '-': -45, '<': -45, 'Bnot': None, 'Bor': None, '+': -45, 'Band': None, '>=': -45, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -45, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': -45, 'int': None, 'C': None, '!=': -45, ')': -45, 'while': None, '&&': -45, 'While': None, ',': -45, '>': -45, '(': None, '=': None},
  12:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': 0, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  13:{'else': None, '!': None, 'S': None, 'Stmt': 1, 'IfHeader': 2, '{': 3, 'break': 4, 'print': 6, 'T': 5, '$': -4, 'BandAmpAmp': None, '/': None, ';': None, 'E': 7, 'Expr': None, 'id': 8, 'Def': 9, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': 37, 'Block': 13, 'continue': 14, 'if': 15, 'return': 16, 'float': 17, '<=': None, 'def': 18, '}': -4, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': 20, '&&': None, 'While': 21, ',': None, '>': None, '(': 22, '=': None},
  14:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': -9, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  15:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 38, '=': None},
  16:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 39, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  17:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': -53, ';': -53, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': -53, '||': -53, '==': -53, '-': -53, '<': -53, 'Bnot': None, 'Bor': None, '+': -53, 'Band': None, '>=': -53, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -53, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': -53, 'int': None, 'C': None, '!=': -53, ')': -53, 'while': None, '&&': -53, 'While': None, ',': -53, '>': -53, '(': None, '=': None},
  18:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': 40, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  19:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': -52, ';': -52, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': -52, '||': -52, '==': -52, '-': -52, '<': -52, 'Bnot': None, 'Bor': None, '+': -52, 'Band': None, '>=': -52, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -52, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': -52, 'int': None, 'C': None, '!=': -52, ')': -52, 'while': None, '&&': -52, 'While': None, ',': -52, '>': -52, '(': None, '=': None},
  20:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': -18, '=': None},
  21:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': 42, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 41, '=': None},
  22:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 43, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  23:{'else': None, '!': None, 'S': None, 'Stmt': 1, 'IfHeader': 2, '{': 3, 'break': 4, 'print': 6, 'T': 5, '$': -2, 'BandAmpAmp': None, '/': None, ';': None, 'E': 7, 'Expr': None, 'id': 8, 'Def': 9, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': 44, 'Block': 13, 'continue': 14, 'if': 15, 'return': 16, 'float': 17, '<=': None, 'def': 18, '}': -2, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': 20, '&&': None, 'While': 21, ',': None, '>': None, '(': 22, '=': None},
  24:{'else': 45, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': -19, 'break': -19, 'print': -19, 'T': None, '$': -19, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': -19, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': -19, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': -19, 'if': -19, 'return': -19, 'float': -19, '<=': None, 'def': -19, '}': -19, 'Else': 46, 'BorBarBar': None, '*': None, 'int': -19, 'C': None, '!=': None, ')': None, 'while': -19, '&&': None, 'While': None, ',': None, '>': None, '(': -19, '=': None},
  25:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': 47, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  26:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 48, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  27:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 49, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  28:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 50, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  29:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': -7, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 31, '<': None, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  30:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': -51, ';': -51, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': -51, '||': -51, '==': -51, '-': -51, '<': -51, 'Bnot': None, 'Bor': None, '+': -51, 'Band': None, '>=': -51, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -51, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': -51, 'int': None, 'C': None, '!=': -51, ')': -51, 'while': None, '&&': -51, 'While': None, ',': -51, '>': -51, '(': 33, '=': None},
  31:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 51, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  32:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 52, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  33:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 54, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': 53, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  34:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 55, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  35:{'else': -11, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': -11, 'break': -11, 'print': -11, 'T': None, '$': -11, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': -11, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': -11, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': -11, 'if': -11, 'return': -11, 'float': -11, '<=': None, 'def': -11, '}': -11, 'Else': None, 'BorBarBar': None, '*': None, 'int': -11, 'C': None, '!=': None, ')': None, 'while': -11, '&&': None, 'While': None, ',': None, '>': None, '(': -11, '=': None},
  36:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': -46, ';': -46, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': -46, '||': -46, '==': -46, '-': -46, '<': -46, 'Bnot': None, 'Bor': None, '+': -46, 'Band': None, '>=': -46, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -46, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': -46, 'int': None, 'C': None, '!=': -46, ')': -46, 'while': None, '&&': -46, 'While': None, ',': -46, '>': -46, '(': None, '=': None},
  37:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': -3, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': -3, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  38:{'else': None, '!': 56, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': 60, '/': None, ';': None, 'E': 63, 'Expr': 65, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': 58, 'Bor': 59, '+': None, 'Band': 62, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': 64, '*': None, 'int': 19, 'C': 57, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 61, '=': None},
  39:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': -6, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 31, '<': None, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  40:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 66, '=': None},
  41:{'else': None, '!': 56, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': 60, '/': None, ';': None, 'E': 63, 'Expr': 67, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': 58, 'Bor': 59, '+': None, 'Band': 62, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': 64, '*': None, 'int': 19, 'C': 57, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 61, '=': None},
  42:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': 2, '{': 3, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': 9, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': 68, 'continue': None, 'if': 15, 'return': None, 'float': None, '<=': None, 'def': 18, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': 20, '&&': None, 'While': 21, ',': None, '>': None, '(': None, '=': None},
  43:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 31, '<': None, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': 69, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  44:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': -1, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': -1, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  45:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': -22, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': -22, 'return': None, 'float': None, '<=': None, 'def': -22, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': -22, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  46:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': 2, '{': 3, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': 9, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': 70, 'continue': None, 'if': 15, 'return': None, 'float': None, '<=': None, 'def': 18, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': 20, '&&': None, 'While': 21, ',': None, '>': None, '(': None, '=': None},
  47:{'else': -15, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': -15, 'break': -15, 'print': -15, 'T': None, '$': -15, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': -15, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': -15, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': -15, 'if': -15, 'return': -15, 'float': -15, '<=': None, 'def': -15, '}': -15, 'Else': None, 'BorBarBar': None, '*': None, 'int': -15, 'C': None, '!=': None, ')': None, 'while': -15, '&&': None, 'While': None, ',': None, '>': None, '(': -15, '=': None},
  48:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': -42, ';': -42, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': -42, '||': -42, '==': -42, '-': -42, '<': -42, 'Bnot': None, 'Bor': None, '+': -42, 'Band': None, '>=': -42, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -42, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': -42, 'int': None, 'C': None, '!=': -42, ')': -42, 'while': None, '&&': -42, 'While': None, ',': -42, '>': -42, '(': None, '=': None},
  49:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': -44, ';': -44, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': -44, '||': -44, '==': -44, '-': -44, '<': -44, 'Bnot': None, 'Bor': None, '+': -44, 'Band': None, '>=': -44, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -44, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': -44, 'int': None, 'C': None, '!=': -44, ')': -44, 'while': None, '&&': -44, 'While': None, ',': -44, '>': -44, '(': None, '=': None},
  50:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': -43, ';': -43, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': -43, '||': -43, '==': -43, '-': -43, '<': -43, 'Bnot': None, 'Bor': None, '+': -43, 'Band': None, '>=': -43, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -43, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': -43, 'int': None, 'C': None, '!=': -43, ')': -43, 'while': None, '&&': -43, 'While': None, ',': -43, '>': -43, '(': None, '=': None},
  51:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': 28, ';': -40, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': 27, '||': -40, '==': -40, '-': -40, '<': -40, 'Bnot': None, 'Bor': None, '+': -40, 'Band': None, '>=': -40, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -40, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': 26, 'int': None, 'C': None, '!=': -40, ')': -40, 'while': None, '&&': -40, 'While': None, ',': -40, '>': -40, '(': None, '=': None},
  52:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': 28, ';': -39, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': 27, '||': -39, '==': -39, '-': -39, '<': -39, 'Bnot': None, 'Bor': None, '+': -39, 'Band': None, '>=': -39, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -39, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': 26, 'int': None, 'C': None, '!=': -39, ')': -39, 'while': None, '&&': -39, 'While': None, ',': -39, '>': -39, '(': None, '=': None},
  53:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': -47, ';': -47, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': -47, '||': -47, '==': -47, '-': -47, '<': -47, 'Bnot': None, 'Bor': None, '+': -47, 'Band': None, '>=': -47, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -47, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': -47, 'int': None, 'C': None, '!=': -47, ')': -47, 'while': None, '&&': -47, 'While': None, ',': -47, '>': -47, '(': None, '=': None},
  54:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 31, '<': None, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': 72, 'while': None, '&&': None, 'While': None, ',': 71, '>': None, '(': None, '=': None},
  55:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': -5, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 31, '<': None, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  56:{'else': None, '!': 56, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 63, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': 73, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': 57, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 61, '=': None},
  57:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': -31, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': -31, 'while': None, '&&': -31, 'While': None, ',': None, '>': None, '(': None, '=': None},
  58:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': -29, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': -29, 'while': None, '&&': -29, 'While': None, ',': None, '>': None, '(': None, '=': None},
  59:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': 74, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': -23, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  60:{'else': None, '!': 56, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 63, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': 75, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': 57, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 61, '=': None},
  61:{'else': None, '!': 56, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': 60, '/': None, ';': None, 'E': 77, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': 58, 'Bor': 76, '+': None, 'Band': 62, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': 64, '*': None, 'int': 19, 'C': 57, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 61, '=': None},
  62:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': -26, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': -26, 'while': None, '&&': 78, 'While': None, ',': None, '>': None, '(': None, '=': None},
  63:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': 80, '-': 31, '<': 81, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': 83, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': 82, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': 79, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': 84, '(': None, '=': None},
  64:{'else': None, '!': 56, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': 60, '/': None, ';': None, 'E': 63, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': 58, 'Bor': None, '+': None, 'Band': 85, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': 57, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 61, '=': None},
  65:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': 86, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  66:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': 87, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': 88, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  67:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': 89, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  68:{'else': -16, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': -16, 'break': -16, 'print': -16, 'T': None, '$': -16, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': -16, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': -16, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': -16, 'if': -16, 'return': -16, 'float': -16, '<=': None, 'def': -16, '}': -16, 'Else': None, 'BorBarBar': None, '*': None, 'int': -16, 'C': None, '!=': None, ')': None, 'while': -16, '&&': None, 'While': None, ',': None, '>': None, '(': -16, '=': None},
  69:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': -54, ';': -54, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': -54, '||': -54, '==': -54, '-': -54, '<': -54, 'Bnot': None, 'Bor': None, '+': -54, 'Band': None, '>=': -54, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -54, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': -54, 'int': None, 'C': None, '!=': -54, ')': -54, 'while': None, '&&': -54, 'While': None, ',': -54, '>': -54, '(': None, '=': None},
  70:{'else': -21, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': -21, 'break': -21, 'print': -21, 'T': None, '$': -21, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': -21, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': -21, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': -21, 'if': -21, 'return': -21, 'float': -21, '<=': None, 'def': -21, '}': -21, 'Else': None, 'BorBarBar': None, '*': None, 'int': -21, 'C': None, '!=': None, ')': None, 'while': -21, '&&': None, 'While': None, ',': None, '>': None, '(': -21, '=': None},
  71:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 90, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  72:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': -48, ';': -48, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': -48, '||': -48, '==': -48, '-': -48, '<': -48, 'Bnot': None, 'Bor': None, '+': -48, 'Band': None, '>=': -48, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -48, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': -48, 'int': None, 'C': None, '!=': -48, ')': -48, 'while': None, '&&': -48, 'While': None, ',': -48, '>': -48, '(': None, '=': None},
  73:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': -30, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': -30, 'while': None, '&&': -30, 'While': None, ',': None, '>': None, '(': None, '=': None},
  74:{'else': None, '!': -25, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': -25, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': -25, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': -25, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': -25, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': -25, '=': None},
  75:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': -27, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': -27, 'while': None, '&&': -27, 'While': None, ',': None, '>': None, '(': None, '=': None},
  76:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': 74, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': 91, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  77:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': 80, '-': 31, '<': 81, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': 83, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': 82, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': 79, ')': 69, 'while': None, '&&': None, 'While': None, ',': None, '>': 84, '(': None, '=': None},
  78:{'else': None, '!': -28, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': -28, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': -28, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': -28, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': -28, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': -28, '=': None},
  79:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 92, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  80:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 93, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  81:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 94, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  82:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 95, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  83:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 96, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  84:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 97, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  85:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': -24, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': -24, 'while': None, '&&': 78, 'While': None, ',': None, '>': None, '(': None, '=': None},
  86:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': -20, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': -20, 'return': None, 'float': None, '<=': None, 'def': -20, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': -20, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  87:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': 99, 'while': None, '&&': None, 'While': None, ',': 98, '>': None, '(': None, '=': None},
  88:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': -12, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': -12, 'return': None, 'float': None, '<=': None, 'def': -12, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': -12, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  89:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': -17, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': -17, 'return': None, 'float': None, '<=': None, 'def': -17, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': -17, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  90:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 31, '<': None, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': 101, 'while': None, '&&': None, 'While': None, ',': 100, '>': None, '(': None, '=': None},
  91:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': -32, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': -32, 'while': None, '&&': -32, 'While': None, ',': None, '>': None, '(': None, '=': None},
  92:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': -34, '==': None, '-': 31, '<': None, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': -34, 'while': None, '&&': -34, 'While': None, ',': None, '>': None, '(': None, '=': None},
  93:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': -33, '==': None, '-': 31, '<': None, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': -33, 'while': None, '&&': -33, 'While': None, ',': None, '>': None, '(': None, '=': None},
  94:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': -35, '==': None, '-': 31, '<': None, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': -35, 'while': None, '&&': -35, 'While': None, ',': None, '>': None, '(': None, '=': None},
  95:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': -36, '==': None, '-': 31, '<': None, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': -36, 'while': None, '&&': -36, 'While': None, ',': None, '>': None, '(': None, '=': None},
  96:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': -38, '==': None, '-': 31, '<': None, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': -38, 'while': None, '&&': -38, 'While': None, ',': None, '>': None, '(': None, '=': None},
  97:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': -37, '==': None, '-': 31, '<': None, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': -37, 'while': None, '&&': -37, 'While': None, ',': None, '>': None, '(': None, '=': None},
  98:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': 102, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  99:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': -13, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': -13, 'return': None, 'float': None, '<=': None, 'def': -13, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': -13, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  100:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': 5, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': 103, 'Expr': None, 'id': 30, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 10, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': 11, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': 17, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': 19, 'C': None, '!=': None, ')': None, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': 22, '=': None},
  101:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': -49, ';': -49, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': -49, '||': -49, '==': -49, '-': -49, '<': -49, 'Bnot': None, 'Bor': None, '+': -49, 'Band': None, '>=': -49, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -49, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': -49, 'int': None, 'C': None, '!=': -49, ')': -49, 'while': None, '&&': -49, 'While': None, ',': -49, '>': -49, '(': None, '=': None},
  102:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': 104, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  103:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': 31, '<': None, 'Bnot': None, 'Bor': None, '+': 32, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': None, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': 105, 'while': None, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  104:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': -14, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': None, ';': None, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': None, '||': None, '==': None, '-': None, '<': None, 'Bnot': None, 'Bor': None, '+': None, 'Band': None, '>=': None, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': -14, 'return': None, 'float': None, '<=': None, 'def': -14, '}': None, 'Else': None, 'BorBarBar': None, '*': None, 'int': None, 'C': None, '!=': None, ')': None, 'while': -14, '&&': None, 'While': None, ',': None, '>': None, '(': None, '=': None},
  105:{'else': None, '!': None, 'S': None, 'Stmt': None, 'IfHeader': None, '{': None, 'break': None, 'print': None, 'T': None, '$': None, 'BandAmpAmp': None, '/': -50, ';': -50, 'E': None, 'Expr': None, 'id': None, 'Def': None, 'WhileExpr': None, '%': -50, '||': -50, '==': -50, '-': -50, '<': -50, 'Bnot': None, 'Bor': None, '+': -50, 'Band': None, '>=': -50, 'F': None, 'Stmts': None, 'Block': None, 'continue': None, 'if': None, 'return': None, 'float': None, '<=': -50, 'def': None, '}': None, 'Else': None, 'BorBarBar': None, '*': -50, 'int': None, 'C': None, '!=': -50, ')': -50, 'while': None, '&&': -50, 'While': None, ',': -50, '>': -50, '(': None, '=': None}
}


def action(lst,table):
    state = 0
    for token in lst:      
        try:
            state = table[state][token[0]]
        except KeyError:
            return err          
        if state == err:        # error state is implicit so fail as soon as you hit an error
            return err
    return state


def instruction_to_string(k,instruction):
    if (len(instruction) == 4):
        (op,(_,dest),(_,src1),(_,src2)) = instruction
        return (str(k) + ": " + dest + " = " + str(src1) + " " + op + " " + str(src2))
    elif instruction[0] == 'uminus':
        return (str(k) + ": " + instruction[1][1] + " = - " + str(instruction[2][1]))
    elif instruction[0] == '!':
        return (str(k) + ": " + instruction[1][1] + " = ! " + str(instruction[2][1]))
    elif instruction[0] == '=':
        return (str(k) + ": " + instruction[1][1] + " = " + str(instruction[2][1]))
    elif instruction[0] == 'jump':
        return (str(k) + ": " + "jump " + str(instruction[1]))
    elif instruction[0] == 'bzero':
        return (str(k) + ": " + "bzero " + str(instruction[1][1]) + " " + str(instruction[2]))
    elif instruction[0] == 'call':
        return (str(k) + ": " + "call " + str(instruction[1])) 
    elif instruction[0] == 'push':
        return (str(k) + ": " + "push " ) 
    elif instruction[0] == 'ret':
        return (str(k) + ": " + "ret " + str(instruction[1][1]))    
    elif instruction[0] == 'print':
        return (str(k) + ": " + "print \"" + str(instruction[1]) + "\" " + str(instruction[2][1]))
    else:
        return (str(k) + ": Unknown Instruction!")

def pprint_program(P):
    print("Program:\n")
    for k in range(len(P)):
        print(instruction_to_string(k,P[k]))
        

# Lookup takes a constant and or variable in form ('id',...) and, if a variables, and attempts 
# to find a value, first checking RTS frames (which are dictionaries) from top down, then
# the global Mem; if not found prints error and returns None. 

def lookup(var,Mem,RTS):
    #print("lookup: " + str(var) + " " + str(Mem) + " " + str(RTS))
    if var[0] == 'int' or var[0] == 'float':
        return int(var[1])
    elif var[0] == 'id':
        for k in range(len(RTS)-1, -1, -1):    # look down the stack from top to bottom
            if var[1] in RTS[k]:
                return RTS[k][var[1]]
        if var[1] in Mem:
            return Mem[var[1]]
        else:
            print("Unbound variable:" + str(var))
            return None
    else:
        print("Unbound object:" + str(var))
        return None
        

def execute(Code,Memory,Verbose=False):
    
    # program counter holding index of next instruction to execute
    PC = 0
    
    # Run-Time Stack to hold data for function calls; is a stack of dictionaries
    RTS = []
    
    if Verbose:
        print("Execution Trace:")
        print()
        print("Instruction\t\tMemory\t\tRun-Time Stack")
    else:
        print("Execution:\n")
            
    while( PC < len(Code) ):     # when run off end of list, halt program
        if Verbose:
            print("\t\t\t" + str(Memory))  
            print("\t\t\t\t\t" + str(RTS)) 
            print(instruction_to_string(PC,Code[PC]))
            
        instruction = Code[PC]
        PC += 1
        # parse instruction
        if len(instruction) == 4:   # binary operation
            (op,dest,src1,src2) = instruction
            if op == '+': 
                RTS[-1][dest[1]] = lookup(src1,Memory,RTS) + lookup(src2,Memory,RTS)
            elif op == '-': 
                RTS[-1][dest[1]] = lookup(src1,Memory,RTS) - lookup(src2,Memory,RTS)
            elif op == '*': 
                RTS[-1][dest[1]] = lookup(src1,Memory,RTS) * lookup(src2,Memory,RTS)
            elif op == '/': 
                RTS[-1][dest[1]] = lookup(src1,Memory,RTS) / lookup(src2,Memory,RTS)
            elif op == '%': 
                RTS[-1][dest[1]] = lookup(src1,Memory,RTS) % lookup(src2,Memory,RTS)
            elif op == '<': 
                RTS[-1][dest[1]] = int(lookup(src1,Memory,RTS) < lookup(src2,Memory,RTS))
            elif op == '>': 
                RTS[-1][dest[1]] = int(lookup(src1,Memory,RTS) > lookup(src2,Memory,RTS))
            elif op == '>=': 
                RTS[-1][dest[1]] = int(lookup(src1,Memory,RTS) >= lookup(src2,Memory,RTS))
            elif op == '<=': 
                RTS[-1][dest[1]] = int(lookup(src1,Memory,RTS) <= lookup(src2,Memory,RTS))
            elif op == '==': 
                RTS[-1][dest[1]] = int(lookup(src1,Memory,RTS) == lookup(src2,Memory,RTS))
            elif op == '!=': 
                RTS[-1][dest[1]] = int(lookup(src1,Memory,RTS) != lookup(src2,Memory,RTS))
        elif instruction[0] == 'uminus':
            RTS[-1][instruction[1][1]] = - lookup(instruction[2],RMemory,RTS) 
        elif instruction[0] == '=':
            RTS[-1][instruction[1][1]] = lookup(instruction[2],Memory,RTS) 
        elif instruction[0] == 'jump':
            PC = instruction[1]
        elif instruction[0] == 'bzero':
            if lookup(instruction[1],Memory,RTS) == 0:
                PC = instruction[2]
        elif instruction[0] == 'push':      # put another stack frame on the run-time stack
            RTS.append( { } )
        elif instruction[0] == 'call':      # like a jump but first store return address in current stack frame
            RTS[-1]['_ret_addr'] = PC 
            PC = instruction[1]
        elif instruction[0] == 'ret':       # return to return address after the original call and pop stack frame
            PC = lookup( ('id','_ret_addr'),Memory,RTS)
            if len(RTS) == 1:
                RTS.pop()
            elif len(RTS) > 1:     # put return value in stack frame of CALLER
                RTS[-2]['_ret_val'] = lookup(instruction[1],Memory,RTS)
                RTS.pop()
                 
        elif instruction[0] == 'print':
            print(instruction[1] + str(lookup(instruction[2],Memory,RTS)))
        else:
            print("Illegal instruction" + str(instruction))
    
    if Verbose:
            print("\t\t\t" + str(Memory))  
            print("\t\t\t\t\t" + str(RTS)) 


# Code for shift-reduce parser

# pretty-printing parser configurations

def pprint_parser(parsingStack,inputListOfTokens):
    totalWidth = 80
    smallestGap = 6
    largestStackLength = int(totalWidth*0.6 - smallestGap/2)   # most characters to display
    largestInputLength = totalWidth - largestStackLength - smallestGap
    
    p = '| '
    for symbol in parsingStack:
        p = p + tokenToString(symbol) + ' '
    if len(p) > largestStackLength:
        ind = int(len(p) - largestStackLength + 9)
        p = '| ... ' + p[ind:]
        
    q = ""
    for tok in inputListOfTokens[:-1]:
        q = q + tokenToString(tok) + ' '
    if len(inputListOfTokens) > 0:
        q = q + tokenToString(inputListOfTokens[-1]) 

    if len(q) > largestInputLength:
        ind = int(largestInputLength - 9)
        q = q[:ind] + ' ... ' 
    
    q = q + ' |'
        
    p = p + (' ' * (totalWidth - len(p) - len(q)))
    print(p+q)
    
    
# Generate a new temporary variable

count = 0
stack = []

def reset():
    global stack
    global count
    stack = []
    count = 0

def getTemp():
    if stack == []:
        global count
        count += 1
        return ('id', '_t' + str(count))
    else:
        return stack.pop()
    
def freeTemp(tmp):
    stack.append(tmp)
    
def isTemp(v):
    return v[0] == 'id' and v[1][0] == '_'

# go to jumps or bzeros at addresses in lst and put in addr as target
# will also work if lst is an integer and not a list

def backpatch(lst,addr,Code):
    #print(str(lst) + " " + str(addr) + " " + str(Code))
    if type(lst) == int:
        lst = [ lst ]
    for n in lst:
        if(Code[n][0] == 'jump'):
            Code[n] = ('jump',addr)
        elif(Code[n][0] == 'call'):
            Code[n] = ('call',addr)
        elif(Code[n][0] == 'bzero'):
            Code[n] = ('bzero',Code[n][1], addr)
        else:
            print("Error in backpatching at address: " + str(n))
            
# Dictionary to hold information about functions (starting location and parameter list)

symbol_table = {}

# total hack: check if assignment statement is in global scope if stack does not contain 'Def' tuple;
# better way is to rewrite grammar, but didn't want to change Lab 07 grammar for HW 07

def isGlobal(stack):
    for t in stack:
        if t[0] == 'Def':
            return False
    return True


# parse takes a list of tokens and determines if it is a 
# well-formed arithmetic expression. 


def parse(list_of_input_tokens,rules,table, verbose=False):

    reset()
    
    # start with a pushing stack frame for main on RTS, then store
    # return address of main (length of Code + 1), then
    # jump to main() function, both to be backpatched when parse main()
    
    Code = [('push',),('call',None),('jump',None)] 
    
    M = {}
    
    # add end of input marker
    list_of_input_tokens.append( (end_of_input,) )
    
    # input stack; use pop(0) to remove front item in list
    input_stack = list_of_input_tokens
    
    # parsing stack; use append to push onto end and pop() to pop from end
    parsing_stack = []
    
    if verbose:
        print('Input Tokens: ' + tokenListToString(input_stack) + '\n')
        pprint_parser(parsing_stack,input_stack) 
    
    while( len(input_stack) > 0 ):
        
        n = action(parsing_stack+[input_stack[0]],table)
        
        if n == accept:   # reduce by start rule, success
            if verbose:
                print("\nAccept!")
            if 'main' in symbol_table:
                (start,) = symbol_table['main']
            else:
                print('Warning: no main method defined!')

            backpatch(1,start,Code)               # backpatch start of main to call in line 1
            backpatch(2,len(Code),Code)           # halt, jump to past end of Code list
            
            return (Code,M) 
        elif n == err:     #  problem on stack!
            if verbose:
                print("\nERROR: No transition here:")
                pprint_parser(parsing_stack,input_stack)
            return None
        elif n > 0:     # shift 
            if verbose:
                print('\naction: ' + str(n) + '\tshift\n')
            parsing_stack.append( input_stack.pop(0)) 
        else:         # reduce by rule -n 
            if verbose:
                print('\naction: ' + str(n) + '\treduce by rule ' + str(-n) + ': ' + rule_to_string(rules[-n])+'\n')
            r = -n
            LHS = rules[r][0]
            
            # todo: put your code from lab 07 here for rules 1 - 4
            if r == 1:                                   # Stmts := Stmt ; Stmts
                (_, blist2, clist2) = parsing_stack.pop() # Stmts
                parsing_stack.pop()                      # ;
                (_, blist1, clist1) = parsing_stack.pop() # Stmt
                
                parsing_stack.append((LHS[0], blist1 + blist2, clist1 + clist2))
                
            elif r == 2:                                 # Stmts := Stmt ;
                parsing_stack.pop()                      # ;
                (_, blist, clist) = parsing_stack.pop()   # Stmt
                parsing_stack.append( (LHS[0], blist, clist) )
            elif r == 3: 
                
                (_, blist2, clist2) = parsing_stack.pop() # stmts
                (_, blist1, clist1) = parsing_stack.pop() # Block

                parsing_stack.append( (LHS[0], blist1+ blist2, clist1 + clist2))
            elif r == 4:                                 # Stmts := Block  
                (_, blist, clist) = parsing_stack.pop()   # Block
                parsing_stack.append( (LHS[0], blist, clist) )
            
            # rule 5 uses the hack for globals, leave it alone unless you know what you are doing....
            elif r == 5:                                 # Stmt := id = E
                (_,src) = parsing_stack.pop()            # Expr
                if isTemp(src):
                    freeTemp(src)
                parsing_stack.pop()                      # =
                dest = parsing_stack.pop()               # id
                if isGlobal(parsing_stack):      # if this is in global scope just add to memory
                    M[dest[1]] = src[1]          # RHS can only be an integer
                else:
                    Code.append( ('=',dest,src) )
                parsing_stack.append( (LHS[0],[],[]) ) 

            # todo: your code here from lab 07 for rules 6 - 10
            elif r == 6:                               # Stmt := return E
                (_,src) = parsing_stack.pop()          # E
                parsing_stack.pop()                    # return
                Code.append( ('ret',src) )
                parsing_stack.append( (LHS[0],[],[]) )
            elif r == 7:                               # Stmt := print E
                (_,src) = parsing_stack.pop()          # E
                parsing_stack.pop()                    # print
                if src[0] == 'id':
                    Code.append( ('print', src[1] + " = ", src) )
                else:
                    Code.append( ('print', "", src) )
                parsing_stack.append( (LHS[0],[],[]) )
            elif r == 8:                               # Stmt := break
                parsing_stack.pop()               # break
                Code.append( ('jump', None) ) 
                parsing_stack.append( (LHS[0], [len(Code)-1], []) )
            elif r == 9:                               # Stmt := continue
                parsing_stack.pop()                # continue
                Code.append( ('jump', None) )
                parsing_stack.append( (LHS[0], [], [len(Code)-1]) )
            elif r == 10:                              # Stmt := E
                parsing_stack.pop()                    # E
                parsing_stack.append( (LHS[0],[],[]) )
                
            # function definitions
            elif r == 11:                              # Block := Def Block
                parsing_stack.pop()                    # Block
                parsing_stack.pop()                    # Def
                parsing_stack.append( (LHS[0],[],[]) )
            elif r == 12:                              # Def := def id () 
                parsing_stack.pop()                    # )
                parsing_stack.pop()                    # (
                (_, name) = parsing_stack.pop()            # id
                parsing_stack.pop()                    # def
                start = len(Code)
                symbol_table[name] = (start,)
                parsing_stack.append( (LHS[0],None ) )
            elif r == 13:                              # Def := def id (id) 
                parsing_stack.pop()                    # )
                param = parsing_stack.pop()             # id
                parsing_stack.pop()                    # (
                (_, name) = parsing_stack.pop()            # id
                parsing_stack.pop()                   # def
                start = len(Code)
                symbol_table[name] = (start, param)
                parsing_stack.append( (LHS[0],None) )
            elif r == 14:                              # Def := def id (id,id) 
                parsing_stack.pop()                    # )
                param2 = parsing_stack.pop()             # id
                parsing_stack.pop()                    # ,
                param1 = parsing_stack.pop()             # id
                parsing_stack.pop()                    # (
                (_, name) = parsing_stack.pop()            # id
                parsing_stack.pop()                    # def
                start = len(Code)
                symbol_table[name] = (start, param1, param2)
                parsing_stack.append( (LHS[0],None) )                  
            
            # todo: your code here from Lab07 for rules 15 - 47
            elif r == 15:                                # Block := { Stmts }
                parsing_stack.pop()                      # }
                (_,blist,clist)  = parsing_stack.pop()   # Stmts
                parsing_stack.pop()                      # {
                parsing_stack.append( (LHS[0],blist,clist) ) 
                
            # while loop
            elif r == 16:                             # Block := While WhileExpr Block
                (_, blist, clist) = parsing_stack.pop() # Block
                (_, _, flist) = parsing_stack.pop()     # WhileExpr
                (_,start_addr) = parsing_stack.pop()  # While

                Code.append( ('jump', start_addr) )   # generate jump instruction
                backpatch(blist+flist, len(Code), Code)
                backpatch(clist, start_addr, Code)
                
                parsing_stack.append( (LHS[0], [], []) ) 
            elif r == 17:                              # WhileExpr := ( Expr )
                parsing_stack.pop()                   # )
                (_, tlist, flist) = parsing_stack.pop()         # Expr
                parsing_stack.pop()                   # (
                backpatch(tlist, len(Code), Code)
                parsing_stack.append( (LHS[0], [], flist))
                
            elif r == 18:                             # While := while
                parsing_stack.pop()                # while
                parsing_stack.append( (LHS[0], len(Code)) ) # store start of while loop in While
                

            # if statement
            elif r == 19:                             # Block := IfHeader Block
                (_, blist, clist) = parsing_stack.pop() # Block
                (_, _, flist) = parsing_stack.pop()    # IfHeader 
                backpatch(flist, len(Code), Code)
                parsing_stack.append( (LHS[0], blist, clist) ) 
            elif r == 20:                             # IfHeader := if ( Expr )
                parsing_stack.pop()                   # )
                (_, tlist, flist) = parsing_stack.pop() # Expr:  retrieve tlist and flist
                parsing_stack.pop()                   # (
                parsing_stack.pop()                   # if
                backpatch(tlist, len(Code), Code)
                parsing_stack.append( (LHS[0],[],flist) )   
            # if-then-else statement
            elif r == 21:                               # Block := IfHeader Block Else Block
                (_, blist1, clist1) = parsing_stack.pop() # Block
                (_,jump_addr) = parsing_stack.pop()     # Else 
                (_, blist2, clist2) = parsing_stack.pop() # Block
                (_, tlist, flist) = parsing_stack.pop()       # IfHeader 
                
                blist = blist1 + blist2
                clist = clist1 + clist2
                backpatch(jump_addr, len(Code), Code)
                backpatch(flist, jump_addr+1, Code)
                parsing_stack.append( (LHS[0],blist,clist) ) 
            elif r == 22:                             # Else := else
                parsing_stack.pop()                   # else 
                jaddr = len(Code)
                Code.append( ('jump', None) )         # generate jump instruction
                parsing_stack.append( (LHS[0], jaddr ))   # store address in Else 
            elif r in [23,26,29,31]:                      #  Expr := Bor | Bor := Band 
                                                          # Band := Bnot | Bnot := C
                (_, tlist, flist) = parsing_stack.pop()                      
                parsing_stack.append( (LHS[0], tlist, flist) )  # pass up the lists
            elif r in [24,27]:                            # Bor := BorBarBar Band  |
                                                          # Band := BandAmpAmp Bnot
                (_, tlist1, flist1) = parsing_stack.pop()   # Band or Bnot
                (_, tlist2, flist2) = parsing_stack.pop()   # BorBarBar |  BandAmpAmp
                tlist = tlist1 + tlist2
                flist = flist1 + flist2
                parsing_stack.append( (LHS[0],tlist,flist) )
            elif r == 25:                                 # BorBarBar := Bor ||
                parsing_stack.pop()                       # || 
                (_, tlist, flist) = parsing_stack.pop()     # Bor
                backpatch(flist, len(Code), Code)
                parsing_stack.append( (LHS[0],tlist,[]) )
            elif r == 28:                                 # BandAmpAmp := Band &&
                parsing_stack.pop()                       # &&
                (_, tlist, flist) = parsing_stack.pop()     # Band
                backpatch(tlist, len(Code), Code)
                parsing_stack.append( (LHS[0],[], flist) )
            elif r in [30]:                               # Bnot := ! Bnot
                (_, tlist, flist) = parsing_stack.pop()     # Bnot 
                parsing_stack.pop()                       # ! 
                parsing_stack.append( (LHS[0],flist,tlist) )  
            elif r == 32:                                 #  Bnot := ( Bor )
                parsing_stack.pop()                       # )
                (_, tlist, flist) = parsing_stack.pop()     # Bor
                parsing_stack.pop()                       # (
                parsing_stack.append( (LHS[0],tlist,flist) )  
                
            elif r in [33,34,35,36,37,38]:               # relational ops
                (_,src2) = parsing_stack.pop()           # E                
                (operator,) = parsing_stack.pop()        # op
                (_,src1) = parsing_stack.pop()           # E
                if isTemp(src1):
                    freeTemp(src1)
                if isTemp(src2):
                    freeTemp(src2)
                dest = getTemp()
                Code.append( (operator,dest,src1,src2) )
                
                
                # generate the bzero and jump here and store in lists flist and tlist
                addr = len(Code)
                Code.append(('bzero', dest, None))
                addr2 = len(Code)
                Code.append(('jump', dest, None))
                parsing_stack.append((LHS[0], [addr2], [addr]))
            # Nothing needs to be changed in the rest of the function below here
            
            elif r in [39,40,42,43,44]:                   # binary arith ops
                (_,src2) = parsing_stack.pop()                  
                (operator,) = parsing_stack.pop()
                (_,src1) = parsing_stack.pop()
                if isTemp(src1):
                    freeTemp(src1)
                if isTemp(src2):
                    freeTemp(src2)
                dest = getTemp()
                Code.append( (operator,dest,src1,src2) )
                parsing_stack.append( (LHS[0],dest) )
            elif r in [41,45]:                            # Unary arith expr rules just pass attributes up
                (_,loc) = parsing_stack.pop()
                parsing_stack.append( (LHS[0],loc) ) 
            elif r == 46:                              # unary minus
                (_,src) = parsing_stack.pop()          # F  
                parsing_stack.pop()                    # -
                if isTemp(src):
                    freeTemp(src)
                dest = getTemp()
                Code.append( ('uminus',dest,src) )
                parsing_stack.append( (LHS[0],dest) )
                
            # function calls
            elif r == 47:                              # F := id ()
                parsing_stack.pop()                    # ) 
                parsing_stack.pop()                    # (
                (_, name) = parsing_stack.pop()            # id
                Code.append(('push',))
                addr = symbol_table[name]
                
                Code.append(('call', addr))
                
                dest = getTemp()
                Code.append(('=', dest, ('id', '_ret_val')))
                
                parsing_stack.append( (LHS[0], dest) )
            elif r == 48:                              # F := id ( Expr )
                parsing_stack.pop()                    # ) 
                (_,loc) = parsing_stack.pop()          # Expr
                parsing_stack.pop()                    # (
                (_, name) = parsing_stack.pop()            # id
                Code.append(('push',))
                (addr, param) = symbol_table[name]
                
                Code.append(('=', param, loc))
                Code.append(('call', addr))
                
                dest = getTemp()
                Code.append(('=', dest, ('id', '_ret_val')))
                
                parsing_stack.append( (LHS[0], dest) )
            elif r == 49:                              # F := id ( Expr, Expr )
                parsing_stack.pop()                    # ) 
                (_, loc2) = parsing_stack.pop()         # Expr
                parsing_stack.pop()                    # , 
                (_, loc1) = parsing_stack.pop()         # Expr
                parsing_stack.pop()                    # (
                (_, name) = parsing_stack.pop()                    # id
                Code.append(('push',))
                (addr, param1, param2) = symbol_table[name]
                
                Code.append(('=', param2, loc2))
                Code.append(('=', param1, loc1))
                Code.append(('call', addr))
                
                dest = getTemp()
                Code.append(('=', dest, ('id', '_ret_val')))
                
                parsing_stack.append( (LHS[0],dest ) )
            # NOTE: this next rule will never be used, but left in to avoid renumbering remaining rules
            elif r == 50:                              # id ( Expr, Expr, Expr )
                parsing_stack.pop()                    # ) 
                parsing_stack.pop()         # Expr
                parsing_stack.pop()                    # , 
                parsing_stack.pop()         # Expr
                parsing_stack.pop()                    # , 
                parsing_stack.pop()         # Expr
                parsing_stack.pop()                    # (
                parsing_stack.pop()       # id              
                
                parsing_stack.append( (LHS[0],None) )
            elif r in [51,52,53]:                      # F := id | int | float 
                name = parsing_stack.pop()
                parsing_stack.append( (LHS[0],name) )  # create location to pass up tree
            elif r in [54]:                            # F := ( E )   just pass location up
                parsing_stack.pop()                    # )
                (_,loc) = parsing_stack.pop()          # E
                parsing_stack.pop()                    # (
                parsing_stack.append( (LHS[0],loc) )
            else:
                print("parse stack error: action " + str(n))
                return None
   
        if verbose:
            pprint_parser(parsing_stack,input_stack)
            
    return (Code,M)     # this will never be executed
    

def test(P,M,verbose=False):
    if(P == None):
        print("Syntax error in program!")
    else:
        pprint_program(P)
        print()
        print('Memory: ' + str(M))
        print()
        execute(P,M,verbose)


# Test 1: basic function call and global variable

s = '''

a = 5;

def succ(x) {
    z = x + 1;
    return z;
}

def main() {
    z = succ(a);
    print z;
    return 0; 
}

'''

(P,M) = parse(lexer(s),Grammar_HW07,table)


verbose = False

if verbose:
    for i in range(len(P)):
        print(str(i) + ": " + str(P[i]))
    test(P,M,True)
else:
    test(P,M)


# Test 2: multiple function calls 

s = '''

a = 1;

def succ(x) {
    return x + 1;
}

def main() {
    z = succ(a) + succ(a+1) * succ(a*2); 
    print z;
    return 0; 
}

'''

(P,M) = parse(lexer(s),Grammar_HW07,table)

verbose = False

if verbose:
    for i in range(len(P)):
        print(str(i) + ": " + str(P[i]))
    test(P,M,True)
else:
    test(P,M)



# Test 3: nested function calls 

s = '''

a = 5;

def succ(x) {
    return x + 1;
}

def main() {
    z = succ(succ(succ(a)));
    print z;
    return 0; 
}

'''

(P,M) = parse(lexer(s),Grammar_HW07,table)

verbose = False

if verbose:
    for i in range(len(P)):
        print(str(i) + ": " + str(P[i]))
    test(P,M,True)
else:
    test(P,M)


# Test 4: basic function calls (functions with two arguments)

s = '''

a = 1;

def add(x,y) {
    return x + y;
}

def times(x,y) {
    return x * y;
}

def main() {
    z = times(add(a,1),add(2,a));
    print z;
    return 0; 
}

'''

(P,M) = parse(lexer(s),Grammar_HW07,table)

verbose = False

if verbose:
    for i in range(len(P)):
        print(str(i) + ": " + str(P[i]))
    test(P,M,True)
else:
    test(P,M)

# Test 5: multiple functions calling each other

s = '''

def succ(x) {
    return x + 1;
}

def times2(x) {
    return x * 2;
}

def f(y) {
    z = succ(y);
    y = times2(z);
    return y;
}

def main() {
    z = f(10);
    print z;
    return 0; 
}

'''

(P,M) = parse(lexer(s),Grammar_HW07,table)

verbose = False

if verbose:
    for i in range(len(P)):
        print(str(i) + ": " + str(P[i]))
    test(P,M,True)
else:
    test(P,M)


# Test 6: recursion!

s = '''

def fact(x) {
    if( x < 2) {
        return 1;
    }
    else {
        return x * fact( x - 1 );
    }
}

def main() {
    z = fact(5);
    print z;
    return 0; 
}

'''

(P,M) = parse(lexer(s),Grammar_HW07,table)

verbose = False

if verbose:
    for i in range(len(P)):
        print(str(i) + ": " + str(P[i]))
    test(P,M,True)
else:
    test(P,M)


# Test 7:  More recursion: the Hofstader Q sequence

s = '''

def Q(n) {
    if(n <= 2) {
        return 1;
    }
    else {
        return Q(n - Q(n-1)) + Q(n - Q(n-2));
    }
}
    
def main() {
    k = 1;
    while(k<20) {
        q = Q(k);
        print(q);
        k = k + 1;
    }
}

'''

(P,M) = parse(lexer(s),Grammar_HW07,table)

verbose = False

if verbose:
    for i in range(len(P)):
        print(str(i) + ": " + str(P[i]))
    test(P,M,True)
else:
    test(P,M)


