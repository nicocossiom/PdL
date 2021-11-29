import sys
import os
import errno
import processorComponents
from processorComponents.JS_PdL import Lexer, Syntactic
# import processorComponents.resources
from processorComponents.tablaSimbolos import TS
OUTPUTDIR = ""

def run(file) -> None:
    '''
    1) Lexical analyzer -> creates token and error list 
    2) Syntactical analyzer -> creates parse and error list
    3) Symbol table -> inserts tokens and values
    4) Displays errors 
    '''
    lexer = Lexer(file).tokenize()
    lexer.printTokens()
    ts = TS(lexer.tokenList)
    ts.printTS()
    syntactic = Syntactic(lexer.tokenList)
    syntactic.P()
    syntactic.exportParse()

'''
This file will contain all parts of the lenguage processor from 
which its services will be launched to perform their tasks
'''
if len(sys.argv) == 1:
    f = open("./casosPruebas/correcto2.txt", "r") 
    sys.exit("JS_PdL usage: must input total path to file to be processed as argument: \n \
        Example: File to be processed in ~/Documents/file --> \n\t \
        $./JS_PdL.py ~/Documents/fileToBeProcessed")
if len(sys.argv) > 3:
    sys.exit("Input file path to analyze as program argument")
# manual path specification for debugging puropses
# file that the lexer will generate tokens for
elif os.path.exists(sys.argv[1]):
    f = open(sys.argv[1], "r")
    OUTPUTDIR = os.getcwd() + "/JS-PdL-Output/"+f.name.replace(".txt", "")
    try:
        os.makedirs(OUTPUTDIR)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    print(f"Directorio de volcado del programa creado en: {OUTPUTDIR}")
    run(f)

else:
    sys.exit(f"File \'{sys.argv[1]}\' does not exist")
