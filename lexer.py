#!/usr/bin/python
#!/usr/bin/python3
#!/usr/bin/pyton3.10
import sys
MIN_PYTHON = (3, 10)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

if len(sys.argv) > 2: sys.exit("Input file path to analyze as program argumen")


#file that the lexer will generate tokens for 
f = open(sys.argv[1], "r")
#Lenguage definitions by class
DELIMITERS = " \n\t"
RES_WORD = [ "let","function","rn","else","input","print","while","do","true","false","int","boolean","string"]
LETTERS = "abcdefghijlmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
SYMB_OPS ={
    "+": "mas",
    "*": "por",
    "&": "and",
    "=": "asig",
    ">": "mayor",
    ",": "coma",
    ";": "puntoComa",
    "(": "parAbierto",
    ")": "parCerrado",
    "{": "llaveAbierto",
    "}": "llaveCerrado"
}

def peek_nextCar(f):
    pos = f.tell()
    f.seek(pos)
    car = f.read(1)
    return car
class Token:
    def __init__(self, type:str, attribute):
        self.code = type
        self.att = attribute 

class Lexer:
    def __init__(self):
        self.num = 0 #current integer number being constructed
        self.lex = "" #current string being constructed
        self.car = f.read(1) #current character being read

    def next(self):
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

    def genToken(self, code:str, attribute) -> Token: 
        token = Token(code, attribute)
        return token

    def tokenize(self):
        while self.next() is None and self.car != "":
            #Integer being formed 
            if (self.car).isDigit() and self.lex=="":
                self.generateNumber()
                if(not peek_nextCar(f).isDigit()): self.genToken("cteEntera", self.num)
            #Identifiers or Reserved Words
            elif self.car in LETTERS and self.lex != "": 
                self.concatenate()
                nextCar = peek_nextCar(f)
                if( nextCar not in LETTERS):
                    if self.lex in RES_WORD: self.genToken(id,self.lex)
                    else: self.genToken(self.lex, None)
            #Block comment processing
            elif self.car == "/" and self.next() is None and self.car == "*": 
                while self.car != "*" and self.next() is None and self.car == "/":
                    self.next()
            #String (cadena) processing
            elif self.car == "\"": 
                while self.car != "\"":
                    self.concatenate()
                    self.next()
                self.genToken("cadena",self.lex)
            #Operators, symbols
            elif self.car in SYMB_OPS:
                #+ or ++
                if(self.car == "+"):
                    if (peek_nextCar(f) == "+") :
                        self.genToken("postIncrem", None)
                        self.next()
                    else: self.genToken("mas", None)
                #&&
                elif (self.car == "&"):
                    if (peek_nextCar(f) == "&") : 
                        self.genToken("and", None)
                        self.next()
                #= or ==
                elif(self.car == "="):
                    if (peek_nextCar(f) == "="):
                        self.genToken("equals", None)
                        self.next()
                    else:
                        self.genToken("asig", None)
                else:
                    self.genToken(SYMB_OPS[self.car], None)
                        
               
                #Identitificadores
                
 