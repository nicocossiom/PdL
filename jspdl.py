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
    global FILE, FILENAME, OUTPUTDIR, TOKENLIST, TOKENFILE, PARSEFILE, TSFILE, ERRORFILE, PARSESTRING, LINES

    FILE, FILENAME, OUTPUTDIR, TOKENLIST, PARSESTRING = None, None, None, [], None
    TOKENFILE, PARSEFILE, TSFILE, ERRORFILE = None, None, None, None
    LINES = None

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
                OUTPUTDIR = os.getcwd() + "/" + FILENAME.replace(".js", "")
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
    writing_line = LINES[line - 1]
    line = Colors.OKBLUE + LINES[line - 1]
    if line[-1:] != "\n":
        line += "\n"
        writing_line += "\n"
    line = Colors.ENDC + line + Colors.FAIL
    line += " " * start
    writing_line += " " * start + "^" + "~" * (end - 1)
    line += Colors.WARNING + "^" + "~" * (end - 1) + Colors.FAIL
    return line, writing_line


class Error:
    """
    Global error class used for all parts of the procesor. Each part must define its own error() method
    that creates an Error and adds it to the list of errors of said class
    """

    def __init__(self, msg: str, origin: str, linea: int, writing_line: str, attr=None):
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
        self.writing_line = writing_line
        self.print()

    def print(self):
        """
        Prints the error through stderr
        """
        error_str = "*" * 75 + f"\n{self.origin} at line {self.line}: \n{self.msg}\n" + "*" * 75 + "\n\n"
        writing_line = "*" * 75 + f"\n{self.origin} at line {self.line}: \n{self.writing_line}\n" + "*" * 75 + "\n\n"
        eprint(Colors.FAIL + error_str + Colors.ENDC)
        ERRORFILE.write(writing_line)


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
        self.col = 1
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
                    self.col = 1
            self.nextChar()
            self.nextChar()
        elif self.car == "/":
            FILE.readline()
            self.col = 1
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
                    self.col = 1
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
        strings = gen_error_line(self.line, self.startCol, self.col)
        Error(strings[0] + "\n" + msg, "Lexical error", self.line, strings[1] + "\n" + msg, attr)

    # < codigo , atributo >
    def genToken(self, code: str, attribute=None) -> Token:
        """Generates a token and appends it to the list of tokens:\n
        -code: specifies token code (id,string,cteEnt,etc)
        -attribute: (OPTIONAL) specifies an attribute if the token needs it i.e < cteEnt , valor >
        """
        self.tokenizing = False
        generated_token = Token(code, self.line, self.startCol, self.col, attribute)
        global TOKENLIST
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
        if self.car != "" and self.car == "\\" and (Lexer.peekNextCar() == '\"' or Lexer.peekNextCar() == "\'"):
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
            if self.car == "": break
            # Integer being formed
            if self.car.isdigit() and self.lex == "":
                self.generateNumber()
                if not Lexer.peekNextCar().isdigit():
                    if self.num < 32768:
                        self.num = 0
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
            elif self.car == "\"" or self.car == "\'":
                if self.car == "\'":
                    self.error("Cadena se debe especificar entre \" \", no con \' \'. Corregido")
                self.next()
                while self.car != "" and not self.getQuotation() and (self.car != "\"" and self.car != '\''):
                    self.concatenate()
                    self.nextChar()
                if self.car == "":
                    self.error("Cadena debe ir entre \", falta el segundo")
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
            else:
                self.error(
                    f"Simbolo: \"{self.car}\" no permitido. \nNo pertence al lenguaje, consulte la documentacion para "
                    f"ver carácteres aceptados")
                while self.car != "":
                    self.tokenize()
        return result


First = {
    'P': ["function", "eof", "let", "if", "do", "id", "return", "print", "input"],
    'B': ["let", "if", "do", "id", "return", "print", "input"],
    "T": ["int", "boolean", "string"],
    "S": ["id", "return", "print", "input"],
    "Sp": ["asig", "parAbierto", "postIncrem"],
    "X": ["id", "parAbierto", "int", "cadena", "true", "false", "lambda"],
    "C": ["let", "if", "id", "return", "print", "input", "do"],
    "L": ["id", "parAbierto", "int", "cadena", "true", "false"],
    "Q": "coma",
    "F": "function",
    "H": ["int", "boolean", "string"],
    "A": ["int", "boolean", "string"],
    "K": "coma",
    "E": ["id", "parAbierto", "int", "cteEnt", "cadena", "true", "false", "and", "or", "lambda", "mayor", "equals"],
    "N": ["id", "parAbierto", "int", "cteEnt", "cadena", "true", "false", "and", "or", "lambda", "mayor", "equals"],
    "Z": ["id", "parAbierto", "int", "cteEnt", "cadena", "true", "false", "mas", "por", "lambda"],
    "O1": ["and", "or", "lambda"],
    "O2": ["equals", "mayor", "lambda"],
    "O3": ["por", "mas", "lambda"],
    "R": ["id", "parAbierto", "cteEnt", "cadena", "true", "false"],
    "Rp": ["parAbierto", "postIncrem", "lambda"],
}

# usamos eof como $ para marcar fin de sentencia admisible
Follow = {
    "O1": ["puntoComa", "parCerrado", "coma"],
    "O2": ["mayor", "equals", "parCerrado", "puntoComa", "coma", "and", "or"],
    "O3": ["mayor", "equals", "parCerrado", "coma", "and", "or", "puntoComa"],
    "X": "puntoComa",
    "C": "llaveCerrado",
    "L": "parCerrado",
    "Q": "parCerrado",
    "H": "parAbierto",
    "A": "parCerrado",
    "K": "parCerrado",
    "Rp": ["or", "and", "mas", "por", "coma", "puntoComa", "parCerrado", "equals", "mayor"],
}
SYMB_OPS_R = {
    "mas": "+",
    "por": "*",
    "and": "&&",
    "asig": "=",
    "mayor": ">",
    "coma": ",",
    "puntoComa": ";",
    "parAbierto": "(",
    "parCerrado": ")",
    "llaveAbierto": "{",
    "llaveCerrado": "}",
    "or": "||",
    "postIncrem": "++"
}


def createLexer():
    global LEXER
    LEXER = Lexer()


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
        size_sep = 75
        name = "TABLA PRINCIPAL" if self.name == "TSG" else f"TABLA de funcion \"{self.name}\""
        final_string = "\n" + "-" * size_sep + f"\n\t\t\t{name} #{self.creation_number}\n"
        for lex, entrada in self.map.items():
            final_string += f"\n*  LEXEMA : \"{lex}\"" \
                            f"\n   ATRIBUTOS : \n\t\t" \
                            f"+ Tipo: {entrada.tipo}\n"
            if isinstance(entrada, TS.FunctionElement):
                final_string += f"\t\t+numParam: {entrada.num_param}\n\t\t\t"

                for i in range(len(entrada.tipo_params)):
                    final_string += f"+ TipoParam{i}: {entrada.tipo_params[i]}\n\t\t\t"

                final_string += f"+TipoRetorno: {entrada.tipo_dev}\n"
            else:
                final_string += f"\t\t+ Despl: {entrada.desp}\n"
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

    def insertarId(self, given_id: str, tipo: str, *args):
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
            return elem
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
            self.num_param = args[3][1]
            self.tipo_dev = args[3][2]

    # def insertarTipoDev(self, id, tipo):
    #     try:
    #         self.map[id].tipo_dev = tipo
    #     except KeyError:
    #         sys.exit(f"No existe el id dado: {id} en la tabla")


def dictFromTokenList():
    d = {}
    global TOKENLIST
    for token in TOKENLIST:
        try:
            d[token.line] += f"  |  <{token.code},{token.att} {token.startCol} {token.endCol}>"
        except KeyError:
            d[token.line] = f"   {token.code} {token.att} {token.startCol} {token.endCol}"
    for line, tokens in d.items():
        print(f"{line}-> {tokens}")
    return d


class ProductionObject:
    def __init__(self, **kwargs: object) -> None:
        r"""
        An object representing a Syntactic production rule which holds values for a Semantic functions
        :param \**kwargs:
                See below
            :Keyword Arguments:
            * *tipo* (``str``) --
              Extra stuff
            * *ancho* (``str``) --
            * *tipoRet* (``str``) --

        """
        try:
            self.tipo = kwargs["tipo"]
        except KeyError:
            self.tipo = None
        try:
            self.ancho = kwargs["ancho"]
        except KeyError:
            self.ancho = None
        try:
            self.tipoRet = kwargs["tipoRet"]
        except KeyError:
            self.tipoRet = None


class Syntactic:
    # Tablas de Símbolos class (static vars of shared by all members of the class) variables,
    # which will be referred to as self.{} inside the methods, but they're not instance class variables
    TSG: TS = None
    TSActual: TS = None
    TSLIST = []

    def __init__(self) -> None:
        createLexer()
        self.index = 0  # indice que apunta al elemento actual de la lista de tokens
        self.actualToken: Token = None
        self.token = None
        self.lastToken = None
        self.lastActualToken = None

    def next(self) -> Token:
        """
        Returns code (str) of the next token from the Lexer and stores the actual token in self
        :return: next Token
        """
        self.lastActualToken = self.actualToken
        self.lastToken = self.actualToken
        self.actualToken: Token = LEXER.tokenize()
        self.index += 1
        if not self.actualToken:
            return self.next()
        else:
            self.token = self.actualToken.code
            return self.actualToken

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
        # print(f"equipara({self.token} , {code} )", end="")

        if self.token == code:
            # print("CORRECTO")
            if rule:
                # only add rule when it's first check in a function (has regla), and we're sure it's the correct token
                Syntactic.addParseElement(rule)
            self.next()
            return True
        if not rule:  # after first check (means we're in the middle of a state
            # we expected a certain token but it was not it, now we can say it's an error
            if self.token == "eof":
                self.lastActualToken = TOKENLIST[-2]
                try:
                    symbol = SYMB_OPS_R[code]
                except KeyError:
                    symbol = code
                self.error("WrongTokenError", f"No ha cerrado con {symbol}")
            try:
                symbol = SYMB_OPS_R[code]
            except KeyError:
                symbol = code
            self.error("WrongTokenError", f"Recibido {symbol} - Esperaba el token {self.token}",
                       True)
        # print("INCORRECTO -> siguiente")
        return False

    def equierror(self, expected):
        expected_with_symbol = []
        try:
            symbol = SYMB_OPS_R[self.token]
            for elem in expected:
                try:
                    expected_with_symbol.append(SYMB_OPS_R[elem])
                except KeyError:
                    expected_with_symbol.append(elem)

        except KeyError:
            symbol = self.token
        self.error("WrongTokenError",
                   f"Recibido \"{symbol}\" - Esperaba uno de los siguientes tokens {expected_with_symbol}", True)

    def error(self, error_type, msg: string, attr=None):
        if self.token == "eof":
            self.lastActualToken = TOKENLIST[-2]
        token = self.actualToken if attr else self.lastActualToken
        strings = gen_error_line(token.line, token.startCol, token.endCol)
        Error(strings[0] + "\n" + msg, error_type, token.line,
              strings[1] + "\n" + msg, attr)
        sys.exit("Error fatal, saliendo ...")

    @staticmethod
    def addParseElement(regla: int) -> None:
        """Writes the given parse element int the tokens.txt """
        global PARSESTRING
        if PARSESTRING is None:
            PARSESTRING = f"Descendente {regla} ".replace("None", "")
        else:
            PARSESTRING += f"{regla} "
        # print(PARSESTRING)

    def start(self):
        """Starts the Syntactic process"""
        self.TSG = TS()
        self.TSLIST.append(self.TSG)
        self.TSActual = self.TSG
        self.next()
        self.P()
        PARSEFILE.write(PARSESTRING)
        print(Colors.OKGREEN + f"Archivo {sys.argv[1]} analizado, es correcto" + Colors.ENDC
              + "\nErrores corregidos durante el análisis:")

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
            self.writeTS()
            return

    def B(self) -> ProductionObject(tipo=True):
        if self.equipara("let", 4):
            T = self.T()
            id = self.actualToken.att
            if self.equipara("id"):
                if self.equipara("puntoComa"):
                    if not self.TSActual.buscarId(id):
                        self.TSActual.insertarId(id, T.tipo)
                    return
        elif self.equipara("if", 5) and self.equipara("parAbierto"):
            E = self.E()
            if not E:
                self.error("EmptyConditionError", "La condición está vacía")
            if self.equipara("parCerrado"):
                if self.token == "llaveAbierto":
                    self.error("IfBlockError", "Solo estan soportados los ifs simples")
                self.S()
                if E.tipo != "boolean":
                    self.error("WrongDataTypeError",
                               "El tipo de E tiene que ser boolean ya que nos encontramos en la condición de if")
        elif self.token in First["S"]:
            Syntactic.addParseElement(6)
            self.S()
        elif self.equipara("do", 7):
            if self.equipara("llaveAbierto"):
                self.C()
                if self.equipara("llaveCerrado") and self.equipara("while") and self.equipara("parAbierto"):
                    E = self.E()
                    if not E:
                        self.error("EmptyConditionError", "La condición está vacía")
                    if self.equipara("parCerrado") and self.equipara("puntoComa"):
                        if E.tipo != "boolean":
                            self.error("WrongDataTypeError", "La condición del while debe ser de tipo booleano")
        else:
            self.equierror(First["B"])

    def T(self) -> ProductionObject:
        if self.equipara("int", 8):
            return ProductionObject(tipo="int", ancho=1)
        elif self.equipara("boolean", 9):
            return ProductionObject(tipo="boolean", ancho=1)
        elif self.equipara("string", 10):
            return ProductionObject(tipo="string", ancho=64)
        self.error("TypeError", f"Tipo {self.token} no reconocido, tipos disponibles {First['T']}", True)

    def S(self) -> ProductionObject:
        id = self.actualToken.att
        if self.equipara("id", 11):
            Sp = self.Sp()
            if not Sp or isinstance(Sp.tipo, list):  # es una llamada a funcion
                if self.TSG.buscarId(id):
                    id: TS.FunctionElement = self.TSG.map[id]
                    params = id.tipo_params
                    if Sp:
                        params_dados = Sp.tipo
                        if id.tipo == "function" and params != params_dados:  # funcion con parametros incorrectos
                            self.error("ArgumentTypeError", f"La funcion {id} recibe los argumentos de tipo "
                                                            f"{params}, tipos recibidos {params_dados}")
                else:
                    self.error("NonDeclaredError", f"Error la función {id} no ha sido declarada previamente")
            else:  # es una asignacion
                var_tabla = None
                if self.TSActual.buscarId(id):
                    var_tabla = self.TSActual.map[id]
                elif self.TSG.buscarId(id):
                    var_tabla = self.TSG.map[id]
                if not var_tabla:  # declaracion e inicialización de una variable global i.e (a = 5)
                    if Sp.tipo == "int":
                        id: TS.TSElement = self.TSG.insertarId(id, Sp.tipo)
                        if Sp.tipo != "postIncrem" and id.tipo != Sp.tipo:
                            self.error("TypeError",
                                       f"Tipo de la variable: \"{id.lex}\" no coincide con tipo tipo de la asignación: \"{Sp.tipo}\"")
                        return ProductionObject(tipo=True)
                    else:
                        self.error("TypeError", f"Solo se pueden hacer asignaciones sin inicializacion cuando la asignacion es de tipo int, en este caso es de tipo {Sp.tipo}")
                elif Sp.tipo == "postIncrem" and var_tabla.tipo != "int":
                    self.error("WrongDataTypeError",
                               "El operador post incremento solo es aplicable a variables del tipo entero")
                elif Sp.tipo != "postIncrem" and var_tabla.tipo != Sp.tipo:  # es una asignacion normal
                    self.error("TypeError", f"Tipo de la variable: \"{var_tabla.tipo}\" no coincide con el tipo de la asignación: \"{Sp.tipo}\"")

        elif self.equipara("return", 12):
            X = self.X()
            if self.equipara("puntoComa"):
                return ProductionObject(tipo=True, tipoRet=X.tipo)

        elif self.equipara("print", 13):
            if self.equipara("parAbierto"):
                E = self.E()
                if not E:
                    self.error("EmptyConditionError", "La condición está vacía")
                if self.equipara("parCerrado") and self.equipara("puntoComa"):
                    if E.tipo in {"string", "int"}:
                        return ProductionObject(tipo=True)
                    else:
                        self.error("WrongDataTypeError", "La función print solo acepta parámetros de tipo string")

        elif self.equipara("input", 14) and self.equipara("parAbierto"):
            id = self.actualToken.att
            if self.equipara("id") and self.equipara("parCerrado") and self.equipara("puntoComa"):
                tipo = None
                if self.TSActual.buscarId(id):
                    tipo = self.TSActual.map[id].tipo
                elif self.TSG.buscarId(id):
                    tipo = self.TSG.map[id].tipo
                if tipo not in {"int", "string"}:
                    self.error("TypeError", f"Variable a es de tipo {tipo}, input() debe recibir una variable de "
                                            f"tipo string o entero")
                if not tipo:
                    self.TSG.insertarId(id, "int")
                else:
                    return ProductionObject(tipo=True)

        else:
            self.equierror(First["S"])

    def Sp(self) -> ProductionObject:
        if self.equipara("asig", 15):
            E = self.E()
            if not E:
                self.error("EmptyConditionError", "La condición está vacía")
            if self.equipara("puntoComa"):
                return E
        elif self.equipara("parAbierto", 16):
            L = self.L()
            if self.equipara("parCerrado") and self.equipara("puntoComa"):
                if L: return ProductionObject(tipo=L.tipo)
        elif self.equipara("postIncrem", 17) and self.equipara("puntoComa"):
            return ProductionObject(tipo="postIncrem")
        else:
            self.equierror(First["Sp"])

    def X(self) -> ProductionObject:
        if self.token in First['E']:
            Syntactic.addParseElement(18)
            return self.E()
        elif self.token in Follow['X']:
            Syntactic.addParseElement(19)
            return ProductionObject(tipo=True)
        else:
            self.error("SentenceNotTerminatedError",
                       f"Esperaba ';' al terminar la sentencia, después de un return vacío")

    def C(self) -> None:
        if self.token in First["B"]:
            Syntactic.addParseElement(20)
            if self.token != "eof":
                self.B()
                self.C()
        elif self.token in Follow['C']:
            Syntactic.addParseElement(21)

    def L(self) -> ProductionObject:
        if self.token in First["E"]:
            Syntactic.addParseElement(22)
            E = self.E()
            if E:
                return ProductionObject(tipo=self.Q([E.tipo]))
            return ProductionObject(tipo=[])
        elif self.token in Follow['L']:
            Syntactic.addParseElement(23)
        else:
            self.error("FunctionCallError", "No se ha cerrado paréntesis en la llamada a la función")

    def Q(self, lista=None) -> List[str]:
        if self.equipara("coma", 24):
            Q = lista if lista else []
            E = self.E()
            if E:
                Q.append(E.tipo)
                return self.Q(lista)
        elif self.token in Follow['Q']:
            Syntactic.addParseElement(25)
            return lista if lista else None
        self.equierror(First["Q"])

    def F(self) -> ProductionObject:
        if self.equipara("function", 26):
            id = self.actualToken.att
            if self.equipara("id"):
                tipo_ret = self.H().tipo
                self.TSActual = TS(id)  # tabla de funcion
                self.TSLIST.append(self.TSActual)
                if self.equipara("parAbierto"):
                    A = self.A()
                    if A:
                        tipo_params = A.tipo
                    else:
                        tipo_params = ""
                    if self.equipara("parCerrado") and self.equipara("llaveAbierto"):
                        self.TSG.insertarId(id, "funcion", tipo_params, len(tipo_params), tipo_ret)
                        self.C()
                        if self.equipara("llaveCerrado"):
                            # insertar funcion en TSG de una
                            self.TSActual = self.TSG  # ~= destruir tabla de la funcion
                            return ProductionObject(tipo=True)
        else:
            self.equierror(First["F"])

    def H(self) -> ProductionObject:
        if self.token in First['T']:
            Syntactic.addParseElement(27)
            T = self.T()
            return ProductionObject(tipo=T.tipo)
        elif self.token in Follow['H']:
            Syntactic.addParseElement(28)
            return ProductionObject(tipo="")
        else:
            self.error("TypeError",
                       f"Tipo de función no aceptado. Debe usar {First['T']} o \"\" (no poner nada para void)")

    def A(self) -> ProductionObject:
        if self.token in First['T']:
            Syntactic.addParseElement(29)
            T = self.T()
            id = self.actualToken.att
            if self.equipara("id"):
                K = self.K([T.tipo])
                self.TSActual.insertarId(id, T.tipo)
                if K:
                    return ProductionObject(tipo=K)
        elif self.token in Follow['A']:
            Syntactic.addParseElement(30)
        else:
            self.error("FunctionCallError", f"No ha cerrado paréntesis en la llamada a la función")

    def K(self, lista=None) -> List[str]:
        if self.equipara("coma", 31):
            K = lista if lista else []
            T = self.T()
            K.append(T.tipo)
            id = self.actualToken.att
            if self.equipara("id"):
                self.TSActual.insertarId(id, T.tipo)
                return self.K(lista)
        elif self.token in Follow['K']:
            Syntactic.addParseElement(32)
            return lista if lista else None
        else:
            self.error("ArgumentDeclarationError",
                       "Los argumentos de las funciones deben estar separados por \',\'")

    def E(self) -> ProductionObject:
        if self.token in First["N"]:
            Syntactic.addParseElement(33)
            N = self.N()  # primer argumento
            return self.O1(N)

    def N(self) -> ProductionObject:
        if self.token in First["Z"]:
            Syntactic.addParseElement(34)
            Z = self.Z()
            # si llega aqui no ha habido errores entonces devolvemos el tipo que espera O2 por si ha llamado a Z
            return self.O2(Z)

    def Z(self) -> ProductionObject:
        if self.token in First["R"]:
            Syntactic.addParseElement(35)
            R = self.R()
            # si llega aqui no ha habido errores entonces devolvemos el tipo que espera O3 por si ha llamado a R
            return self.O3(R)

    def O1(self, prev=None) -> ProductionObject:
        if self.equipara("or", 36):
            N = self.N()
            if N.tipo != "boolean":
                self.error("WrongDataTypeError", f"Operador || solo acepta datos lógicos, tipo dado {N.tipo}")
            return self.O1()
        elif self.equipara("and", 37):
            N = self.N()
            if N.tipo != "boolean":
                self.error("OperandTypeError", f"Operador && solo acepta datos lógicos, tipo dado {N.tipo}")
            return self.O1()
        elif self.token in Follow['O1']:
            Syntactic.addParseElement(38)
            if prev:
                return prev
            return ProductionObject(tipo="boolean")
        else:
            self.error("NonSupportedOperationError", f"Esperaba uno de los siguientes símbolos{Follow['O1']}")

    def O2(self, prev=None) -> ProductionObject:
        if self.equipara("equals", 39):
            Z = self.Z()
            if Z.tipo != "int":
                self.error("OperandTypeError", f"Operador == solo acepta datos de tipo entero, tipo dado {Z.tipo}")
            return self.O2()
        elif self.equipara("mayor", 40):
            Z = self.Z()
            if Z.tipo != "int":
                self.error("OperandTypeError", f"Operador > solo acepta datos de tipo entero, tipo dado {Z.tipo}")
            return self.O2()
        elif self.token in Follow['O2']:
            Syntactic.addParseElement(41)
            if prev:
                return prev
            return ProductionObject(tipo="boolean")
        else:
            self.error("NonSupportedOperationError", f"Esperaba uno de los siguientes símbolos{Follow['O2']}")

    def O3(self, prev=None) -> ProductionObject:
        if self.equipara("mas", 42):
            R = self.R()
            if R.tipo != "int":
                self.error("OperandTypeError", f"Operador + solo acepta datos enteros, tipo dado {R.tipo}")
            else:
                return self.O3()
        elif self.equipara("por", 43):
            R = self.R()
            if R.tipo != "int":
                self.error("OperandTypeError", f"Operador * solo acepta datos enteros, tipo dado {R.tipo}")
            return self.O3()
        elif self.token in Follow['O3']:
            Syntactic.addParseElement(44)
            if prev:
                return prev
            return ProductionObject(tipo="int")
        else:
            self.error("NonSupportedOperationError", f"Esperaba uno de los siguientes símbolos{Follow['O3']}")

    def R(self) -> ProductionObject:
        id = self.actualToken.att
        if self.equipara("id", 45):
            Rp = self.Rp()
            if Rp:  # es una llamada a una funcion o post incremento
                if Rp.tipo == "postIncrem":
                    if not self.TSG.buscarId(id) and not self.TSActual.buscarId(id) :
                        self.error("NonDeclaredError", f"Error la variable {id} no ha sido declarada previamente")
                    try:
                        ident = self.TSActual.map[id]
                    except KeyError:
                        ident = self.TSG.map[id]
                    if ident.tipo != "int":
                        self.error("OperandTypeError",
                               "El operador post incremento solo es aplicable a variables del tipo entero")
                elif not self.TSG.buscarId(id):
                    self.error("NonDeclaredError", f"Error la función {id} no ha sido declarada previamente")
                elif Rp.tipo != "true" and Rp.tipo != self.TSG.map[id].tipo_params:
                    self.error("WrongArguemensError", f"Tipos de los atributos incorrectos en llamada a función \"{id}\" ")
                else:
                    return ProductionObject(tipo=self.TSG.map[id].tipo_dev)
            else:
                if self.TSActual.buscarId(id):
                    return ProductionObject(tipo=self.TSActual.map[id].tipo)
                if self.TSG.buscarId(id):
                    return ProductionObject(tipo=self.TSG.map[id].tipo)
                else:
                    self.error("NonDeclaredError", f"Error la variable {id} no ha sido declarada previamente")
        if self.equipara("parAbierto", 46):
            E = self.E()
            if self.equipara("parCerrado"):
                return ProductionObject(tipo=E.tipo)
        elif self.equipara("cteEnt", 47):
            return ProductionObject(tipo="int", ancho=1)
        elif self.equipara("cadena", 48):
            return ProductionObject(tipo="string", ancho=1)
        elif self.equipara("true", 49):
            return ProductionObject(tipo="boolean", ancho=1)
        elif self.equipara("false", 50):
            return ProductionObject(tipo="boolean", ancho=1)

    def Rp(self) -> ProductionObject:
        if self.equipara("parAbierto", 51):
            L = self.L()
            if self.equipara("parCerrado"):
                if L:
                    return ProductionObject(tipo=L.tipo)
                else:
                     return ProductionObject(tipo="true")
        elif self.equipara("postIncrem", 52):
            return ProductionObject(tipo="postIncrem")
        elif self.token in Follow["Rp"]:
            Syntactic.addParseElement(53)

    def writeTS(self):
        for ts in self.TSLIST:
            TSFILE.write(str(ts))


def createSyntactic():
    """Creates the Syntactic parser"""
    global SYNTACTIC
    SYNTACTIC = Syntactic()
    SYNTACTIC.start()


if __name__ == "__main__":
    createProcessor()
    createLexer()
    createSyntactic()

    # while True:
    #     token = LEXER.tokenize()
    #     if token is not None and token.code == "eof":
    #         break
    close_all_files()  # closes all file descriptors
