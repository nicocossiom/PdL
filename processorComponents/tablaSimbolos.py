from typing import List
from ordered_set import OrderedSet
from processorComponents.JS_PdL import Token

class TS():
    def __init__(self, tokenList: List[Token], outputdir):
        self.tokenList = tokenList
        self.outputdir = outputdir
    def setIds(self):
        setTokenList = OrderedSet()
        for token in self.lexer.tokenList:
            if token.code == "id": setTokenList.add(token.att)
        return setTokenList 

    def printTS(self):
        '''Outputs containing Symbol Table with correct format to 'ts.txt' in directory specified in $lexer.outputdir'''
        with open(self.outputdir+"/ts.txt", "w") as f:
            f.write(("TS GLOBAL #1"))
            for lexId in self.setIds():
                f.write(f"\n*Lexema: '{lexId}'")
