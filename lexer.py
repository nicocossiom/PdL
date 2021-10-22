from transitions import Machine
DELIMITERS = " \n\t"
DIGITS = "123456789"
LETTERS = "abcdefghijlmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
SYMBOLS = ["+","*","&","=",">", "," ,";", "(",")","{","}", ""]
TOKEN_CODES = ["mas", "por", "and", "asig", "mayor", "coma", "puntoComa", "parAbierto", "parCerrado", "llaveAbierto", "llaveAbierto", "eof"]
PTR = [ "let","function","rn","else","input","print","while","do","true","false","int","boolean","string"]
STATES = list(range(25))
class Lexer:
    def __init__(self, file:str):
        '''
        Initializes state macine at state 0
        '''
        self.machine = Machine(model=self, states = STATES, intial=0)
        self.state = 0 #initial state
        
    def action(self, state:int, car:str) -> int:
        '''
        Returns action to be taken in a certain state
        state: (int) describes current state
        car: (str) describes current char in buffereturns next state to whill will be transitioned to 
        '''


    def next(self, state:int, car:str) -> int:
        '''
        Returns next state to which will be transitioned to
        state: (int) describes current state
        car: (str) describes current char in buffereturns next state to whill will be transitioned to 
        '''

    def error(self, type:int):
        '''
        Returns error type detected
        state: (int) describes current state
        car: (str) describes current char in buffereturns next state to whill will be transitioned to 
        '''



             
