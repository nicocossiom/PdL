First = {
    'P': ["let", "if", "while", "do", "function", "eof"], 
    'B': ["let", "if", "while", "do"],
    "O" : "else",
    "T" : ["int", "boolean", "string"],
    "S" : ["id", "return", "print", "input" ],             
    "Sp": ["asig", "parAbierto", "postIncrem", "asig" ],
    "X" : [ "id", "parAbierto", "entero", "cadena", "true", "false"],
    "C" : ["let", "if", "while", "do"],
    "L" : ["id", "parAbierto", "entero", "cadena", "true", "false" ],
    "Q" : "coma" ,
    "F" : "function" ,
    "H" : [ "int", "boolean", "string" ],
    "A" : [ "int", "boolean", "string" ],
    "K" : "coma",
    "E" : ["id", "parAbierto", "entero", "cadena", "true", "false"],
    "Ep": [ "and", "mayor"],
    "Epp": [ "id", "parAbierto", "entero", "cadena", "true", "false"],
    "R" : ["id", "parAbierto", "entero", "cadena", "true", "false"],
    "Rp": "mayor",
    "U" : [ "id", "parAbierto", "entero", "cadena", "true", "false"],
    "Up": [ "mas", "por"],
    "V" : ["id", "parAbierto", "entero", "cadena", "true", "false"],
    "Vp": "parAbierto"
}
import errorHandler, lexer, syntactic, tablaSimbolos

class Syntactic: 
    
    class error(Error):
        def __init__(self, num, linea):
            super().__init__(num, linea)
            
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.tokenList = lexer.tokenList 
        self.index = 0 # indice que apunta al elemento actual de la lista de tokens
        self.token = self.tokenList[self.index].code
        self.reglas = []
        self.outputdir = lexer.outputdir
        self.errorList = []
    
    def next(self) -> Token:
        self.index+=1
        self.token = self.tokenList[self.index].code
        return self.token
    
    def equipara(self, code: String, regla=None) -> Boolean:
        self.reglas.append(regla)
        if equipara(code):
            self.next()
            return True
        self.errorList.append(error(8, self.token.line))                     

    def exportParse(self) -> None:
        '''Creates a directory (specified in self.ouput dir which will contain all the output of the processor.\n
        Writes all tokens with the appropiate format to the file "tokens.txt" after tokenize() has been used'''
        try: 
            os.mkdir(self.outputdir)
        except OSError: 
            print(f"Error al crear carpeta de volcado en: {self.outputdir}")
        except FileExistsError:
            print(f"Directorio de volcado del programa creado en: {self.outputdir}") 
        with open(self.outputdir+"/tokens.txt", "w") as f:
            f.write("Descendente ")
            # for regla in self.reglas: f.write(f"{regla}")
            [f.write(regla) for regla in self.reglas]

    def P(self) -> None:
        if(self.index>0): self.next()
        # First(B)
        if (self.token) in First[B]:
            self.reglas.append(1)
            B()
            P()
        elif (self.token) in First[F]: 
            self.reglas.append(2)
            F() 
            P()
        elif (equipara("eof")): 
            self.reglas.append(3)
            return

    def B(self) -> None:
        if equipara("let", 4):
            T()
            if equipara("id"):
                if equipara("puntoComa"): return 
        elif (equipara("if") and equipara("parAbierto")): 
                E()
                if equipara("parCerrado") and equipara("llaveAbierto"):
                        S()
                        if(equipara("llaveCerrado")):
                            O()
                            return                     
        elif(self.token in First[S]):
            self.reglas.append(6)
            S()
        elif equipara("while", 7):
            if equipara("parAbierto"):
                E()
                if (equipara("parCerrado")):
                    if equipara("llaveAbierto"):
                        C()
                        if equipara("llaveCerrado"): return
        elif equipara("do", 8):
            if equipara("llaveAbierto"):
                S()
                if equipara("llaveCerrado"):
                    if equipara("while"):
                        if equipara("parAbierto"):
                            E()
                            if equipara("parCerrado") and equipara("puntoComa"): return
        return 
            
    def O(self) -> None:
        if equipara("else", 9):
            if equipara("parAbierto"): 
                T()
                if equipara("parCerrado"): return
        else:
            self.reglas.append(10)
            return 
    
    def T(self) -> None:
        if(equipara("entero", 11)):
            return
        elif(equipara("boolean", 12)):
            return
        elif(equipara("cadena", 13)):
            return

    def S(self) -> None:
        if(equipara("id", 14)): 
            Sp()
        elif(equipara("return", 15)):
            X()
            if(equipara("puntoComa")): return
        elif equipara("print", 16): 
            if (equipara('parAbierto')):
                E()
                if equipara("parCerrado") and equipara("puntoComa"): return 
        elif(equipara("input", 17) and equipara("parAbierto") and equipara("id") and equipara("parCerrado") and equipara("puntoComa")):
            return
        
    def Sp(self) -> None:
        if equipara("asig", 18):
            E()
            if equipara("puntoComa"):
                return
        elif (equipara("parAbierto", 19)):
            L()
            if equipara("parCerrado"): return
        elif equipara("postIncrem", 20): return
        elif equipara("equals", 21):
            E()

            
    def X(self) -> None:
        if self.next() in First['E']: 
            self.reglas.append(22)
            E()
        else: self.reglas.append(23)
        return

    def C(self) -> None: 
        if self.next() in First["B"]:
            self.reglas.append(24)
            B()
            C()
        else: self.reglas.append(25)
        return
    
    def L(self) -> None:
        if self.next() in First["E"]:
            self.reglas.append(26)
            Q()
        else: self.reglas.append(27)
        return 

    def Q(self) -> None:
        if equipara("coma", 28):
            E()
            Q()
        else: self.reglas.append(29)
        return
    
    def F(self) -> None:
        if equipara("function", 30) and equipara("id") and self.next() in First["H"]:
            H()
            if equipara("parAbierto"): 
                A()
                if equipara("parCerrado") and equipara("llaveAbierto"):
                    C()
                    if equipara("llaveCerrado"): return
                  
    
    def H(self) -> None:
        if self.next() in First['T']:
            self.reglas.append(31)
            T()
        else: self.reglas.append(32)
        return
    
    def A(self) -> None:
        if self.next() in First['T']: 
            self.reglas.append(33)
            T()
            if equipara("id"):
                K()
        else: self.reglas.append(34)
        return
        
    def K(self) -> None:
        if equipara("coma", 35):
            T()
            if equipara("id"):
                K()
        else: self.reglas.append(36)
        return

    def E(self) -> None:
        if self.next() in First["R"]:
            self.reglas.append(37)
            R()
            Ep()

    def Ep(self) -> None: 
        if equipara("and", 38) :  
            Epp()
        elif equipara(">", 39):
            Epp()
        else: self.reglas.append(40)
        return 
            
    def Epp(self) -> None:
        if self.next() in First["R"]:
            self.reglas.append(41)
            R()
            Ep()
        return

    def R(self) -> None:
        if self.next() in First['U']:
            self.reglas.append(42)
            U()
            Rp()
        return

    def Rp(self) -> None:
        if (self .next() == ">"):
            self.reglas.append(43)
            U()
            Rp()
        else: self.reglas.append(44)
        return
        
    def U(self) -> None:
        if self.next() in First["V"]:
            self.reglas.append(45)
            V()
            Up()
        return
        
    def Up(self) -> None:
        if equipara("mas", 46):
            U()
        elif equipara("*", 47):
            U()
        else: self.reglas.append(48)
        return

    def V(self) -> None:
        if equipara("id", 49):
            Vp()
        elif equipara("parAbierto", 50):
            E()
            if equipara("parCerrado"): return
        elif(equipara("cteEnt", 51)): return
        elif(equipara("cadena", 52)): return
        elif(equipara("true", 53)): return
        elif(equipara("false", 54)): return

    def Vp(self) -> None:
        if (equipara("parAbierto", 55)): 
            L()
            if equipara("parCerrado"): return
        else: self.reglas.append(56)
        return