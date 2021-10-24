#!/usr/bin/python
#!/usr/bin/python3
#!/usr/bin/pyton3.10
import sys

if len(sys.argv) > 2: sys.exit("Input file path to analyze as program argument")
#file that the lexer will generate tokens for 
f = open(sys.argv[1], "r")
#Lenguage definitions by class
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
ERROR_CODE = {
    0:"Uso erróneo de comentarios",
    1:"Lexema excede el tamaño máximo de caracteres permitido",
    2:"Dígito con valor mayor al permitido (32768) en el sistema"
}

def peek_nextCar(f):
    pos = f.tell()
    car = f.read(1)
    f.seek(pos)
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
        self.tokenList = [] #current list of tokens being generated and saved

    def next(self):
        '''Advances current character to the next one from the file'''
        self.car = f.read(1)
        if self.car != "": 
            while(ord(self.car) < 33):
                self.car = f.read(1)
    
    def generateNumber(self):
        '''Adds current char to number in construction after multiplying the number by 10 '''
        self.num = self.num * 10 + int(self.car)        

    def concatenate(self):
        '''Concatenates current char to lexeme in contruction'''
        self.lex += self.car

    def printToken(self,):
        with open("tokens.txt", "w") as f:
            for token in self.tokenList:
                f.write(f"< {token.code} , {token.att} >\n".replace("None", " ")) #del* < código del* , del* [atributo] del* > del* RE

    def printTS(self):
        with open("ts.txt", "w") as f:
            #to do
            for token in self.tokenList:
                f.write(f"* TS de X#N:\n*'{token}'\n+tipo: {token.code}\n+despl: {token}num_x \n") #pal* # del* núm del* : del* RC



# < codigo , atributo > 
    def genToken(self, code:str, attribute=None) -> Token: 
        token = Token(code, attribute)
        self.tokenList.append(token)
        self.lex = ""
        self.num = 0
        return token

    def error(self, tipo: int):
        sys.exit(f"[ERROR] {ERROR_CODE[tipo]}")

    def tokenize(self):
        while self.car != "":
            # ------------------ TO FIX ------------------
            #Integer being formed
            if (self.car).isdigit() and self.lex=="":
                self.generateNumber()
                if(not peek_nextCar(f).isdigit()):
                    if(self.num < 32768):
                        self.genToken("cteEnt", self.num)
                    else:
                        self.error(2)
            
            #Identifiers or Reserved Words
            elif self.car in LETTERS or self.lex != "":
                self.concatenate()
                nextCar = peek_nextCar(f)
                if(nextCar not in LETTERS or nextCar == "_" or nextCar.isdigit() or nextCar ==""):
                    if self.lex in RES_WORD: 
                        self.genToken(self.lex)
                    else:
                        if(len(self.lex)<65):self.genToken(self.lex)
                        else:self.error(1)
            
            #Block comment processing
            elif self.car == "/":
                self.next()
                if self.car == "*":
                    self.next()
                    while (peek_nextCar(f) != "/" and self.car != "*"):
                        self.next()
                        self.next()
                else: self.error(0)
                self.next()
            
            #String (cadena) processing
            elif self.car == "\"": 
                self.next()
                while self.car != "\"":
                    self.concatenate()
                    self.next()
                if(len(self.lex)<65):self.genToken("cadena",self.lex)
                else:self.error(1)
            
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
            self.next()