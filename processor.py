import sys
import os
from string import Template
from typing import List

if len(sys.argv) > 2: sys.exit("Input file path to analyze as program argument")
# manual path specification for debugging puropses
if len(sys.argv) == 1:
    f = open("./casosPruebas/correcto2.txt", "r")
# file that the lexer will generate tokens for
elif os.path.exists(os.getcwd() + "/" + sys.argv[1]):
    f = open(sys.argv[1], "r")
else:
    sys.exit(f"File \'{sys.argv[1]}\' does not exist")
# Lenguage definitions by class
RES_WORD = ["let", "function", "rn", "else", "input", "print", "while", "do", "true", "false", "int", "boolean",
            "string", "return"]
LETTERS = "abcdefghijlmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
SYMB_OPS = {
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
    def __init__(self, type: str, attribute=None, line=None):
        self.code = type
        self.att = attribute
        self.line = line


class Lexer:
    def __init__(self):
        self.num = 0  # current integer number being constructed
        self.lex = ""  # current string being constructed
        self.filename = os.path.basename(f.name)
        self.car = ""  # current character being read
        self.outputdir = os.getcwd() + "/" + self.filename.replace(".txt", "")
        self.line = 1
        self.tokenList = []  # current list of tokens being generated and saved
        self.errorList = []

    def skipBlockComments(self):
        '''Skips block comments and detects error in its specification'''
        self.car = f.read(1)
        if self.car == "*":
            self.car = f.read(1)
            while (self.peekNextCar() != "/" and self.car != "*" and self.car != ""):
                self.car = f.read(1)
                if self.car == "": self.error(3)
                if self.car == "/n": self.car += 1
            self.car = f.read(1)
            self.car = f.read(1)
        elif self.car == "/":
            f.readline()
            self.line += 1
            self.error(5)
        else:
            self.error(4, self.car)

    def skipDelimeters(self):
        '''Skips delimeters such as \\t and \\n '''
        if self.car != "":
            while (self.car != "" and ord(self.car) < 33):
                if self.car == "\n": self.line += 1
                if self.car == "": break  # Block comment processing
                self.car = f.read(1)
            if self.car == "/": self.skipBlockComments()

    def next(self):
        '''Retrieves next character recognized in the leanguage for processing'''
        # if self.peekNextCar()!="": self.car = f.read(1)
        self.car = f.read(1)
        if self.car != "":
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
        try:
            os.mkdir(self.outputdir)
        except OSError:
            f"Error al crear carpeta de volcado en: {self.outputdir}"
        except:
            FileExistsError
        print(f"Directorio de volcado del programa creado en: {self.outputdir}")
        with open(self.outputdir + "/tokens.txt", "w") as f:
            for token in self.tokenList:
                f.write(f"< {token.code} , {token.att} >\n")  # del* < código del* , del* [atributo] del* > del* RE

    def peekNextCar(self) -> str:
        '''Returns the character next to that which the file pointer is at, without advancing said file pointer'''
        pos = f.tell()
        car = f.read(1)
        f.seek(pos)
        return car

    # < codigo , atributo > 
    def genToken(self, code: str, attribute=None) -> Token:
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
            # Integer being formed
            if (self.car).isdigit() and self.lex == "":
                self.generateNumber()
                if (not self.peekNextCar().isdigit()):
                    if (self.num < 32768):
                        self.genToken("cteEnt", self.num)
                    else:
                        self.error(2)

            # Identifiers or Reserved Words
            elif self.car in LETTERS or self.lex != "":
                self.concatenate()
                nextCar = self.peekNextCar()
                if (nextCar not in LETTERS or nextCar == "_" or nextCar.isdigit() or nextCar == ""):
                    if self.lex in RES_WORD:
                        print(self.lex)
                        self.genToken(self.lex)
                    else:
                        if (len(self.lex) < 65):
                            self.genToken("id", self.lex)
                        else:
                            self.error(1)

            # String (cadena) processing
            elif self.car == "\"":
                self.next()
                while self.car != "\"":
                    self.concatenate()
                    self.car = f.read(1)
                if (len(self.lex) < 65):
                    self.genToken("cadena", self.lex)
                else:
                    self.error(1)

            # Operators, symbols
            elif self.car in SYMB_OPS:
                # + or ++
                if (self.car == "+"):
                    if (self.peekNextCar() == "+"):
                        self.genToken("postIncrem")
                        self.next()
                    else:
                        self.genToken("mas")
                # &&
                elif (self.car == "&"):
                    if (self.peekNextCar() == "&"):
                        self.genToken("and")
                        self.next()
                # = or ==
                elif (self.car == "="):
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
                    while self.car != "\'":
                        self.car = f.read(1)
                    if self.car != "":
                        self.error(6)
                    else:
                        self.error(7)
                else:
                    error(4, self.car)
            if self.car != "": self.next()
        self.genToken("eof")  # llega al final de archivo -> eof


First = {
    'P': ["let", "if", "while", "do", "function", "eof"],
    'B': ["let", "if", "while", "do"],
    "O": "else",
    "T": ["int", "boolean", "string"],
    "S": ["id", "return", "print", "input"],
    "Sp": ["asig", "parAbierto", "postIncrem", "asig"],
    "X": ["id", "parAbierto", "entero", "cadena", "true", "false"],
    "C": ["let", "if", "while", "do"],
    "L": ["id", "parAbierto", "entero", "cadena", "true", "false"],
    "Q": "coma",
    "F": "function",
    "H": ["int", "boolean", "string"],
    "A": ["int", "boolean", "string"],
    "K": "coma",
    "E": ["id", "parAbierto", "entero", "cadena", "true", "false"],
    "Ep": ["and", "mayor"],
    "Epp": ["id", "parAbierto", "entero", "cadena", "true", "false"],
    "R": ["id", "parAbierto", "entero", "cadena", "true", "false"],
    "Rp": "mayor",
    "U": ["id", "parAbierto", "entero", "cadena", "true", "false"],
    "Up": ["mas", "por"],
    "V": ["id", "parAbierto", "entero", "cadena", "true", "false"],
    "Vp": "parAbierto"
}


# class error:
#     def __init__(self, tipo: int, attribute=None, line = None):
#         '''Generates an error and appends it to the list of error:\n
#         -tipo: specifies error type. 
#         -All error types are specified in the errorHandler class
#         -attribute: (OPTIONAL) specifies an attribute if the error needs it i.e symbol which was not recognized in error4
#         '''
#         Lexer.errorList.append(err)
#         if tipo == 5: self.line+=1
#         if tipo == 1: self.lex = ""
#         self.line = line


class Syntactic:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.tokenList = lexer.tokenList
        self.index = 0  # indice que apunta al elemento actual de la lista de tokens
        self.token = self.tokenList[self.index].code
        self.reglas = []
        self.outputdir = lexer.outputdir
        self.errorList = []

    def next(self) -> Token:
        print("next: actual= " + self.token)
        self.index += 1
        self.token = self.tokenList[self.index].code
        print("siguiente " + self.token + '\n')
        return self.token

    def equipara(self, code: str, regla=None) -> bool:
        print("actual= " + self.token + " " + "a comparar= " + code)
        if regla is not None: self.reglas.append(regla)
        if (self.token == code):
            self.next()
            return True
        self.errorList.append(error(8, self.tokenList[self.index].line))

    def exportParse(self) -> None:
        '''Creates a directory (specified in self.ouput dir which will contain all the output of the processor.\n
        Writes all tokens with the appropiate format to the file "tokens.txt" after tokenize() has been used'''
        with open(self.outputdir + "/parse.txt", "w") as f:
            f.write("Descendente ")
            for regla in self.reglas: f.write(f"{regla} ".replace("None", ""))

    def P(self) -> None:
        # First(B)
        if (self.token) in First["B"]:
            self.reglas.append(1)
            self.B()
            self.P()
        elif (self.token) in First['F']:
            self.reglas.append(2)
            self.F()
            self.P()
        elif (self.equipara("eof")):
            self.reglas.append(3)
            return

    def B(self) -> None:
        if self.equipara("let", 4):
            self.T()
            if self.equipara("id"):
                if self.equipara("puntoComa"): return
        elif (self.equipara("if") and self.equipara("parAbierto")):
            self.E()
            if self.equipara("parCerrado") and self.equipara("llaveAbierto"):
                self.S()
                if (self.equipara("llaveCerrado")):
                    O()
                    return
        elif (self.token in First["S"]):
            self.reglas.append(6)
            self.S()
        elif self.equipara("while", 7):
            if self.equipara("parAbierto"):
                self.E()
                if (self.equipara("parCerrado")):
                    if self.equipara("llaveAbierto"):
                        self.C()
                        if self.equipara("llaveCerrado"): return
        elif self.equipara("do", 8):
            if self.equipara("llaveAbierto"):
                self.S()
                if self.equipara("llaveCerrado"):
                    if self.equipara("while"):
                        if self.equipara("parAbierto"):
                            self.E()
                            if self.equipara("parCerrado") and self.equipara("puntoComa"): return
        return

    def O(self) -> None:
        if self.equipara("else", 9):
            if self.equipara("parAbierto"):
                self.T()
                if self.equipara("parCerrado"): return
        else:
            self.reglas.append(10)
            return

    def T(self) -> None:
        if (self.equipara("int", 11)):
            return
        elif (self.equipara("boolean", 12)):
            return
        elif (self.equipara("string", 13)):
            return

    def S(self) -> None:
        if (self.equipara("id", 14)):
            self.Sp()
        elif (self.equipara("return", 15)):
            self.X()
            if (self.equipara("puntoComa")): return
        elif self.equipara("print", 16):
            if (self.equipara('parAbierto')):
                self.E()
                if self.equipara("parCerrado") and self.equipara("puntoComa"): return
        elif (self.equipara("input", 17) and self.equipara("parAbierto") and self.equipara("id") and self.equipara(
                "parCerrado") and self.equipara("puntoComa")):
            return

    def Sp(self) -> None:
        if self.equipara("asig", 18):
            self.E()
            if self.equipara("puntoComa"):
                return
        elif (self.equipara("parAbierto", 19)):
            self.L()
            if self.equipara("parCerrado"): return
        elif self.equipara("postIncrem", 20):
            return
        elif self.equipara("equals", 21):
            self.E()

    def X(self) -> None:
        if self.token in First['E']:
            self.reglas.append(22)
            self.E()
        else:
            self.reglas.append(23)
        return

    def C(self) -> None:
        if self.token in First["B"]:
            self.reglas.append(24)
            self.B()
            self.C()
        elif self.token in First["T"]:
            self.T()
            if self.token in First['S']:
                self.reglas.append(9999)
                self.S()
                if (self.equipara("puntoComa")):
                    return
        else:
            self.reglas.append(25)
        return

    def L(self) -> None:
        if self.token in First["E"]:
            self.reglas.append(26)
            self.Q()
        else:
            self.reglas.append(27)
        return

    def Q(self) -> None:
        if self.equipara("coma", 28):
            self.E()
            self.Q()
        else:
            self.reglas.append(29)
        return

    def F(self) -> None:
        if self.equipara("function", 30) and self.equipara("id"):
            if self.token in First["H"]:
                self.H()
                if self.equipara("parAbierto"):
                    self.A()
                    if self.equipara("parCerrado") and self.equipara("llaveAbierto"):
                        self.C()
                        if self.equipara("llaveCerrado"): return

    def H(self) -> None:
        if self.token in First['T']:
            self.reglas.append(31)
            self.T()
        else:
            self.reglas.append(32)
        return

    def A(self) -> None:
        if self.token in First['T']:
            self.reglas.append(33)
            self.T()
            if self.equipara("id"):
                self.K()
        else:
            self.reglas.append(34)
        return

    def K(self) -> None:
        if self.equipara("coma", 35):
            self.T()
            if self.equipara("id"):
                self.K()
        else:
            self.reglas.append(36)
        return

    def E(self) -> None:
        if self.token in First["R"]:
            self.reglas.append(37)
            self.R()
            self.Ep()

    def Ep(self) -> None:
        if self.equipara("and", 38):
            self.Epp()
        elif self.equipara(">", 39):
            self.Epp()
        else:
            self.reglas.append(40)
        return

    def Epp(self) -> None:
        if self.token in First["R"]:
            self.reglas.append(41)
            self.R()
            self.Ep()
        return

    def R(self) -> None:
        if self.token in First['U']:
            self.reglas.append(42)
            self.U()
            self.Rp()
        return

    def Rp(self) -> None:
        if (self.next() == ">"):
            self.reglas.append(43)
            self.U()
            self.Rp()
        else:
            self.reglas.append(44)
        return

    def U(self) -> None:
        if self.token in First["V"]:
            self.reglas.append(45)
            self.V()
            self.Up()
        return

    def Up(self) -> None:
        if self.equipara("mas", 46):
            self.U()
        elif self.equipara("*", 47):
            self.U()
        else:
            self.reglas.append(48)
        return

    def V(self) -> None:
        if self.equipara("id", 49):
            self.Vp()
        elif self.equipara("parAbierto", 50):
            self.E()
            if self.equipara("parCerrado"): return
        elif (self.equipara("cteEnt", 51)):
            return
        elif (self.equipara("cadena", 52)):
            return
        elif (self.equipara("true", 53)):
            return
        elif (self.equipara("false", 54)):
            return

    def Vp(self) -> None:
        if (self.equipara("parAbierto", 55)):
            self.L()
            if self.equipara("parCerrado"): return
        else:
            self.reglas.append(56)
        return


class TS():
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def setIds(self):
        from ordered_set import OrderedSet
        setTokenList = OrderedSet()
        for token in self.lexer.tokenList:
            if token.code == "id": setTokenList.add(token.att)
        return setTokenList

    def printTS(self):
        '''Outputs containing Symbol Table with correct format to 'ts.txt' in directory specified in $lexer.outputdir'''
        with open(self.lexer.outputdir + "/ts.txt", "w") as f:
            f.write(("TS GLOBAL #1"))
            for lexId in self.setIds():
                f.write(f"\n*Lexema: '{lexId}'")


ERROR_MSG = {
    0: "Uso erroneo de comentario de bloque\n\tFormato:\'/* Comentario de bloque */ \'",
    1: "Lexema excede el tamaño maximo de caracteres permitido",
    2: "Digito con valor mayor al permitido (32768) en el sistema",
    3: "Comentario de bloque no cerrado",
    4: "Simbolo '$simbolo' no pertenece al lenguaje",
    5: "Comentarios de tipo: '//comentario', no estan permitidos",
    6: "Cadena se debe especificar entre \" \", no con \' \'",
    7: "cadena no cerrada",
    8: "Error sintáctico"
}


class error:
    def __init__(self, num: int, linea: int, attr=None):
        self.code = num
        self.line = linea
        self.att = attr


class errorHandler:
    def __init__(self, lexer: Lexer, syntactic: Syntactic) -> None:
        self.lexer = lexer
        self.syntactic = syntactic

    def errorStringBuilder(self, tipo: str, f) -> None:
        if tipo == "lex": errList = self.lexer.errorList
        if tipo == "syn": errList = self.syntactic.errorList
        for error in errList:
            errorString = f"\nError code'{error.code}': {ERROR_MSG[error.code]}"
            if error.code == 4: errorString = Template(errorString).substitute(simbolo=error.att)
            if error.code == 7: errorString += ERROR_MSG[7]
            errorString += f"--> linea {error.line}"
            f.write(errorString)

    def errorPrinter(self):
        with open(self.lexer.outputdir + "/errors.txt", "w") as f:
            header = f"Errors output for file '{self.lexer.filename}':\n "
            times = len(header) - 1
            header += "-" * times
            header = "-" * times + "\n" + header + "\nLexical errors: "
            f.write(header)
            self.errorStringBuilder("lex", f)
            header = f"\nSyntactic errors':\n"
            times = len(header) - 1
            header += "-" * times
            header = "-" * times + "\n" + header
            f.write(header)
            self.errorStringBuilder("syn", f)


def pipInstall(package):
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def checkDependencies(deps):
    import pkg_resources
    installed = [d for d in pkg_resources.working_set]
    for dep, realname in deps.items():
        if dep not in str(installed):
            print(f'Module {realname} is not installed and is necessary to run')
            answer = input('Do you want to install it (Y/N): ')
            if answer == "N" or answer == "n" or answer == "No":
                print(f"Exiting ... You must install the {realname} module for the processor to work")
                exit()
            elif answer == "Y" or answer == "y" or answer == "Yes":
                print(f"Installing {realname}...")
                pipInstall(realname)


if __name__ == "__main__":
    # dictionary of dependencies where key is the string used in the working set and value is the
    # actual name of the package that
    deps = {"ordered-set": "ordered_set"}
    checkDependencies(deps)

    lexer = Lexer()
    lexer.tokenize()
    lexer.printTokens()

    ts = TS(lexer)
    ts.printTS()

    syntactic = Syntactic(lexer)
    syntactic.P()
    syntactic.exportParse()

    errorHandler = errorHandler(lexer, syntactic)
    errorHandler.errorPrinter()
