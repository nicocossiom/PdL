from lexer import Lexer

def main():
    lexer = Lexer()
    lexer.tokenize()
    lexer.printToken()

if __name__ == '__main__':
    main()