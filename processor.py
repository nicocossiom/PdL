'''
This file will contain all parts of the lenguage processor from 
which its services will be launched to perform their tasks
'''
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
