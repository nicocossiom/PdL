#!/usr/bin/python
#!/usr/bin/python3
#!/usr/bin/pyton3.10
import sys
import os 

if len(sys.argv) > 2: sys.exit("Input file path to analyze as program argument")
#file that the lexer will generate tokens for 
if len(sys.argv) == 1: f = open("./casosPruebas/correcto1.txt" ,"r")
elif os.path.exists(os.getcwd() + "/"+ sys.argv[1]): f = open(sys.argv[1], "r")
else: sys.exit(f"File \'{sys.argv[1]}\' does not exist")
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


class Error():
    def __init__(self, num:int, linea:int, attr=None):
        self.code = num
        self.line = linea
        self.att = attr

class Token:
    def __init__(self, type:str, attribute=None):
        self.code = type
        self.att = attribute 

class Lexer:
    def __init__(self):
        self.num = 0 #current integer number being constructed
        self.lex = "" #current string being constructed
        self.filename = os.path.basename(f.name)
        self.car = "" #current character being read
        self.outputdir = os.getcwd()+"/" +self.filename+"Output"
        self.line = 1
        self.tokenList = [] #current list of tokens being generated and saved
        self.errorList = []

    def skipBlockComments(self):
        self.car = f.read(1)
        if self.car == "*":
            self.car = f.read(1)
            while (self.peek_nextCar(f) != "/" and self.car != "*" and self.car != ""):
                self.car = f.read(1)
                if(self.car == ""): self.error(3)
            self.car = f.read(1)
            self.car = f.read(1)
        elif self.car == "/": 
            f.readline()
            self.line+=1
            self.error(5)
        else: self.error(4, self.car)
    
    def skipDelimeters(self):
        if self.car!= "":
            while(self.car != "" and ord(self.car) < 33):    
                if self.car == "\n": self.line+=1
                if self.car == "": break#Block comment processing
                self.car = f.read(1)
            if self.car == "/": self.skipBlockComments()

    def next(self):
        '''Advances current character to the next one from the file'''
        # if self.peek_nextCar(f)!="": self.car = f.read(1)
        self.car = f.read(1)
        if self.car !="":
            if self.car != "/":
               self.skipDelimeters() 
            else: 
                self.skipBlockComments()
                self.skipDelimeters()

            

    def generateNumber(self):
        '''Adds current char to number in construction after multiplying the number by 10 '''
        self.num = self.num * 10 + int(self.car)        

    def concatenate(self):
        '''Concatenates current char to lexeme in contruction'''
        self.lex += self.car

    def printToken(self,):
        try: os.mkdir(self.outputdir)    
        except OSError: f"Error al crear carpeta de volcado en: {self.outputdir}"
        except: FileExistsError
        print(f"Directorio de volcado del programa creado en: {self.outputdir}") 
        with open(self.outputdir+"/tokens.txt", "w") as f:
            for token in self.tokenList:
                f.write(f"< {token.code} , {token.att} >\n".replace("None", " ")) #del* < código del* , del* [atributo] del* > del* RE

    def peek_nextCar(self, f) -> str:
        pos = f.tell()
        car = f.read(1)
        f.seek(pos)
        return car
        
    # < codigo , atributo > 
    def genToken(self, code:str, attribute=None) -> Token: 
        token = Token(code, attribute)
        self.tokenList.append(token)
        self.lex = ""
        self.num = 0
        return token
    
    def error(self, tipo: int, attributes=None):
        err = Error(tipo, self.line, attributes)
        self.errorList.append(err)
        if tipo == 5: self.line+=1
        if tipo == 1: self.lex = ""
   
    def tokenize(self):
        self.next()
        while self.car != "":
            #Integer being formed
            if (self.car).isdigit() and self.lex=="":
                self.generateNumber()
                if(not self.peek_nextCar(f).isdigit()):
                    if(self.num < 32768):
                        self.genToken("cteEnt", self.num)
                    else:
                        self.error(2)
            
            #Identifiers or Reserved Words
            elif self.car in LETTERS or self.lex != "":
                self.concatenate()
                nextCar = self.peek_nextCar(f)
                if(nextCar not in LETTERS or nextCar == "_" or nextCar.isdigit() or nextCar ==""):
                    if self.lex in RES_WORD: 
                        self.genToken(self.lex)
                    else:
                        if(len(self.lex)<65):self.genToken("id", self.lex)
                        else: self.error(1)
            
            #String (cadena) processing
            elif self.car == "\"" or "": 
                self.next()
                while self.car != "\"":
                    self.concatenate()
                    self.car = f.read(1)
                if(len(self.lex)<65): self.genToken("cadena",self.lex)
                else: self.error(1)
            
            #Operators, symbols
            elif self.car in SYMB_OPS:
                #+ or ++
                if(self.car == "+"):
                    if (self.peek_nextCar(f) == "+") :
                        self.genToken("postIncrem")
                        self.next()
                    else: self.genToken("mas")
                #&&
                elif (self.car == "&"):
                    if (self.peek_nextCar(f) == "&") : 
                        self.genToken("and")
                        self.next()
                #= or ==
                elif(self.car == "="):
                    if (self.peek_nextCar(f) == "="):
                        self.genToken("equals")
                        self.next()
                    else:
                        self.genToken("asig")
                else:
                    self.genToken(SYMB_OPS[self.car])
            else:
                if self.car in "\'`":
                    while self.car not in "\'`":
                        self.next()
                    if self.car != "": 
                        self.error(6) 
                    else: self.error(7)
                else: self.error(4, self.car)
            if self.car != "": self.next()