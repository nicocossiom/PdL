DELIMITERS = " \n\t"
DIGITS = "123456789"
LETTERS = "abcdefghijlmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ_"
OPERATORS_OTHERS = ["+","*","&","=",">", "," ,";", "(",")","{","}", ""]
class Lexer:
    def __init__(self, file:str):
        self.f = open(file, "r")
        self.PTR = [ "hola", "let","function","rn","else","input","print","while","do","true","false","int","boolean","string"]
        self.num = 0
        self.car = self.read(1)

    def next(self):
        self.car = self.f.read(1)

    def changeFile(self, file:str):
        self.f.close()
        self.f = f = open(file, "r")

    def generateNumber(self):
        self.num = self.num * 10 + int(self.car)        

    def concatenate(self):
        self.lex = self.lex + self.car

    def tokenize(self):
        while self.next() is None and self.car != "":
            if(self.car in DELIMITERS):
                self.next()
            elif self.car in DIGITS and self.num != 0:
                self.generateNumber()
            elif self.car in (LETTERS, DIGITS, "_"):
                self.concatenate()
            elif self.car == "/" and self.next() is None and self.car == "*": 
                while self.car != "*" and self.next() is None and self.car == "/":
                    pass
            elif self.car in OPERATORS_OTHERS:
                index = OPERATORS_OTHERS.index(self.car)
                match(index):
                    case 0: 
                        
                    case 1:
                    
                    case 2:

                    case 3:
                    
                    case 4:
                    

self.close()