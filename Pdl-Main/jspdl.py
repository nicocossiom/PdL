import os
import string
import sys
from os import error
from string import Template

from ordered_set import T

# Lenguage definitions by class
RES_WORD = ["let", "function", "rn", "else", "input", "print", "while", "do", "true", "false", "int", "boolean",
            "string", "return", "if"]
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


class Error:
    """
    Global error class used for all parts of the procesor. Each part must define its own error() method
    that creates an Error and adds it to the list of errors of said class
    """
    def __init__(self, msg: string, linea: int = None, attr=None):
        """
        msg = msg
        
        """
        self.msg = msg
        self.line = linea
        self.att = attr


class Token:
    def __init__(self, type: str, attribute=None, line=None):
        self.code = type
        self.att = attribute
        self.line = line


class Lexer:
    def __init__(self, f):
        self.f = f
        self.num = 0  # current integer number being constructed
        self.lex = ""  # current string being constructed
        self.filename = os.path.basename(self.f.name)
        self.car = ""  # current character being read
        self.outputdir = os.getcwd() + "/" + self.filename.replace(".jspdl", "")
        self.line = 1
        self.tokenList = []  # current list of tokens being generated and saved
        self.errorList = []

    def skipBlockComments(self):
        """Skips block comments and detects error in its specification"""
        self.car = self.f.read(1)
        if self.car == "*":
            self.car = self.f.read(1)
            while self.peekNextCar() != "/" and self.car != "*" and self.car != "":
                self.car = self.f.read(1)
                if self.car == "": self.error("Comentario de bloque no cerrado")
                if self.car == "/n": self.car += 1
            self.car = self.f.read(1)
            self.car = self.f.read(1)
        elif self.car == "/":
            self.f.readline()
            self.line += 1
            self.error("Comentarios de tipo '//comentario' no estan permitidos")
        else:
            self.error("Simbolo '$simbolo' no pertenece al lenguaje", self.car)

    def skipDelimeters(self):
        """Skips delimiters such as \\t and \\n """
        if self.car != "":
            while self.car != "" and ord(self.car) < 33:
                if self.car == "\n": self.line += 1
                if self.car == "": break  # Block comment processing
                self.car = self.f.read(1)
            if self.car == "/": self.skipBlockComments()

    def next(self):
        """Retrieves next character recognized in the language for processing"""
        # if self.peekNextCar()!="": self.car = self.f.read(1)
        self.car = self.f.read(1)
        if self.car != "":
            if self.car != "/":
                self.skipDelimeters()
            else:
                self.skipBlockComments()
                self.skipDelimeters()

    def generateNumber(self):
        """Adds current char to number in construction after multiplying the number by 10 """
        self.num = self.num * 10 + int(self.car)

    def concatenate(self):
        """Concatenates current char to lexeme in contruction"""
        self.lex += self.car

    def printTokens(self):
        """Creates a directory (specified in self.output dir which will contain all the output of the processor.\n
        Writes all tokens with the appropriate format to the file "tokens.txt" after tokenize() has been used"""

        try:
            os.mkdir(self.outputdir)
        except OSError:
            f"Error al crear carpeta de volcado en: {self.outputdir}"
        except FileExistsError:
            pass
        print(f"Directorio de volcado del programa creado en: {self.outputdir}")
        with open(self.outputdir + "/tokens.txt", "w") as f:
            for token in self.tokenList:
                f.write(f"< {token.code} , {token.att} >\n")  # del* < código del* , del* [atributo] del* > del* RE

    def peekNextCar(self) -> str:
        """Returns the character next to that which the file pointer is at, without advancing said file pointer"""
        pos = self.f.tell()
        car = self.f.read(1)
        self.f.seek(pos)
        return car

    def error(self, msg: string, linea: int = None, attr=None):
        self.errorList.append(Error(msg, linea, attr))

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
        """'
        Analyzes characters, generates tokens and errors if found
        """
        self.next()
        while self.car != "":
            # Integer being formed
            if (self.car).isdigit() and self.lex == "":
                self.generateNumber()
                if not self.peekNextCar().isdigit():
                    if self.num < 32768:
                        self.genToken("cteEnt", self.num)
                    else:
                        self.error("Digito con valor mayor al permitido (32768) en el sistema")

            # Identifiers or Reserved Words
            elif self.car in LETTERS or self.lex != "":
                self.concatenate()
                nextCar = self.peekNextCar()
                if not nextCar.isdigit() and nextCar not in LETTERS and nextCar != "_" or nextCar == "":
                    if self.lex in RES_WORD:
                        self.genToken(self.lex)
                    else:
                        if len(self.lex) < 65:
                            self.genToken("id", self.lex)
                        else:
                            self.error("Lexema (Id, Res) excede el tamaño maximo de caracteres permitido")

            # String (cadena) processing
            elif self.car == "\"":
                self.next()
                while self.car != "\"":
                    self.concatenate()
                    self.car = self.f.read(1)
                if len(self.lex) < 65:
                    self.genToken("cadena", self.lex)
                else:
                    self.error("Lexema (String) excede el tamaño maximo de caracteres permitido")

            # Operators, symbols
            elif self.car in SYMB_OPS:
                # + or ++
                if self.car == "+":
                    if self.peekNextCar() == "+":
                        self.genToken("postIncrem")
                        self.next()
                    else:
                        self.genToken("mas")
                # &&
                elif self.car == "&":
                    if self.peekNextCar() == "&":
                        self.genToken("and")
                        self.next()
                # = or ==
                elif self.car == "=":
                    if self.peekNextCar() == "=":
                        self.genToken("equals")
                        self.next()
                    else:
                        self.genToken("asig")
                else:
                    self.genToken(SYMB_OPS[self.car])
            else:
                if self.car in "\'":
                    self.car = self.f.read(1)
                    while self.car != "\'":
                        self.car = self.f.read(1)
                    if self.car != "":
                        self.error("Cadena se debe especificar entre \" \", no con \' \'")
                    else:
                        self.error("Cadena no cerrada")
                else:
                    error("Simbolo '$simbolo' no pertenece al lenguaje", self.car)
            if self.car != "": self.next()
        self.genToken("eof")  # llega al final de archivo -> eof


# -------------------------Syntactic-------------------------------

First = {
    'P':  ["function", "eof", "let", "if", "do", "id", "return", "print", "input"],
    'B':  ["let", "if", "do", "id", "return", "print", "input"],
    "T":  ["int", "boolean", "string"],
    "S":  ["id", "return", "print", "input"],
    "Sp": ["asig", "parAbierto", "postIncrem"],
    "X":  ["id", "parAbierto", "cteEnt", "cadena", "boolT", "boolF", "lambda"],
    "C":  ["let", "if", "id", "return", "print", "input", "do"],
    "L":  ["id", "parAbierto", "cteEnt", "cadena", "boolT", "boolF"],
    "Q":  "coma",
    "F":  "function",
    "H":  ["int", "boolean", "string"],
    "A":  ["int", "boolean", "string"],
    "K":  "coma",
    "E":  ["mas", "por", "lambda"],
    "N":  ["equals", "mayor", "lambda"],
    "Z":  ["or", "and", "lambda"],
    "O1":  ["mas", "por", "lambda"],
    "O2":  ["equals", "mayor", "lambda"],
    "O3":  ["or", "and", "lambda"],
    "R":  ["id", "parAbierto", "cteEnt", "cadena", "boolT", "boolF"],
    "Rp": ["parAbierto", "postIncrem", "lambda"],
}

# usamos eof como $ para marcar fin de sentencia admisible
Follow = {
    "O1":  ["puntoComa", "parCerrado", "coma"],
    "O2":  ["mas", "por", "lambda"],
    "O3":  ["equals", "mayor", "lambda"],
    "X":  "puntoComa",
    "C":  "llaveAbierto",
    "L":  "parCerrado",
    "Q":  "parCerrado",
    "H":  "parAbierto",
    "A":  "parCerrado",
    "K":  "parCerrado",
    "Rp": ["and",  "mas", "por", "equals", "mayor", "lambda", "coma", "puntoComa", "parCerrado"],
    "Spp": [""]
}


class Syntactic:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.tokenList = lexer.tokenList
        self.index = 0  # indice que apunta al elemento actual de la lista de tokens
        self.actualToken = self.tokenList[self.index]
        self.token = self.actualToken.code
        self.reglas = []
        self.outputdir = lexer.outputdir
        self.errorList = []

    def next(self) -> Token:
        if self.token != "eof":
            compStr = "\nnext: " + self.token
            self.index += 1
            self.actualToken = self.tokenList[self.index]
            self.token = self.actualToken.code
            print(compStr + " -> " + self.token)
            return self.token

    def equipara(self, code: str, regla=None) -> bool:
        print(f"equipara({self.token} , {code} )", end="")
        if self.token == code:
            print("CORRECTO")
            if regla is not None:
                # only add rule when it's first check in a function (has regla), and we're sure it's the correct token
                self.reglas.append(regla)
            self.next()
            return True
        if regla is None: # after first check (means we're in the middle of a state
            # we expected a certain token but it was not it, now we can say it's an error
            self.error(f"Received {code} - Expected another certain token", self.tokenList[self.index].line)
        print("INCORRECTO -> siguiente")
        return False

    def error(self, msg: string, linea: int = None, attr=None):
        self.errorList.append(Error(msg, linea, attr))

    def exportParse(self) -> None:
        """Creates a directory (specified in self.ouput dir which will contain all the output of the processor.\n
        Writes all tokens with the appropiate format to the file "tokens.txt" after tokenize() has been used"""
        with open(self.outputdir + "/parse.txt", "w") as f:
            f.write("Descendente ")
            for regla in self.reglas:
                f.write(f"{regla} ".replace("None", ""))

    def startSyntactic(self):
        self.P()
        # if self.next() != "eof":
        #     self.error("Error sintáctico")
        # else:
        print("Terminado ")

    def P(self) -> None:
        if self.token in First["B"]:
            self.reglas.append(1)
            self.B()
            self.P()
        elif self.token in First['F']:
            self.reglas.append(2)
            self.F()
            self.P()
        elif self.equipara("eof"):
            self.reglas.append(3)
            return

    def B(self) -> None:
        if self.equipara("let", 4):
            self.T()
            if self.equipara("id"):
                if self.equipara("puntoComa"):
                    return
        elif self.equipara("if", 5) and self.equipara("parAbierto"):
            self.E()
            if self.equipara("parCerrado"):
                self.S()
        elif self.token in First["S"]:
            self.reglas.append(6)
            self.S()
        elif self.equipara("do", 7):
            if self.equipara("llaveAbierto"):
                self.C()
                if self.equipara("llaveCerrado") and self.equipara("while") and self.equipara("parAbierto"):
                    self.E()
                    if self.equipara("parCerrado") and self.equipara("puntoComa"):
                        return

    def T(self) -> None:
        if self.equipara("int", 8):
            return
        elif self.equipara("boolean", 9):
            return
        elif self.equipara("string", 10):
            return

    def S(self) -> None:
        if self.equipara("id", 11):
            self.Sp()
        elif self.equipara("return", 12):
            self.X()
            if self.equipara("puntoComa"):
                return
        elif self.equipara("print", 13):
            if self.equipara("parAbierto"):
                self.E()
                if self.equipara("parCerrado") and self.equipara("puntoComa"):
                     return
        elif (self.equipara("input", 14) and self.equipara("parAbierto") and self.equipara("id") and self.equipara(
                "parCerrado") and self.equipara("puntoComa")):
            return

    def Sp(self) -> None:
        if self.equipara("asig", 15):
            self.E()
            if self.equipara("puntoComa"):
                return
        elif self.equipara("parAbierto", 16):
            self.L()
            if self.equipara("parCerrado") and self.equipara("puntoComa"):
                return
        elif self.equipara("postIncrem", 17) and self.equipara("puntoComa"):
            return
        #else:
        #    self.error("Error sintáctico")

    def X(self) -> None:
        if self.token in First['E']:
            self.reglas.append(18)
            self.E()
        elif self.token in Follow['X']:
            self.reglas.append(19)
        else:
            self.error(f"Expected ';' to terminate sentence after return")

    def C(self) -> None:
        if self.token in First["B"]:
            self.reglas.append(20)
            self.B()
            self.C()
        elif self.token in Follow['C']:
            self.reglas.append(21)

    def L(self) -> None:
        if self.token in First["E"]:
            self.reglas.append(22)
            self.E()
            self.Q()
        elif self.token in Follow['L']:
            self.reglas.append(23)
        else:
            self.error("Error sintáctico")

    def Q(self) -> None:
        if self.equipara("coma", 24):
            self.E()
            self.Q()
        elif self.token in Follow['Q']:
            self.reglas.append(25)

    def F(self) -> None:
        if self.equipara("function", 26) and self.equipara("id"):
            self.H()
            if self.equipara("parAbierto"):
                self.A()
                if self.equipara("parCerrado") and self.equipara("llaveAbierto"):
                    self.C()
                    if self.equipara("llaveCerrado"):
                        return

    def H(self) -> None:
        if self.token in First['T']:
            self.reglas.append(27)
            self.T()
        elif self.token in Follow['H']:
            self.reglas.append(28)
        else:
            self.error(f"Las funciones deben tener un tipo de identificador {First['T']}")

    def A(self) -> None:
        if self.token in First['T']:
            self.reglas.append(29)
            self.T()
            if self.equipara("id"):
                self.K()
        elif self.token in Follow['A']:
            self.reglas.append(30)
        else:
            self.error(f"Los argumentos de entrada de las funciones deben tener un tipo de identificador {First['T']}")

    def K(self) -> None:
        if self.equipara("coma", 31):
            self.T()
            if self.equipara("id"):
                self.K()
        elif self.token in Follow['K']:
            self.reglas.append(32)
        else:
            self.error("Los argumentos de las funciones tienen que ir separados por ','")

    def E(self) -> None:
        if self.token in First["N"]:
            self.reglas.append(33)
            self.N()
            self.O1()

    def N(self) -> None:
        if self.token in First["Z"]:
            self.reglas.append(34)
            self.Z()
            self.O2()

    def Z(self) -> None:
        if self.token in First["R"]:
            self.reglas.append(35)
            self.R()
            self.O3()
    
    def O1(self) -> None:
        if self.equipara("mas", 36):
            self.R()
            self.O1()
        elif self.equipara("por", 37):
            self.R()
            self.O1()
        elif self.token in Follow['O1']:
            self.reglas.append(38)
        #else:
        #    self.error("Expected '+' / '*' sign")

    def O2(self) -> None:
        if self.equipara("equals", 39):
            self.R()
            self.O2()
        elif self.equipara("mayor", 40):
            self.R()
            self.O2()
        elif self.token in Follow['O2']:
            self.reglas.append(41)
        #else:
        #    self.error("Expected '==' / '>' sign")

    def O3(self) -> None:
        if self.equipara("or", 42):
            self.R()
            self.O3()
        elif self.equipara("and", 43):
            self.R()
            self.O3()
        elif self.token in Follow['O3']:
            self.reglas.append(44)
        #else:
        #    self.error("Expected '||' / '&&' / 'λ' sign")

    def R(self) -> None:
        if self.equipara("id", 45):
            self.Rp()
        elif self.equipara("parAbirto", 46): return
        elif self.equipara("cteEnt", 47): return
        elif self.equipara("cadena", 48): return
        elif self.equipara("boolT", 49): return
        elif self.equipara("boolF", 50): return

    def Rp(self) -> None:
        if self.equipara("parAbierto", 51):
            self.L()
            if self.equipara("parCerrado"): return
        elif self.equipara("postIncrem", 52): return
        elif self.token in Follow["Rp"]:
            self.reglas.append(53)

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
        """Outputs containing Symbol Table with correct format to 'ts.txt' in directory specified in $lexer.outputdir"""
        with open(self.lexer.outputdir + "/ts.txt", "w") as f:
            f.write("TS GLOBAL #1")
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


class errorHandler:
    def __init__(self, lexer: Lexer, syntactic: Syntactic = None) -> None:
        self.lexer = lexer
        self.syntactic = syntactic

    def createErrorString(self, tipo: str, f) -> None:
        errList = None  # empty initializd
        if tipo == "lex":
            errList = self.lexer.errorList
        elif tipo == "syn":
            errList = self.syntactic.errorList
        if errList is not None:
            for errElem in errList:
                errorString = f"\nError code'{errElem.code}': {ERROR_MSG[errElem.code]}"
                if errElem.code == 4: errorString = Template(errorString).substitute(simbolo=errElem.att)
                if errElem.code == 7: errorString += ERROR_MSG[7]
                errorString += f"--> linea {errElem.line}"
                f.write(errorString)
        else:
            sys.exit("se ha intentado crear un ErrorString especificando mal de donde viene")

    def errorPrinter(self):
        with open(self.lexer.outputdir + "/errors.txt", "w") as f:
            header = f"Errors output for file '{self.lexer.filename}':\n "
            times = len(header) - 1
            header += "-" * times
            header = "-" * times + "\n" + header + "\nLexical errors: "
            f.write(header)
            self.createErrorString("lex", f)
            header = f"\nSyntactic errors':\n"
            times = len(header) - 1
            header += "-" * times
            header = "-" * times + "\n" + header
            f.write(header)
            self.createErrorString("syn", f)


def pipInstall(package):
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def checkDependencies(dependencies):
    """
       Checks and installs all dependencies needed for a projects

       Parameters
       ----------
       dependencies : Dict{key : str -> value : str}
           List of strings of dependencies that are wanted to be checked
           Must be named after pip given list
           Example:
       """
    import pkg_resources
    installed = [d for d in pkg_resources.working_set]
    for dep, realname in dependencies.items():
        if dep not in str(installed):
            print(f'Module {realname} is not installed and is necessary to run')
            answer = input('Do you want to install it (Y/N): ')
            if answer == "N" or answer == "n" or answer == "No":
                print(f"Exiting ... You must install the {realname} module for the processor to work")
                sys.exit()
            elif answer == "Y" or answer == "y" or answer == "Yes":
                print(f"Installing {realname}...")
                pipInstall(realname)


def getInput():
    """
    Gets the input from stdin or executes a certain file if none is given

    Parameters
    ----------
    file : str
        path to file to be executed, ignores stdin file
    """
    if len(sys.argv) > 2: sys.exit("Input file path to analyze as program argument")
    # manual path specification for debugging puropses
    if len(sys.argv) == 1:
        sys.exit(f"No file specified, see -h or -help for program usage")
    # file that the lexer will generate tokens for
    else:
        if sys.argv[1] in "-help":
            sys.exit("See help at https://github.com/nicocossiom/PdL")
        elif os.path.exists(os.getcwd() + "/" + sys.argv[1]):
            return open(sys.argv[1], "r")
        else:
            sys.exit(f"File \'{sys.argv[1]}\' does not exist")


def main():
    # dictionary of dependencies where key is the string used in the working set and value is the
    # actual name of the package that
    deps = {"ordered-set": "ordered_set"}
    checkDependencies(deps)

    f = getInput()

    lexer = Lexer(f)
    lexer.tokenize()
    lexer.printTokens()

    ts = TS(lexer)
    ts.printTS()

    syntactic = Syntactic(lexer)
    syntactic.startSyntactic()
    syntactic.exportParse()

    EH = errorHandler(lexer, syntactic)
    EH.errorPrinter()


if __name__ == "__main__":
    main()