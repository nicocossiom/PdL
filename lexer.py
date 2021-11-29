import sys
import os 
import errorHandler

if len(sys.argv) > 2: sys.exit("Input file path to analyze as program argument")
#manual path specification for debugging puropses
if len(sys.argv) == 1: f = open("./casosPruebas/incorrecto3.txt" ,"r")
#file that the lexer will generate tokens for 
elif os.path.exists(os.getcwd() + "/"+ sys.argv[1]): f = open(sys.argv[1], "r")
else: sys.exit(f"File \'{sys.argv[1]}\' does not exist")
#Lenguage definitions by class
RES_WORD = [ "let","function","rn","else","input","print","while","do","true","false","int","boolean","string","return"]
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

class Token:
    def __init__(self, type:str, attribute=None, linea = None):
        self.code = type
        self.att = attribute
        self.linea = linea
class Lexer:
    def __init__(self):
        self.num = 0 #current integer number being constructed
        self.lex = "" #current string being constructed
        self.filename = os.path.basename(f.name)
        self.car = "" #current character being read
        self.outputdir = os.getcwd()+"/output" +self.filename+"Output"
        self.line = 1
        self.tokenList = [] #current list of tokens being generated and saved
        self.errorList = []
    
    class error(errorHandler):
        def __init__(self, tipo: int, attribute=None):
            '''Generates an error and appends it to the list of error:\n
            -tipo: specifies error type. 
            -All error types are specified in the errorHandler class
            -attribute: (OPTIONAL) specifies an attribute if the error needs it i.e symbol which was not recognized in error4
            '''
            err = Error(tipo, self.line, attribute)
            self.errorList.append(err)
            if tipo == 5: self.line+=1
            if tipo == 1: self.lex = ""
    
    def skipBlockComments(self):
        '''Skips block comments and detects error in its specification'''
        self.car = f.read(1)
        if self.car == "*":
            self.car = f.read(1)
            while (self.peekNextCar() != "/" and self.car != "*" and self.car != ""):
                self.car = f.read(1)
                if self.car == "" : self.error(3)
                if self.car == "/n": self.car+=1
            self.car = f.read(1)
            self.car = f.read(1)
        elif self.car == "/": 
            f.readline()
            self.line+=1
            self.error(5)
        else: self.error(4, self.car)
    
    def skipDelimeters(self):
        '''Skips delimeters such as \\t and \\n '''
        if self.car!= "":
            while(self.car != "" and ord(self.car) < 33):    
                if self.car == "\n": self.line+=1
                if self.car == "": break#Block comment processing
                self.car = f.read(1)
            if self.car == "/": self.skipBlockComments()

    def next(self):
        '''Retrieves next character recognized in the leanguage for processing'''
        # if self.peekNextCar()!="": self.car = f.read(1)
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

    def printTokens(self):
        '''Creates a directory (specified in self.ouput dir which will contain all the output of the processor.\n
        Writes all tokens with the appropiate format to the file "tokens.txt" after tokenize() has been used'''
        os.mkdir(self.outputdir)   
        # try: os.mkdir(self.outputdir)    
        # except OSError: f"Error al crear carpeta de volcado en: {self.outputdir}"
        # except: FileExistsError
        # print(f"Directorio de volcado del programa creado en: {self.outputdir}") 
        # with open(self.outputdir+"/tokens.txt", "w") as f:
        #     for token in self.tokenList:
        #         f.write(f"< {token.code} , {token.att} >\n".replace("None", " ")) #del* < código del* , del* [atributo] del* > del* RE

    def peekNextCar(self) -> str:
        '''Returns the character next to that which the file pointer is at, without advancing said file pointer'''
        pos = f.tell()
        car = f.read(1)
        f.seek(pos)
        return car
        
    # < codigo , atributo > 
    def genToken(self, code:str, attribute=None) -> Token: 
        '''Generates a token and appends it to the list of tokens:\n
        -code: specifies token code (id,string,cteEnt,etc)
        -attribute: (OPTIONAL) specifies an attribute if the token needs it i.e < cteEnt , valor > 
        '''
        token = Token(code, attribute, self.line)
        self.tokenList.append(token)
        self.lex = ""
        self.num = 0
        return token
   
    def tokenize(self):
        ''''
        Analyzes characters, generates tokens and errors if found
        '''
        self.next()
        while self.car != "":
            #Integer being formed
            if (self.car).isdigit() and self.lex=="":
                self.generateNumber()
                if(not self.peekNextCar().isdigit()):
                    if(self.num < 32768):
                        self.genToken("cteEnt", self.num)
                    else:
                        self.error(2)
            
            #Identifiers or Reserved Words
            elif self.car in LETTERS or self.lex != "":
                self.concatenate()
                nextCar = self.peekNextCar()
                if(nextCar not in LETTERS or nextCar == "_" or nextCar.isdigit() or nextCar ==""):
                    if self.lex in RES_WORD: 
                        self.genToken(self.lex)
                    else:
                        if(len(self.lex)<65):self.genToken("id", self.lex)
                        else: self.error(1)
            
            #String (cadena) processing
            elif self.car == "\"":
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
                    if (self.peekNextCar() == "+") :
                        self.genToken("postIncrem")
                        self.next()
                    else: self.genToken("mas")
                #&&
                elif (self.car == "&"):
                    if (self.peekNextCar() == "&") : 
                        self.genToken("and")
                        self.next()
                #= or ==
                elif(self.car == "="):
                    if (self.peekNextCar() == "="):
                        self.genToken("equals")
                        self.next()
                    else:
                        self.genToken("asig")
                else:
                    self.genToken(SYMB_OPS[self.car])
            else:
                if self.car in "\'":
                    self.car = f.read(1)
                    while self.car !="\'":
                        self.car = f.read(1)
                    if self.car != "": 
                        self.error(6) 
                    else: self.error(7)
                else: self.error(4, self.car)
            if self.car != "": self.next()
        self.genToken("eof") #llega al final de archivo -> eof