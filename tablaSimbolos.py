from lexer import Lexer
class TS():
    def __init__(self, lexer: Lexer):     
        self.lexer = lexer
    def printTS(self):
        with open(self.lexer.outputdir+"/ts.txt", "w") as f:
            f.write(("TS GLOBAL #1"))
            for token in self.lexer.tokenList:
                if token.code == "id": f.write(f"\n*Lexema: '{token.att}'")
                else: f.write(f"\n*Lexema: '{token.code}'")
