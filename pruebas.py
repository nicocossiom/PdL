from errorHandler import ErrorHandler
from lexer import Lexer
from tablaSimbolos import TS
from errorHandler import ErrorHandler
lexer = Lexer()
lexer.tokenize()
lexer.printToken()
ts = TS(lexer)
ts.printTS()
errorHandler = ErrorHandler(lexer)
errorHandler.errorPrinter()
