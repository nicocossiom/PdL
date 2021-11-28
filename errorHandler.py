from string import Template
from lexer import *
from syntactic import *

ERROR_MSG = {
    0:"Uso erroneo de comentario de bloque\n\tFormato:\'/* Comentario de bloque */ \'",
    1:"Lexema excede el tamaño maximo de caracteres permitido",
    2:"Digito con valor mayor al permitido (32768) en el sistema",
    3:"Comentario de bloque no cerrado",
    4:"Simbolo '$simbolo' no pertenece al lenguaje",
    5:"Comentarios de tipo: '//comentario', no estan permitidos",
    6:"Cadena se debe especificar entre \" \", no con \' \'",
    7:"cadena no cerrada",
    8:"Error sintáctico"
}

class Error():
    def __init__(self, num:int, linea:int, attr=None):
        self.code = num
        self.line = linea
        self.att = attr

class errorHandler:
    def __init__(self, lexer : lexer , syntactic : Syntactic ) -> None:
        self.lexer = lexer
        self.syntactic = syntactic
    
    def errorStringBuilder(self, tipo :String ) -> None:
        if tipo == "lex": errList = self.lexer.errorList
        if tipo == "syn": errList = self.syntactic.errorList
        for error in errList:
            errorString = f"\nError code'{error.code}'': {ERROR_MSG[error.code]}"
            if error.code == 4: errorString=Template(errorString).substitute(simbolo = error.att)
            if error.code == 7: errorString+=ERROR_MSG[7]
            errorString+= f"--> linea {error.line}"
            f.write(errorString)
        
    def errorPrinter (self):
        with open(self.lexer.outputdir+"/errors.txt", "w") as f:
            header = f"Errors output for file '{self.lexer.filename}':\n Lexical errors: "
            times = len(header)-1
            header+="-" * times 
            header = "-" * times +"\n"+header
            f.write(header)
            errorStringBuilder("lex")
            header = f"\nSynactic errors':\n"
            times = len(header)-1
            header+="-" * times 
            header = "-" * times +"\n"+header
            f.write(header)   
            errorStrinBuilder("syn")