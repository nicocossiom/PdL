# Lenguage definitions by class
RES_WORD = ["let", "function", "rn", "else", "input", "print",
            "while", "do", "true", "false", "int", "boolean", "string", "return"]
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

FIRST = {
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