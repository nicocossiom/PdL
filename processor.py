'''
This file will contain all parts of the lenguage processor from 
which its services will be launched to perform their tasks
'''
from errorHandler import ErrorHandler
from lexer import Lexer
from tablaSimbolos import TS
from errorHandler import ErrorHandler
from syntactic import Syntactic
lexer = Lexer()
lexer.tokenize()
lexer.printTokens()
ts = TS(lexer)
ts.printTS()
syntactic = Syntactic(lexer)
syntactic.P()
syntactic.exportParse()
errorHandler = ErrorHandler(lexer, syntactic)
errorHandler.errorPrinter()
