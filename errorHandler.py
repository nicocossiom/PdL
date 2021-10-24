from string import Template
from lexer import *

ERROR_MSG = {
    0:"Uso erroneo de comentario de bloque\n\tFormato:\'/* Comentario de bloque */ \'",
    1:"Lexema excede el tamaño maximo de caracteres permitido",
    2:"Digito con valor mayor al permitido (32768) en el sistema",
    3:"Comentario de bloque no cerrado",
    4:"Simbolo '$simbolo' no pertenece al lenguaje",
    5:"Comentarios de tipo: '//comentario', no estan permitidos",
    6:"Cadena se debe especificar entre \" \", no con \' \'",
    7:"cadena no cerrada"
}
class ErrorHandler():
    def __init__(self, lexer:Lexer):
        self.lexer = lexer

    def errorPrinter (self):
        with open(self.lexer.outputdir+"/errors.txt", "w") as f:
            header = f"Errors output for file '{self.lexer.filename}':\n"
            times = len(header)-1
            header+="-" * times 
            header = "-" * times +"\n"+header
            f.write(header)
            for error in self.lexer.errorList:
                errorString =f"\nError code'{error.code}'': {ERROR_MSG[error.code]}"
                if error.code == 4: errorString=Template(errorString).substitute(simbolo = error.att)
                if error.code == 7:errorString+=ERROR_MSG[7]
                errorString+= f"--> linea {error.line}"
                f.write(errorString)
    

