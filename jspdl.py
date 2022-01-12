import os
import string
import sys
from typing import List


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# GLOBAL VARIABLES -> used all along the program
FILE, FILENAME, OUTPUTDIR, TOKENLIST = None, None, None, [], 
TOKENFILE, PARSEFILE, TSFILE, ERRORFILE = None, None, None, None
LEXER, SYNTACTIC, SEMANTYC = None, None, None
LINES = None


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def createProcessor():
    """
    Checks if a file name has been given as an argument, if it has and is a correct file does the following:
    1. Creates the output folder with the name of the argument without an extension
    2. Creates all files for output, those being:
        - tokens.txt
        - parse.txt
        - ts.txt
        - errors.txt
    """
    global FILE, FILENAME, OUTPUTDIR, TOKENLIST, TOKENFILE, PARSEFILE, TSFILE, ERRORFILE
    num = len(sys.argv)
    if num > 2:
        sys.exit("Input file path to analyze as program argument")
    # elif num == 1:
    #     FILE = sys.stdin
    #     TOKENFILE = sys.stdout
    #     ERRORFILE = sys.stderr
    #     PARSEFILE = sys.stdout
    #     TSFILE = sys.stdout
    #     FILE.write(FILE.readline())
    elif num == 2:
        if sys.argv[1] in "-help":
            sys.exit("See help at https://github.com/nicocossiom/PdL")
        else:
            if os.path.exists(os.getcwd() + "/" + sys.argv[1]):
                FILE = open(sys.argv[1], "r")
                FILENAME = os.path.basename(FILE.name)
                OUTPUTDIR = os.getcwd() + "/" + FILENAME.replace(".jspdl", "")
                try:
                    os.mkdir(OUTPUTDIR)
                except FileExistsError:
                    pass
                except OSError:
                    f"Error al crear carpeta de volcado en: {OUTPUTDIR}"
                print(f"Directorio de volcado del programa creado en: {OUTPUTDIR}")
                TOKENFILE = open(OUTPUTDIR + "/tokens.txt", "w")
                ERRORFILE = open(OUTPUTDIR + "/errors.txt", "w")
                PARSEFILE = open(OUTPUTDIR + "/parse.txt", "w")
                TSFILE = open(OUTPUTDIR + "/ts.txt", "w")
            else:
                sys.exit(f"File \'{sys.argv[1]}\' does not exist")


def ger_error_line(line, start, end):
    global LINES
    if not LINES:
        fd = open(sys.argv[1], "r")
        LINES = fd.readlines()
    line = Colors.OKBLUE + LINES[line - 1]
    if line[-1:] != "\n": 
        line += "\n"
    line = Colors.ENDC + line + Colors.FAIL
    line += " " * start
    line += Colors.WARNING + "^" + "~" * (end - 1) + Colors.FAIL
    return line


class Error:
    """
    Global error class used for all parts of the procesor. Each part must define its own error() method
    that creates an Error and adds it to the list of errors of said class
    """

    def __init__(self, msg: string, origin: str, linea: int, attr=None):
        """
        msg = msg

        """
        self.msg = msg
        self.line = linea
        self.att = attr
        self.origin = origin
        self.print()

    def print(self):
        error_str = f"{self.origin} at line {self.line}: \n{self.msg}"
        eprint(Colors.FAIL + error_str + Colors.ENDC)
        ERRORFILE.write(error_str)


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


class Token:
    def __init__(self, error_string: str, line, start_col, end_col, attribute=None):
        self.code = error_string
        self.att = attribute
        self.line = line
        self.startCol = start_col
        self.endCol = end_col

    def print(self):
        print(f"{self.code},{self.att} line: {self.line}, cols: {self.startCol} -> {self.endCol}")


class Lexer:
    def __init__(self):
        self.num = 0  # current integer number being constructed
        self.lex = ""  # current string being constructed
        self.car = ""  # current character being read
        self.line = 1
        self.tokenizing = True  # keeps track of if a token is being built -> True:yes, False:No
        self.col = 0
        self.startCol = 0

    def skipBlockComments(self):
        """Skips block comments and detects error in its specification"""
        self.nextChar()
        if self.car == "*":
            self.nextChar()
            while Lexer.peekNextCar() != "/" and self.car != "*" and self.car != "":
                self.nextChar()
                if self.car == "": 
                    self.error("Comentario de bloque no cerrado")
                if self.car == "\n":
                    self.line += 1
                    self.startCol = 0
                    self.col = 0
            self.nextChar()
            self.nextChar()
        elif self.car == "/":
            FILE.readline()
            self.line += 1
            self.col = 0
            self.error("Comentarios de tipo '//comentario' no estan permitidos")
        else:
            self.error("Simbolo '$simbolo' no pertenece al lenguaje", self.car)

    def nextChar(self):
        self.car = FILE.read(1)
        self.col += 1

    def skipDelimeters(self):
        """Skips delimiters such as \\t and \\n """
        if self.car != "":
            while self.car != "" and ord(self.car) < 33:
                if self.car == "\n":
                    self.line += 1
                    self.col = -1
                    self.startCol = 0
                if self.car == "":
                    break  # Block comment processing
                self.nextChar()
            if self.car == "/":
                self.skipBlockComments()
                self.skipDelimeters()

    def next(self):
        """Retrieves next character recognized in the language for processing"""
        self.nextChar()
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
        
    @staticmethod
    def writeToken(given_token: Token):
        """Writes the given token in the token.txt file"""
        # del* < código del* , del* [atributo] del* > del* RE
        TOKENFILE.write(f"< {given_token.code} , {given_token.att} >\n")  
    
    @staticmethod
    def peekNextCar() -> str:
        """Returns the character next to that which the file pointer is at, without advancing said file pointer"""
        pos = FILE.tell()
        car = FILE.read(1)
        FILE.seek(pos)
        return car

    def error(self, msg: string, attr=None):
        self.tokenizing = False
        error_string = ger_error_line(self.line, self.startCol, self.col) + "\n" + msg
        Error(error_string, "Lexical error", self.line, attr)

    # < codigo , atributo >
    def genToken(self, error_string: str, attribute=None) -> Token:
        """Generates a token and appends it to the list of tokens:\n
        -code: specifies token code (id,string,cteEnt,etc)
        -attribute: (OPTIONAL) specifies an attribute if the token needs it i.e < cteEnt , valor >
        """
        self.tokenizing = False
        generated_token = Token(error_string, self.line, self.startCol, self.col, attribute)
        TOKENLIST.append(generated_token)
        self.writeToken(generated_token)
        self.lex = ""
        return generated_token

    def getQuotation(self):
        """
        Looks for \" inside a string, if found it concatenates " to the string and advances to
        the next (not looked at) character and tries to find another following quotation
        :return: False if there is no next quotation
        """
        if self.car != "" and self.car == "\\" and Lexer.peekNextCar() == '\"':
            self.nextChar()
            self.concatenate()
            self.nextChar()
            return True if self.getQuotation() else False
        else:
            return False

    def tokenize(self):
        """
        Goes through the characters, generates a token if found, and lexical errors if any occur.
        Returns said Token
        """
        result = None  # token to be returned to the Syntactic
        self.tokenizing = True  # start to tokenize
        if Lexer.peekNextCar() == "":
            result = self.genToken("eof")  # llega al final de archivo -> eof
        self.startCol = self.col
        while self.tokenizing:
            self.next()
            # Integer being formed
            if self.car.isdigit() and self.lex == "":
                self.generateNumber()
                if not Lexer.peekNextCar().isdigit():
                    if self.num < 32768:
                        result = self.genToken("cteEnt", self.num)
                    else:
                        self.error("Digito con valor mayor al permitido (32768) en el sistema")

            # Identifiers or Reserved Words
            elif self.car in LETTERS or self.lex != "":
                self.concatenate()
                next_car = Lexer.peekNextCar()
                if not next_car.isdigit() and next_car not in LETTERS and next_car != "_" or next_car == "":
                    if self.lex in RES_WORD:
                        result = self.genToken(self.lex)
                    else:
                        if len(self.lex) < 65:
                            result = self.genToken("id", self.lex)
                        else:
                            self.error(f"Identificador {self.lex} excede el tamaño máximo de caracteres permitido (64)")

            # String (cadena) processing
            elif self.car == "\"":
                self.next()
                while self.car != "" and not self.getQuotation() and self.car != "\"":
                    self.concatenate()
                    self.nextChar()
                if self.car == "":
                    self.error("EOF mientras se escaneaba una cadena")
                elif len(self.lex) < 65:
                    result = self.genToken("cadena", self.lex)
                else:
                    self.error("Cadena excede el tamaño máximo de caracteres permitido (64)")

            # Operators, symbols
            elif self.car in SYMB_OPS:
                # + or ++
                if self.car == "+":
                    if Lexer.peekNextCar() == "+":
                        result = self.genToken("postIncrem")
                        self.next()
                    else:
                        result = self.genToken("mas")
                # &&
                elif self.car == "&" and Lexer.peekNextCar() == "&":
                    result = self.genToken("and")
                    self.next()
                elif self.car == "|" and Lexer.peekNextCar() == '|':
                    result = self.genToken("or")
                    self.next()
                # = or ==
                elif self.car == "=":
                    if Lexer.peekNextCar() == "=":
                        result = self.genToken("equals")
                        self.next()
                    else:
                        result = self.genToken("asig")
                else:
                    result = self.genToken(SYMB_OPS[self.car])
            elif self.car in "\'":
                self.nextChar()
                while self.car != "\'":
                    self.nextChar()
                if self.car != "":
                    self.error("Cadena se debe especificar entre \" \", no con \' \'")
                else:
                    self.error("Cadenas deben ir entre \" \"")
            else:
                self.error(
                    f"Símbolo: \"{self.car}\" no permitido. \nNo pertence al lenguaje, consulte la documentación para "
                    f"ver carácteres aceptados") 
        return result


First = {
    'P': ["function", "eof", "let", "if", "do", "id", "return", "print", "input"],
    'B': ["let", "if", "do", "id", "return", "print", "input"],
    "T": ["int", "boolean", "string"],
    "S": ["id", "return", "print", "input"],
    "Sp": ["asig", "parAbierto", "postIncrem"],
    "X": ["id", "parAbierto", "cteEnt", "cadena", "true", "false", "lambda"],
    "C": ["let", "if", "id", "return", "print", "input", "do"],
    "L": ["id", "parAbierto", "cteEnt", "cadena", "true", "false"],
    "Q": "coma",
    "F": "function",
    "H": ["int", "boolean", "string"],
    "A": ["int", "boolean", "string"],
    "K": "coma",
    "E": ["mas", "por", "lambda"],
    "N": ["equals", "mayor", "lambda"],
    "Z": ["or", "and", "lambda"],
    "O1": ["mas", "por", "lambda"],
    "O2": ["equals", "mayor", "lambda"],
    "O3": ["or", "and", "lambda"],
    "R": ["id", "parAbierto", "cteEnt", "cadena", "true", "false"],
    "Rp": ["parAbierto", "postIncrem", "lambda"],
}

# usamos eof como $ para marcar fin de sentencia admisible
Follow = {
    "O1": ["puntoComa", "parCerrado", "coma"],
    "O2": ["mas", "por", "lambda"],
    "O3": ["equals", "mayor", "lambda"],
    "X": "puntoComa",
    "C": "llaveAbierto",
    "L": "parCerrado",
    "Q": "parCerrado",
    "H": "parAbierto",
    "A": "parCerrado",
    "K": "parCerrado",
    "Rp": ["and", "mas", "por", "equals", "mayor", "lambda", "coma", "puntoComa", "parCerrado"],
}


def createLexer():
    global LEXER
    LEXER = Lexer()
    print("created lexer")


class Syntactic:

    def __init__(self) -> None:
        createLexer()
        self.index = 0  # indice que apunta al elemento actual de la lista de tokens
        self.actualToken = TOKENLIST[self.index]
        self.token = self.actualToken.code

    def next(self) -> Token:
        if self.token != "eof":
            comp_str = "\nnext: " + self.token
            self.index += 1
            self.actualToken: Token = LEXER.tokenize()
            self.token = self.actualToken.code
            print(comp_str + " -> " + self.token)
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
        if regla is None:  # after first check (means we're in the middle of a state
            # we expected a certain token but it was not it, now we can say it's an error
            self.error("WrongTokenError", f"Received {code} - Expected another certain token",
                       TOKENLIST[self.index].line)
        print("INCORRECTO -> siguiente")
        return False

    def error(self, error_type, msg: string, attr=None):
        error_string = ger_error_line(self.actualToken.line, self.actualToken.startCol, self.actualToken.endCol)\
                       + "\n" + msg
        Error(error_string, error_type,  self.line, attr)

    @staticmethod
    def addParseElement(regla: int) -> None:
        """Writes the given parse element int the tokens.txt """
        if regla == 1 or regla == 2:
            parsed_str = f"Descendente {regla}, ".replace("None", "")
        else:
            parsed_str = f"{regla} ".replace("None", "")
        PARSEFILE.write(parsed_str, 'a')

    def startSyntactic(self):
        self.P()
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
        elif (self.equipara("input", 14) and self.equipara("parAbierto") and self.equipara(
                "id") and self.equipara("parCerrado") and self.equipara("puntoComa")):
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

    def X(self) -> None:
        if self.token in First['E']:
            self.reglas.append(18)
            self.E()
        elif self.token in Follow['X']:
            self.reglas.append(19)
        else:
            self.error("SentenceNotTerminatedError", f"Esperaba ';' al terminar la sentencia, después de un return vacío")

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
            self.error("FunctionCallError", "No se ha cerrado paréntesis en la llamada a la función")

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
            self.error("TypeError", f"Tipo de función no aceptado. Debe usar {First['T']} o \"\" (no poner nada para "
                                    f"void)")

    def A(self) -> None:
        if self.token in First['T']:
            self.reglas.append(29)
            self.T()
            if self.equipara("id"):
                self.K()
        elif self.token in Follow['A']:
            self.reglas.append(30)
        else:
            self.error("FunctionCallError", f"No ha cerrado paréntesis en la llamada a la función")

    def K(self) -> None:
        if self.equipara("coma", 31):
            self.T()
            if self.equipara("id"):
                self.K()
        elif self.token in Follow['K']:
            self.reglas.append(32)
        else:
            self.error("FunctionArgumentDeclarationError", "Los argumentos de las funciones deben estar separados por "
                                                           "','")

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
        else:
            self.error("NonSupportedOperationError", f"Esperaba uno de los siguientes símbolos{Follow['O1']}")

    def O2(self) -> None:
        if self.equipara("equals", 39):
            self.R()
            self.O2()
        elif self.equipara("mayor", 40):
            self.R()
            self.O2()
        elif self.token in Follow['O2']:
            self.reglas.append(41)
        else:
            self.error("NonSupportedOperationError", f"Esperaba uno de los siguientes símbolos{Follow['O2']}")

    def O3(self) -> None:
        if self.equipara("or", 42):
            self.R()
            self.O3()
        elif self.equipara("and", 43):
            self.R()
            self.O3()
        elif self.token in Follow['O3']:
            self.reglas.append(44)
        else:
            self.error("NonSupportedOperationError", f"Esperaba uno de los siguientes símbolos{Follow['O3']}")

    def R(self) -> None:
        if self.equipara("id", 45):
            self.Rp()
        elif self.equipara("parAbierto", 46):
            return
        elif self.equipara("cteEnt", 47):
            return
        elif self.equipara("cadena", 48):
            return
        elif self.equipara("true", 49):
            return
        elif self.equipara("false", 50):
            return

    def Rp(self) -> None:
        if self.equipara("parAbierto", 51):
            self.L()
            if self.equipara("parCerrado"):
                return
        elif self.equipara("postIncrem", 52):
            return
        elif self.token in Follow["Rp"]:
            self.reglas.append(53)


class TS:
    class TSElement:
        def __init__(self, identifier: str, tipo, tipo_param: List[str] = None, tipo_dev: str = None):
            self.lex = identifier
            self.tipo = tipo
            if tipo == "function":
                self.tipo_params = tipo_param
                self.numparam = len(tipo_param)
                self.tipo_dev = tipo_dev
            self.desp = TS.pos
            TS.pos += self.desp

    def __init__(self, name=None):
        self.map = {}
        self.name = "TSG" if not None else name

    def buscarId(self, given_id):
        try:
            self.map[given_id]
        except KeyError:
            return False
        return True

    def addId(self, given_id, **kwargs):
        if not self.buscarId(given_id):
            TS.TSElement(given_id, kwargs[1], kwargs[2], kwargs[3], kwargs[4])
        else:
            raise Exception("Identificador ya existe en la TS actual")


def dictFromTokenList():
    d = {}
    for token in TOKENLIST:
        try:
            d[token.line] += f"  |  <{token.code},{token.att} {token.startCol} {token.endCol}>"
        except KeyError:
            d[token.line] = f"   {token.code} {token.att} {token.startCol} {token.endCol}"
    for line, tokens in d.items():
        print(f"{line}-> {tokens}")
    return d


# class ErrorHandler:
#     def __init__(self, lexer: Lexer, syntactic: Syntactic = None) -> None:
#         LEXER = lexer
#         self.syntactic = syntactic
#
#     def createErrorString(self, tipo: str, f) -> None:
#         errList = None  # empty initializd
#         if tipo == "lex":
#             errList = LEXER.errorList
#         elif tipo == "syn":
#             errList = self.syntactic.errorList
#         if errList is not None:
#             for errElem in errList:
#                 errorString = f"\nError code'{errElem.code}': {ERROR_MSG[errElem.code]}"
#                 if errElem.code == 4: errorString = Template(errorString).substitute(simbolo=errElem.att)
#                 if errElem.code == 7: errorString += ERROR_MSG[7]
#                 errorString += f"--> linea {errElem.line}"
#                 f.write(errorString)
#         else:
#             sys.exit("se ha intentado crear un ErrorString especificando mal de donde viene")
#
#     def errorPrinter(self):
#         with open(LEXER.outputdir + "/errors.txt", "w") as f:
#             header = f"Errors output for file '{LEXER.filename}':\n "
#             times = len(header) - 1
#             header += "-" * times
#             header = "-" * times + "\n" + header + "\nLexical errors: "
#             f.write(header)
#             self.createErrorString("lex", f)
#             header = f"\nSyntactic errors':\n"
#             times = len(header) - 1
#             header += "-" * times
#             header = "-" * times + "\n" + header
#             f.write(header)
#             self.createErrorString("syn", f)

if __name__ == "__main__":
    createProcessor()
    createLexer()
    while True:
        token = LEXER.tokenize()
        if token is not None and token.code == "eof":
            break
    # dictFromTokenList()
    if TOKENFILE:
        TOKENFILE.close()
    if ERRORFILE:
        ERRORFILE.close()
    if PARSEFILE:
        PARSEFILE.close()
    if TSFILE:
        TSFILE.close()
