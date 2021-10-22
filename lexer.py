#!/usr/bin/python
#!/usr/bin/python3
#!/usr/bin/pyton3.10
import sys
from types import CodeType
MIN_PYTHON = (3, 10)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

if len(sys.argv) > 2: sys.exit("Input file path to analyze as program argumen")

#file that the lexer will generate tokens for 
f = open(sys.argv[1], "r")
#Lenguage definitions by class
DELIMITERS = " \n\t"
DIGITS = "123456789"
LETTERS = "abcdefghijlmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
SYMS_OPS = ["+","*","&","=",">", "," ,";", "(",")","{","}", ""]
TOKEN_CODES = ["mas", "por", "and", "asig", "mayor", "coma", "puntoComa", "parAbierto", "parCerrado", "llaveAbierto", "llaveAbierto", "eof"]
RES_WORD = [ "let","function","rn","else","input","print","while","do","true","false","int","boolean","string"]

class Token:
    def __init__(self, type:str, attribute):
        self.code = type
        self.att = attribute 

class Lexer:
    def __init__(self):
        self.num = 0 #current integer number being constructed
        self.lex = "" #current string being constructed
        self.car = self.read(1) #current character being read

    def next(self) -> str :
        '''Advances current character to the next one from the file'''
        self.car = f.read(1)

    def generateNumber(self):
        '''Adds current char to number in construction after multiplying the number by 10 '''
        self.num = self.num * 10 + int(self.car)        

    def concatenate(self):
        '''Concatenates current char to lexeme in contruction'''
        self.lex = self.lex + self.car

    def skipDelimeters(self):
        '''Skips white spaces, new lines and tabs'''
        while self.car in DELIMITERS: 
            self.next()

    def genToken(self, code:str, attribute)
    def tokenize(self):
        while self.next() is None and self.car != "":
            #Integer being formed 
            if self.car in DIGITS and self.lex=="":
                self.generateNumber()
            #Lexeme being formed 
            elif self.lex != "": self.concatenate()
            #Block comment processing
            elif self.car == "/" and self.next() is None and self.car == "*": 
                while self.car != "*" and self.next() is None and self.car == "/":
                    pass
            #Operators, symbols
            elif self.car in SYMS_OPS:
                index = SYMS_OPS.index(self.car)
                match(index):
                    case 0: 

                    case 1:

                    case 2:

                    case 3:

                    case 4:


self.close()
             
