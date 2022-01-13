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


# GLOBAL VARIABLES
FILE, FILENAME, OUTPUTDIR, TOKENLIST, PARSESTRING = None, None, None, [], None
TOKENFILE, PARSEFILE, TSFILE, ERRORFILE = None, None, None, None
LEXER, SYNTACTIC, SEMANTYC = None, None, None
LINES = None


def close_all_files():
    if TOKENFILE:
        TOKENFILE.close()
    if ERRORFILE:
        ERRORFILE.close()
    if PARSEFILE:
        PARSEFILE.close()
    if TSFILE:
        TSFILE.close()


def eprint(*args, **kwargs):
    """
    Prints the given parameters to stderr using special colors
    :param args:
    :param kwargs:
    """
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


def gen_error_line(line, start, end):
    """

    :param line: line from the given input file to get
    :param start: starting column to highlight from
    :param end: ending column to highlight to
    :return:
    """
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

    def __init__(self, msg: str, origin: str, linea: int, attr=None):
        """

        :param msg[str]: Error message
        :param origin[str]: string that signalizes from which part of the processor the error comes from
        :param linea[int]: line in that error occurs in
        :param attr[]:
        """
        self.msg = msg
        self.line = linea
        self.att = attr
        self.origin = origin
        self.print()

    def print(self):
        """
        Prints the error through stderr
        """
        error_str = "*" * 100 + f"\n{self.origin} at line {self.line}: \n{self.msg}\n" + "*" * 100 + "\n\n"
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
    "}": "llaveCerrado",
    "|": "or"
}


class Token:
    """A token representation for the processor"""

    def __init__(self, code: str, line, start_col, end_col, attribute=None):
        """

        :param error_string:
        :param line:
        :param start_col:
        :param end_col:
        :param attribute:
        """
        self.code = code
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
            self.col = 0
            self.nextChar()
            self.error("Comentarios de tipo '//comentario' no estan permitidos")
            self.line += 1

        else:
            self.error(f"Simbolo {self.car} no pertenece al lenguaje")

    def nextChar(self):
        """
        Reads the next character from the file while augmenting the column counter at the same time
        :return:
        """
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
        """Writes the given token in the token.txt file \n
        Format:  < code , [attribute] >
        """
        #
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
        error_string = gen_error_line(self.line, self.startCol, self.col) + "\n" + msg
        Error(error_string, "Lexical error", self.line, attr)

    # < codigo , atributo >
    def genToken(self, code: str, attribute=None) -> Token:
        """Generates a token and appends it to the list of tokens:\n
        -code: specifies token code (id,string,cteEnt,etc)
        -attribute: (OPTIONAL) specifies an attribute if the token needs it i.e < cteEnt , valor >
        """
        self.tokenizing = False
        generated_token = Token(code, self.line, self.startCol, self.col, attribute)
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
        while self.tokenizing:
            self.next()
            self.startCol = self.col
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
    "E": ["id", "parAbierto", "cteEnt", "cadena", "true", "false"],
    "N": ["id", "parAbierto", "cteEnt", "cadena", "true", "false"],
    "Z": ["id", "parAbierto", "cteEnt", "cadena", "true", "false"],
    "O1": ["mas", "por", "lambda"],
    "O2": ["equals", "mayor", "lambda"],
    "O3": ["or", "and", "lambda"],
    "R": ["id", "parAbierto", "cteEnt", "cadena", "true", "false"],
    "Rp": ["parAbierto", "postIncrem", "lambda"],
}

# usamos eof como $ para marcar fin de sentencia admisible
Follow = {
    "O1": ["puntoComa", "parCerrado", "coma"],
    "O2": ["mas", "por", "coma", "parCerrado", "puntoComa"],
    "O3": ["equals", "mayor", "mas", "por", "coma", "parCerrado", "puntoComa"],
    "X": "puntoComa",
    "C": "llaveAbierto",
    "L": "parCerrado",
    "Q": "parCerrado",
    "H": "parAbierto",
    "A": "parCerrado",
    "K": "parCerrado",
    "Rp": ["and", "mas", "por", "coma", "puntoComa", "parCerrado"],
}


def createLexer():
    global LEXER
    LEXER = Lexer()


class Syntactic:
    def __init__(self) -> None:
        createLexer()
        self.index = 0  # indice que apunta al elemento actual de la lista de tokens
        self.actualToken = None
        self.token = None

    def next(self) -> str:
        """
        Returns code (str) of the next token from the Lexer and stores the actual token in self
        :return: next Token
        """
        if self.token != "eof":
            self.actualToken: Token = LEXER.tokenize()
            self.token = self.actualToken.code
            return self.token

    def equipara(self, code: str, rule=None) -> bool:
        """
        Compares the given code to the actual token, return status based on said comparison.
        If regla is given means we're checking against a First of current state, rule should be given and if true
        add to parse list. If not rule then we're inside a production hence we know what tokens to expect and can
        error if comparison is false

        :param code: code of token expected in current syntactic position
        :param rule: rule to be added to the parse list
        :return: True if code == current token, else False
        """
        print(f"equipara({self.token} , {code} )", end="")
        if self.token == code:
            print("CORRECTO")
            if rule is not None:
                # only add rule when it's first check in a function (has regla), and we're sure it's the correct token
                Syntactic.addParseElement(rule)
            self.next()
            return True
        if rule is None:  # after first check (means we're in the middle of a state
            # we expected a certain token but it was not it, now we can say it's an error
            self.error("WrongTokenError", f"Received {code} - Expected another certain token",
                       TOKENLIST[self.index].line)
        print("INCORRECTO -> siguiente")
        return False

    def error(self, error_type, msg: string, attr=None):
        error_string = gen_error_line(self.actualToken.line, self.actualToken.startCol,
                                      self.actualToken.endCol) + "\n" + msg
        Error(error_string, error_type, self.actualToken.line, attr)

    @staticmethod
    def addParseElement(regla: int) -> None:
        """Writes the given parse element int the tokens.txt """
        global PARSESTRING
        if PARSESTRING is None:
            PARSESTRING = f"Descendente {regla}, ".replace("None", "")
        else:
            PARSESTRING += f"{regla},"
        print(PARSESTRING)

    def start(self):
        """Starts the Syntactic process"""
        self.next()
        self.P()
        PARSEFILE.write(PARSESTRING)
        eprint("Terminado")

    def P(self) -> None:
        if self.token in First["B"]:
            Syntactic.addParseElement(1)
            self.B()
            self.P()
        elif self.token in First['F']:
            Syntactic.addParseElement(2)
            self.F()
            self.P()
        elif self.equipara("eof"):
            Syntactic.addParseElement(3)
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
            Syntactic.addParseElement(6)
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
            Syntactic.addParseElement(18)
            self.E()
        elif self.token in Follow['X']:
            Syntactic.addParseElement(19)
        else:
            self.error("SentenceNotTerminatedError",
                       f"Esperaba ';' al terminar la sentencia, después de un return vacío")

    def C(self) -> None:
        if self.token in First["B"]:
            Syntactic.addParseElement(20)
            self.B()
            self.C()
        elif self.token in Follow['C']:
            Syntactic.addParseElement(21)

    def L(self) -> None:
        if self.token in First["E"]:
            Syntactic.addParseElement(22)
            self.E()
            self.Q()
        elif self.token in Follow['L']:
            Syntactic.addParseElement(23)
        else:
            self.error("FunctionCallError", "No se ha cerrado paréntesis en la llamada a la función")

    def Q(self) -> None:
        if self.equipara("coma", 24):
            self.E()
            self.Q()
        elif self.token in Follow['Q']:
            Syntactic.addParseElement(25)

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
            Syntactic.addParseElement(27)
            self.T()
        elif self.token in Follow['H']:
            Syntactic.addParseElement(28)
        else:
            self.error("TypeError", f"Tipo de función no aceptado. Debe usar {First['T']} o \"\" (no poner nada para "
                                    f"void)")

    def A(self) -> None:
        if self.token in First['T']:
            Syntactic.addParseElement(29)
            self.T()
            if self.equipara("id"):
                self.K()
        elif self.token in Follow['A']:
            Syntactic.addParseElement(30)
        else:
            self.error("FunctionCallError", f"No ha cerrado paréntesis en la llamada a la función")

    def K(self) -> None:
        if self.equipara("coma", 31):
            self.T()
            if self.equipara("id"):
                self.K()
        elif self.token in Follow['K']:
            Syntactic.addParseElement(32)
        else:
            self.error("FunctionArgumentDeclarationError", "Los argumentos de las funciones deben estar separados por "
                                                           "','")

    def E(self) -> None:
        if self.token in First["N"]:
            Syntactic.addParseElement(33)
            self.N()
            self.O1()

    def N(self) -> None:
        if self.token in First["Z"]:
            Syntactic.addParseElement(34)
            self.Z()
            self.O2()

    def Z(self) -> None:
        if self.token in First["R"]:
            Syntactic.addParseElement(35)
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
            Syntactic.addParseElement(38)
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
            Syntactic.addParseElement(41)
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
            Syntactic.addParseElement(44)
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
            Syntactic.addParseElement(53)


def createSyntactic():
    """Creates the Syntactic parser"""
    global SYNTACTIC
    SYNTACTIC = Syntactic()


class TS:
    CREATION_COUNTER = 0

    def __init__(self, name=None):
        self.map = {}
        self.name = "TSG" if name is None else name
        self.pos = 0
        self.creation_number = TS.CREATION_COUNTER
        TS.CREATION_COUNTER += 1

    def writeTS(self):
        """
        Writes the TS (self) in th the TS.txt file in the output directory
        :return:
        """
        TSFILE.write(str(self))

    def __str__(self):
        size_sep = 100
        name = "TABLA PRINCIPAL" if self.name == "TSG" else f"TABLA de función \"{self.name}\""
        final_string = "\n" + "-" * size_sep + f"\n\t\t\t{name} #{self.creation_number}\n"
        for lex, entrada in self.map.items():
            final_string += f"\n*  LEXEMA :     \"{lex}\"\n" \
                            f"\n   ATRIBUTOS : \n" \
                            f"\+Tipo: {entrada.tipo}\n" \

            if isinstance(entrada, TS.FunctionElement):
                final_string += f"\t\t+numParam: {entrada.numparam}\n\t\t\t"

                for i in range(len(entrada.tipo_params)):
                    final_string += f"+TipoParam{i}: {entrada.tipo_params[i]}\n\t\t\t"

                final_string += f"+TipoRetorno: {entrada.tipo_dev}" \

            else:
                final_string += f"\n  Despl: {entrada.desp}\n"
        return final_string + "-" * size_sep

    @staticmethod
    def get_desp(tipo):
        """
        Given a type returns its value for size
        :param tipo: type whose size we want to know
        :return: size of tipo in Bytes
        """
        res = 0  # function
        if tipo == "boolean":
            res = 1
        elif tipo == "int":
            res = 1
        elif tipo == "string":
            res = 8
        return res

    def buscarId(self, given_id: str):
        """
        Searches for an id in the table
        :param given_id: id we want to check
        :return: True if found, False if not
        """
        try:
            self.map[given_id]
        except KeyError:
            return False
        return True

    def addId(self, given_id: str, tipo: str, *args):
        """

        :param given_id:
        :param tipo:
        :param args:
        :return:
        """
        if not self.buscarId(given_id):
            if len(args) == 0:
                elem = TS.TSElement(self, given_id, tipo)
            else:
                elem = TS.FunctionElement(self, given_id, tipo, args)
            self.map[given_id] = elem
        else:
            raise Exception("Identificador ya existe en la TS actual")

    class TSElement:
        def __init__(self, ts, identifier: str, tipo: str):
            """
            :param identifier:
            :param tipo:
            """
            self.ts = ts
            self.lex = identifier
            self.tipo = tipo
            self.desp = self.ts.pos
            self.ts.pos += TS.get_desp(tipo)

    class FunctionElement(TSElement):
        def __init__(self, *args):
            """
            :param identifier:
            :param tipo
            :param *args:
                See below
            *param 1(List[str]): tipo_params
            """
            super().__init__(args[0], args[1], args[2])
            self.tipo_params = [elem for elem in args[3][0]]
            self.numparam = len(self.tipo_params)
            self.tipo_dev = self.tipo


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


if __name__ == "__main__":
    createProcessor()
    createLexer()
    createSyntactic()
    SYNTACTIC.start()
    # while True:
    #     token = LEXER.tokenize()
    #     if token is not None and token.code == "eof":
    #         break
    close_all_files()  # closes all file descriptors
