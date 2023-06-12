import sys 
import re 

turno = 0

LIST_TERM = ['*','/', '&&']
LIST_EXP = ['+','-','||', "."]
LIST_PAREN = ['(',')']
LIST_ASSIGN = ['=']
LIST_REL = ['<','>','==']

LIST_RESERVED_WORDS = ['println', 'if', 'else', 'while', 'for', 'int', 'float', 'char', 'string', 
                       'bool', 'true', 'false', 'return', 'break', 'continue', 'and', 'or', 'not']

class Node:
    
    def __init__(self, value):
        self.value = value
        self.children = []
        
    def evaluate(self, symboltable):
        pass            
    

class BinOp(Node):
    
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symboltable):
        direita = self.children[0].evaluate(symboltable)
        
        esquerda = self.children[1].evaluate(symboltable)
        
        if self.value == "+":
            if direita[0] == "ITEM" and esquerda[0] == "HP":
                item = self.children[0].value
                receiver = self.children[1].value.split("_")[0]
                print("trainer utilizou " + item)
                print(receiver + " recuperou " + str(direita[1]) + " de HP")
                return ["HP", direita[1] + esquerda[1]]
        
        if self.value == "-":
            if direita[0] == "ATAQUE" and esquerda[0] == "HP":
                #printa que o receiver perdeu x de vida
                attacker = self.children[0].value.split("_")[0]
                receiver = self.children[1].value.split("_")[0]
                print(attacker + " atacou " + receiver)
                print(receiver + " perdeu " + str(direita[1]) + " de HP")        
                if (esquerda[1] - direita[1]) < 0:
                    return ["HP", 0]
                return ["HP", esquerda[1] - direita[1]]
        
        if self.value == "*":
            if direita[0] == "ATAQUE" and esquerda[0] == "Int":
                attacker = self.children[0].value.split("_")[0]
                print(attacker + " obteve BOOST de " + str(esquerda[1]) + " vezes")
                return ["ATAQUE", direita[1] * esquerda[1]]
        if self.value == "==":
            if direita[1] == esquerda[1]:
                return ["Int", 1]
            return ["Int", 0]
                #return ["Int", direita[1] == esquerda[1]]
        if self.value == "<":
            #if direita[0] == "Int" and esquerda[0] == "Int":
            if direita[1] < esquerda[1]:
                return ["Int", 1]
            return ["Int", 0]
                #return ["Int", direita[1] < esquerda[1]]
        if self.value == ">":
            #if direita[0] == "Int" and esquerda[0] == "Int":
            if direita[1] > esquerda[1]:
                return ["Int", 1]
            return ["Int", 0]

class IntVal(Node):
    
    def __init__(self, value):
        self.value = value
    
    def evaluate(self, symboltable):
        return ["Int", int(self.value)]
    
class StringVal(Node):
    
    def __init__(self, value):
        self.value = value
    
    def evaluate(self, symboltable):
        return ["String", str(self.value)]

class HPVal(Node):
    
    def __init__(self, value):
        self.value = value
    
    def evaluate(self, symboltable):
        return ["HP", int(self.value)]

class AtaqueVal(Node):
    
    def __init__(self, value):
        self.value = value
    
    def evaluate(self, symboltable):
        return ["ATAQUE", int(self.value)]
    
class ItemVal(Node):
    
    def __init__(self, value):
        self.value = value
    
    def evaluate(self, symboltable):
        return ["ITEM", int(self.value)]
    
class NoOp(Node):
    
    def __init__(self):
        pass
    
    def evaluate(self, symboltable):
        pass

class Identifier(Node):
    
    def __init__(self, value):
        self.value = value
    
    def evaluate(self, symboltable):
        return symboltable.getter(self.value)
    
class FuncTable:
     
    table = {}
                
    def getter(key):
        #verificar se a chave existe, senão, erro
        if key in FuncTable.table:
            return FuncTable.table[key]
        
        sys.stderr.write('ERROR: KEY NOT DECLARED')
        sys.exit(1)
        
    def setter(key, value):
        #printa o key e value
        
        #verificar se a o value[0] guardado tem o mesmo tipo do novo value a ser guardado, senao, erro
        if key in FuncTable.table:
            if FuncTable.table[key][0] != value[0]:
                sys.stderr.write('ERROR: VALUE TYPE NOT MATCHING')
                sys.exit(1)
                
            FuncTable.table[key] = value
            return

        sys.stderr.write('ERROR: KEY NOT DECLARED')
        sys.exit(1)
    
    def create(key, value):  
        #verificar se a chave existe, senão, erro
        if key in FuncTable.table:
            sys.stderr.write('ERROR: KEY ALREADY EXISTS')
            sys.exit(1)
            
        FuncTable.table[key] = value 
        
class SymbolTable:
     
    def __init__(self):
        self.table = {}
                
    def getter(self, key):
        #verificar se a chave existe, senão, erro
        if key in self.table:
            return self.table[key]
        
        sys.stderr.write('ERROR: KEY NOT DECLARED')
        sys.exit(1)
        
    def setter(self, key, value):
        #printa o key e value
        #verificar se a o value[0] guardado tem o mesmo tipo do novo value a ser guardado, senao, erro
        if key in self.table:
            if self.table[key][0] != value[0]:
                sys.stderr.write('ERROR: VALUE TYPE NOT MATCHING')
                sys.exit(1)
                
            self.table[key] = value
            return

        sys.stderr.write('ERROR: KEY NOT DECLARED')
        sys.exit(1)
        
    def create(self, key, value):
        
        #verificar se a chave existe, senão, erro
        if key in self.table:
            sys.stderr.write('ERROR: KEY ALREADY EXISTS')
            sys.exit(1)
            
        self.table[key] = value 
               
        
        
class Assignment(Node):
    
    def __init__(self, value, children):
        
        self.value = value
        self.children = children
    
    def evaluate(self, symboltable):
        result = self.children[0].evaluate(symboltable)
        symboltable.setter(self.value, result)

class VarDec(Node):
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def evaluate(self, symboltable):
        if len(self.children) == 1:
            if self.value == "Int":
                symboltable.create(self.children[0], [self.value, 0])  
            elif self.value == "HP":
                symboltable.create(self.children[0], [self.value, 0])
            elif self.value == "ATAQUE":
                symboltable.create(self.children[0], [self.value, 0])
            elif self.value == "ITEM":
                symboltable.create(self.children[0], [self.value, 0])
            elif self.value == "String":
                symboltable.create(self.children[0], [self.value, ""]) 
        elif len(self.children) == 2:
            #value = self.children[1].evaluate(symboltable)[0]
            if self.value == "Int" and self.children[1].evaluate(symboltable)[0] == "Int":
                value = self.children[1].evaluate(symboltable)[1]
                symboltable.create(self.children[0], [self.value, value])   
            if self.value == "HP" and self.children[1].evaluate(symboltable)[0] == "Int":
                value = self.children[1].evaluate(symboltable)[1]
                symboltable.create(self.children[0], [self.value, value]) 
            if self.value == "ATAQUE" and self.children[1].evaluate(symboltable)[0] == "Int":
                value = self.children[1].evaluate(symboltable)[1]
                symboltable.create(self.children[0], [self.value, value]) 
            if self.value == "ITEM" and self.children[1].evaluate(symboltable)[0] == "Int":
                value = self.children[1].evaluate(symboltable)[1]
                symboltable.create(self.children[0], [self.value, value])         
            if self.value == "String" and self.children[1].evaluate(symboltable)[0] == "String":
                symboltable.create(self.children[0], [self.value, self.children[1].evaluate(symboltable)[1]])
                
class FuncDec(Node):
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def evaluate(self, symboltable):
        FuncTable.create(self.children[0], self)
    

class FuncCall(Node):
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def evaluate(self, symboltable):
        node_func = FuncTable.getter(self.value)
        local_sb = SymbolTable()
        
        identifier, args, block = node_func.children
        
        if len(args) != len(self.children) and self.children[0] != None:
            sys.stderr.write('ERROR: NUMBER OF ARGUMENTS NOT MATCHING')
            sys.exit(1)
            
        for var, arg in zip(args, self.children):
            var.evaluate(local_sb)
            #valor = 
            local_sb.setter(var.children[0], arg.evaluate(symboltable))
        
        val = block.evaluate(local_sb)
        
        return val
            
class Read(Node):
    
    def __init__(self):
        pass
        
    def evaluate(self, symboltable):
        return ["Int", int(input())]
    
class Block(Node):
    
    def __init__(self, children):
        self.children = children

    def evaluate(self, symboltable):
        for child in self.children:
            #vai quebrar quando achar um return aqui
            if type(child) == Return:
                return child.evaluate(symboltable)    
            child.evaluate(symboltable)
        
        #percorre a simymboltableboltable e printa os valores
        for key in symboltable.table:
            list_values = symboltable.table[key]
            if list_values[0] == "HP" and list_values[1] <= 0:
                name = key.split("_")[0]
                print(name + " desmaiou!")
                
        

class While(Node):
    
    def __init__(self, children):
        self.children = children
    
    def evaluate(self, symboltable):
        print("pokebattle iniciada!")
        while self.children[0].evaluate(symboltable)[1]:
            self.children[1].evaluate(symboltable)
            
class If(Node):
    
    def __init__(self, children):
        self.children = children
    
    def evaluate(self, symboltable):
        #print(self.children[0].evaluate(symboltable)[1])
        if self.children[0].evaluate(symboltable)[1]:
            self.children[1].evaluate(symboltable)
        else:
            if len(self.children) == 3:
                #basicamente verifica se tem um else, o if não obrigatoriamente vai ser verdade
                self.children[2].evaluate(symboltable)

class Return(Node):
        
    def __init__(self, children):
        self.children = children
    
    def evaluate(self, symboltable):
        return self.children.evaluate(symboltable)

class Print(Node):
        def __init__(self, children):
            self.children = children
        
        def evaluate(self, symboltable):
            pt1 = self.children[0].evaluate(symboltable)
            print(pt1[1])    
class Token:
    
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
            
    def __init__(self, source, position):
        self.source = source
        self.position = position 
        
    def selectNext(self):
        while (self.position < len(self.source)) and self.source[self.position] == " ": # se for espaço só pula
            self.position = self.position + 1

        if self.position == len(self.source):
            self.next = Token("EOF", None)

        elif self.source[self.position].isdigit():
            value = ""
            while (self.position < len(self.source)) and (self.source[self.position].isdigit()): # se for digito vai concatenando
                value = value + self.source[self.position]
                self.position = self.position + 1

            self.next = Token("NUMBER", value)
            return 

        elif self.source[self.position] == '*': # se for mult
            self.next =  Token("OPERATOR", "*")
            self.position = self.position + 1
            return
        
        elif self.source[self.position] == ',':
            self.next = Token("AND_ARG", ",")
            self.position = self.position + 1
            return    
            
        elif self.source[self.position] == '(': # se for abrir par
            self.next = Token("OPERATOR", "(")
            self.position = self.position + 1
            return

        elif self.source[self.position] == ')': # se for fechar par
            self.next = Token("OPERATOR", ")")
            self.position = self.position + 1
            return
        
        elif self.source[self.position] == '=': # se for igual
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.next = Token("OPERATOR", "==")
                self.position = self.position + 2
                
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '>':
                self.next = Token("OPERATOR", "=>")
                self.position = self.position + 2
            else:
                self.next = Token("OPERATOR", "=")
                self.position = self.position + 1
            
            return
        
        elif self.source[self.position] == '>':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '>':
                self.next = Token("OPERATOR", ">>")
                self.position = self.position + 2
                return
            else:
                self.next = Token("OPERATOR", ">")
                self.position = self.position + 1
            
            return

        elif self.source[self.position] == '\n': # se for quebra de linha
            self.next = Token("QUEBRA_LINHA", "\n")
            self.position = self.position + 1
        
        elif self.source[self.position] == '"': # se for string, vai concatenando até achar o fechamento
            self.position = self.position + 1
            value = ""
            
            while self.position < len(self.source) and self.source[self.position] != '"':
                value = value + self.source[self.position]
                self.position = self.position + 1
            
            #lembrete: colocar um std error :) 
            
            #para consumir o fechamento (") 
            self.position = self.position + 1
            self.next = Token("STRING", value)
            return 
            

        elif self.source[self.position].isalpha():

            value = "" #se for palavra vai concatenando, precisa checar se chegou no final
            while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == "_"): 
                value = value + self.source[self.position]
                self.position = self.position + 1

            if value == "BATALHA": 
                self.next = Token("WHILE", value)  
                return 
            
            if value == "RECUPERAR":
                self.next = Token("OPERATOR", "+")
                return
        
            if value == "ATACAR":
                self.next = Token("OPERATOR", "-")
                return
            
            if value == "IGUAL":
                self.next = Token("OPERATOR", "=")
                return
            
            if value == "EXATO":
                self.next = Token("OPERATOR", "==")
                return
            
            if value == "MAIOR":
                self.next = Token("GREATER", ">")
                return
            
            if value == "MENOR":
                self.next = Token("LESS", "<")
                return
                      
            elif value == "SE":
               self.next = Token("IF", "if")
               return
            
            elif value == "println":
                self.next = Token("PRINTLN", value) 
                return       
        
            elif value == "FIM_TATICA":
                self.next = Token("END", "end")
                return
            
            elif value == "Int":
                self.next = Token("TYPE", value)
                return 
            
            elif value == "HP":
                self.next = Token("TYPE", "HP")
                return 
            
            elif value == "ATAQUE":
                self.next = Token("TYPE", "ATAQUE")
                return 
        
            elif value == "ITEM":
                self.next = Token("TYPE", "ITEM")
                return 
            
            elif value == "TIPO":
                self.next = Token("TYPE", "String")
                return 
            
            elif value == "String":
                self.next = Token("TYPE", value)
                return

            elif value == "ESTRATEGIA":
                self.next = Token("FUNCTION", "function")
                return
    
            elif value == "RESULTADO":
                self.next = Token("RETURN", "return")
                return

            else:
                self.next = Token("IDENTIFIER", value)
                return
        else:
            sys.stderr.write("Caractere inválido: {}.".format(self.source[self.position]))
            sys.exit(1)
        
class Parse:
    
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        
    @staticmethod
    def parseFactor(tokenizer):
        if tokenizer.next.type == 'NUMBER':
            resultado = int(tokenizer.next.value)
            tokenizer.selectNext()
            intval = IntVal(resultado)
            return intval
        
        if tokenizer.next.type == 'IDENTIFIER':
            
            name = tokenizer.next.value
            tokenizer.selectNext()
            
            if (tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == '('):
                tokenizer.selectNext()
                
                filhos = []
                
                #o erro tá aqui
                while tokenizer.next.value == ',' or len(filhos) == 0:
                    if tokenizer.next.value == ",":
                        tokenizer.selectNext()
                    
                    expression = Parse.ParseRelExpression(tokenizer)
                    filhos.append(expression)
                
                if (tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == ')'):
                    tokenizer.selectNext()
                    
                    call = FuncCall(name, filhos)
                    return call
            
                else:
                    sys.stderr.write('ERROR: PARENTHESIS NOT CLOSED')
                    sys.exit(1)
            
            else:
                identi = Identifier(name)
                return identi
        
        if tokenizer.next.type == 'STRING':
            name = tokenizer.next.value
            tokenizer.selectNext()
            stringVal = StringVal(name)
            return stringVal
        
        if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == '(':
            tokenizer.selectNext()
            resultado = Parse.ParseRelExpression(tokenizer)
            
            if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == ')':
                tokenizer.selectNext()
                return resultado
            else:
                sys.stderr.write('ERROR: PARENTHESIS NOT CLOSED')
                sys.exit(1)
        
        if tokenizer.next.value == "readline":
            tokenizer.selectNext()
            if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == '(':
                tokenizer.selectNext()
                if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == ')':
                    tokenizer.selectNext()
                    readline = Read()
                    return readline
                else:
                        sys.stderr.write('ERROR: PARENTHESIS NOT CLOSED')
                        sys.exit(1)
            else:
                sys.stderr.write('ERROR: PARENTHESIS NOT OPENED')
                sys.exit(1)
            
                
    @staticmethod
    def parseTerm(tokenizer):
        
        noUm = Parse.parseFactor(tokenizer)
        
        while tokenizer.next.type == 'OPERATOR' and tokenizer.next.value in LIST_TERM:
            
            if tokenizer.next.value == '*':
                tokenizer.selectNext()
                noDois = Parse.parseFactor(tokenizer)
                noUm = BinOp("*", [noUm, noDois])    
                
        return noUm
        
    @staticmethod
    def ParseRelExpression(tokenizer):
        
        noUm = Parse.ParseExpression(tokenizer)
        
        while (tokenizer.next.type == "GREATER" or tokenizer.next.type == "LESS" or tokenizer.next.type == "OPERATOR")  and tokenizer.next.value in LIST_REL:
            
            if tokenizer.next.value == '<':
                tokenizer.selectNext()
                noDois = Parse.ParseExpression(tokenizer)
                noUm = BinOp("<", [noUm, noDois])
            
            elif tokenizer.next.value == '>':
                tokenizer.selectNext()
                noDois = Parse.ParseExpression(tokenizer)
                noUm = BinOp(">", [noUm, noDois])
            
            elif tokenizer.next.value == '==':
                tokenizer.selectNext()
                noDois = Parse.ParseExpression(tokenizer)
                noUm = BinOp("==", [noUm, noDois])
        
        return noUm
            
    @staticmethod
    def ParseExpression(tokenizer):
        
        noUm = Parse.parseTerm(tokenizer)
        
        while tokenizer.next.type == 'OPERATOR' and tokenizer.next.value in LIST_EXP:
            
            if tokenizer.next.value == '+':
                tokenizer.selectNext()
                noDois = Parse.parseTerm(tokenizer)
                noUm = BinOp("+", [noUm, noDois])               
                
            elif tokenizer.next.value == '-':
                tokenizer.selectNext()
                noDois = Parse.parseTerm(tokenizer)
                noUm = BinOp("-", [noUm, noDois])
                
        return noUm
    
    @staticmethod
    def ParseBlock(tokenizer):
        children = []
        
        while tokenizer.next.type != 'EOF':
            children.append(Parse.ParseStatement(tokenizer))
            tokenizer.selectNext()
            
        return Block(children)
    
    @staticmethod
    def ParseStatement(tokenizer):
        if tokenizer.next.value == '\n' and tokenizer.next.type == "QUEBRA_LINHA":
            return NoOp()
                
        if tokenizer.next.value in LIST_RESERVED_WORDS and tokenizer.next.type == 'PRINTLN':
            tokenizer.selectNext()
            
            if tokenizer.next.value == '(':
                tokenizer.selectNext()
                
                children = [Parse.ParseRelExpression(tokenizer)]
                
                if tokenizer.next.value == ')':
                    tokenizer.selectNext()
                    return Print(children)
                
                else:
                    sys.stderr.write('ERROR: PARENTHESIS NOT CLOSED')
                    sys.exit(1)
            else:
                sys.stderr.write('ERROR: PARENTHESIS NOT OPENED')
                sys.exit(1)
    
        if tokenizer.next.type == 'IDENTIFIER':
            name = tokenizer.next.value
            tokenizer.selectNext()
            
            if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value in LIST_ASSIGN:
                tokenizer.selectNext()
                
                children = [Parse.ParseRelExpression(tokenizer)]
                
                return Assignment(name, children)
            
            elif tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == '>>':
                
                tokenizer.selectNext()
                
                if tokenizer.next.type == "TYPE" and tokenizer.next.value == "Int":
                    
                    tokenizer.selectNext()
                    
                    if tokenizer.next.type == "QUEBRA_LINHA" and tokenizer.next.value == '\n':
                        #tokenizer.selectNext()
                        
                        children = [name]
                        
                        return VarDec("Int", children)
                    
                    elif tokenizer.next.type == "OPERATOR" and tokenizer.next.value == "=":
                        tokenizer.selectNext()
                        
                        children = [name, Parse.ParseRelExpression(tokenizer)]
                        
                        return VarDec("Int", children)
                
                if tokenizer.next.type == "TYPE" and tokenizer.next.value == "HP":
                    
                    tokenizer.selectNext()
                    
                    if tokenizer.next.type == "QUEBRA_LINHA" and tokenizer.next.value == '\n':
                        #tokenizer.selectNext()
                        
                        children = [name]
                        
                        return VarDec("HP", children)
                    
                    elif tokenizer.next.type == "OPERATOR" and tokenizer.next.value == "=":
                        tokenizer.selectNext()
                        
                        children = [name, Parse.ParseRelExpression(tokenizer)]
                        
                        return VarDec("HP", children)
                
                if tokenizer.next.type == "TYPE" and tokenizer.next.value == "ATAQUE":
                    
                    tokenizer.selectNext()
                    
                    if tokenizer.next.type == "QUEBRA_LINHA" and tokenizer.next.value == '\n':
                        #tokenizer.selectNext()
                        
                        children = [name]
                        
                        return VarDec("ATAQUE", children)
                    
                    elif tokenizer.next.type == "OPERATOR" and tokenizer.next.value == "=":
                        tokenizer.selectNext()
                        
                        children = [name, Parse.ParseRelExpression(tokenizer)]
                        
                        return VarDec("ATAQUE", children)
                    
                
                if tokenizer.next.type == "TYPE" and tokenizer.next.value == "ITEM":
                    
                    tokenizer.selectNext()
                    
                    if tokenizer.next.type == "QUEBRA_LINHA" and tokenizer.next.value == '\n':
                        #tokenizer.selectNext()
                        
                        children = [name]
                        
                        return VarDec("ITEM", children)
                    
                    elif tokenizer.next.type == "OPERATOR" and tokenizer.next.value == "=":
                        tokenizer.selectNext()
                        
                        children = [name, Parse.ParseRelExpression(tokenizer)]
                        
                        return VarDec("ITEM", children)
                    
                    
                if tokenizer.next.type == "TYPE" and tokenizer.next.value == "String":
                    
                    tokenizer.selectNext()
                    
                    if tokenizer.next.type == "QUEBRA_LINHA" and tokenizer.next.value == '\n':
                        #tokenizer.selectNext()
                        
                        children = [name]
                        
                        return VarDec("String", children)
                    
                    elif tokenizer.next.type == "OPERATOR" and tokenizer.next.value == "=":
                        tokenizer.selectNext()
                        
                        children = [name, Parse.ParseRelExpression(tokenizer)]
                        
                        return VarDec("String", children)
            
            elif (tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == '('):
                    tokenizer.selectNext()
                    
                    filhos = []
                    
                    #ponto de atencao
                    while tokenizer.next.type == ',' or len(filhos) == 0  and tokenizer.next.type != "OPERATOR" and tokenizer.next.value != ")":
                        if tokenizer.next.value == ",":
                            tokenizer.selectNext()
                            
                        expression = Parse.ParseRelExpression(tokenizer)
                        filhos.append(expression)
                    
                    if (tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == ')'):
                        tokenizer.selectNext()
                        
                        call = FuncCall(name, filhos)
                        return call
                    
                    else:
                        sys.stderr.write('ERROR: PARENTHESIS NOT CLOSED')
                        sys.exit(1)
            
            else:
                sys.stderr.write('ERROR: NOR EQUALS NOR OPEN PARENTHESIS FOUND')
                sys.exit(1)
                
        if tokenizer.next.value in LIST_RESERVED_WORDS and tokenizer.next.type == 'IF':
            tokenizer.selectNext()
            
            expression = Parse.ParseRelExpression(tokenizer)
            
            if tokenizer.next.value == '\n' and tokenizer.next.type == "QUEBRA_LINHA":
                tokenizer.selectNext()
                
                if_children = []
                
                while tokenizer.next.type != 'END' and tokenizer.next.type != 'ELSE':
                    if_children.append(Parse.ParseStatement(tokenizer))
                    tokenizer.selectNext()
                    
                block_if = Block(if_children)
                
                if tokenizer.next.value == 'else':
                    tokenizer.selectNext()
                    
                    if tokenizer.next.value == '\n' and tokenizer.next.type == "QUEBRA_LINHA":
                        tokenizer.selectNext()
                        
                        else_children = []	
                        
                        while tokenizer.next.type != 'END':
                            else_children.append(Parse.ParseStatement(tokenizer))
                            tokenizer.selectNext()
                        
                        block_else = Block(else_children)
                        
                        #novo trecho que faltava, consumir o end
                        tokenizer.selectNext()
                        return If([expression, block_if, block_else])
                    
                    else:
                        sys.stderr.write('ERROR: \\n NOT FOUND (ELSE)')
                        sys.exit(1)
                
                if tokenizer.next.type == 'END':
                    tokenizer.selectNext()
                    return If([expression, block_if])
            
            else:
                sys.stderr.write('ERROR: \\n NOT FOUND (IF)')
                sys.exit(1)
                
        if tokenizer.next.type == "WHILE":
            tokenizer.selectNext()
            
            expression = Parse.ParseRelExpression(tokenizer)
            
            if tokenizer.next.value == '\n' and tokenizer.next.type == "QUEBRA_LINHA":
                tokenizer.selectNext()
                
                while_children = []
                
                while tokenizer.next.type != 'END':
                    while_children.append(Parse.ParseStatement(tokenizer))
                    tokenizer.selectNext()
                
                #precisa consumir o END 
                tokenizer.selectNext()
                block_while = Block(while_children)
                return While([expression, block_while])
                
            else:
                sys.stderr.write('ERROR: \\n NOT FOUND (WHILE)')
                sys.exit(1)
        
        if tokenizer.next.type == "FUNCTION" and tokenizer.next.value == "function":
            tokenizer.selectNext()
            
            if tokenizer.next.type == "IDENTIFIER":
                name = tokenizer.next.value
                tokenizer.selectNext()
                
                if tokenizer.next.type == "OPERATOR" and tokenizer.next.value == "(":
                    tokenizer.selectNext()
                    
                    filhos = []
                    
                    #ponto de atencao
                    while (tokenizer.next.value == "," or len(filhos) == 0) and tokenizer.next.type != "OPERATOR" and tokenizer.next.value != ")":
                        if tokenizer.next.value == ",":
                            tokenizer.selectNext()
                        
                        if tokenizer.next.type == "IDENTIFIER":
                            name_var = tokenizer.next.value
                            tokenizer.selectNext()
                            
                            if tokenizer.next.value == "=>" and tokenizer.next.type == "OPERATOR":
                                tokenizer.selectNext()
                                
                                if tokenizer.next.type == "TYPE" and tokenizer.next.value == "Int":
                                    filhos.append(VarDec("Int", [name_var]))
                                    tokenizer.selectNext()
                                
                                elif tokenizer.next.type == "TYPE" and tokenizer.next.value == "String":
                                    filhos.append(VarDec("String", [name_var]))
                                    tokenizer.selectNext()
                                
                                elif tokenizer.next.type == "TYPE" and tokenizer.next.value == "ATAQUE":
                                    filhos.append(VarDec("ATAQUE", [name_var]))
                                    tokenizer.selectNext()
                                
                                elif tokenizer.next.type == "TYPE" and tokenizer.next.value == "HP":
                                    filhos.append(VarDec("HP", [name_var]))
                                    tokenizer.selectNext()
                                
                                elif tokenizer.next.type == "TYPE" and tokenizer.next.value == "ITEM":
                                    filhos.append(VarDec("ITEM", [name_var]))
                                    tokenizer.selectNext()
                                
                                else:
                                    sys.stderr.write('ERROR: TYPE NOT FOUND')
                                    sys.exit(1)
                    
                    
                    if tokenizer.next.type == "OPERATOR" and tokenizer.next.value == ")":
                        tokenizer.selectNext()
                        
                            
                        if tokenizer.next.type == "TYPE" and tokenizer.next.value == "Int":
                            
                            functype = tokenizer.next.value
                            tokenizer.selectNext()
                            
                            if tokenizer.next.value == '\n' and tokenizer.next.type == "QUEBRA_LINHA":
                                tokenizer.selectNext()
            
                                while_children = []
            
                                while tokenizer.next.type != 'END':
                                    while_children.append(Parse.ParseStatement(tokenizer))
                                    tokenizer.selectNext()
                                
                                #precisa consumir o END 
                                tokenizer.selectNext()
                                block_while = Block(while_children)
                                
                                return FuncDec(functype, [name, filhos, block_while])
                            
                            else:
                                sys.stderr.write('ERROR: \\n NOT FOUND (FUNCTION)')
                                sys.exit(1)
                        
                        elif tokenizer.next.type == "TYPE" and tokenizer.next.value == "String":
                            
                            functype = tokenizer.next.value
                            tokenizer.selectNext()
                            
                            if tokenizer.next.value == '\n' and tokenizer.next.type == "QUEBRA_LINHA":
                                tokenizer.selectNext()
            
                                while_children = []
            
                                while tokenizer.next.type != 'END':
                                    while_children.append(Parse.ParseStatement(tokenizer))
                                    tokenizer.selectNext()
                                
                                #precisa consumir o END 
                                tokenizer.selectNext()
                                block_while = Block(while_children)
                                
                                return FuncDec(functype, [name, filhos, block_while])
                            
                            else:
                                sys.stderr.write('ERROR: \\n NOT FOUND (FUNCTION)')
                                sys.exit(1)
                                
                        elif tokenizer.next.type == "TYPE" and tokenizer.next.value == "HP":
                            
                            functype = tokenizer.next.value
                            tokenizer.selectNext()
                            
                            if tokenizer.next.value == '\n' and tokenizer.next.type == "QUEBRA_LINHA":
                                tokenizer.selectNext()
            
                                while_children = []
            
                                while tokenizer.next.type != 'END':
                                    while_children.append(Parse.ParseStatement(tokenizer))
                                    tokenizer.selectNext()
                                
                                #precisa consumir o END 
                                tokenizer.selectNext()
                                block_while = Block(while_children)
                                
                                return FuncDec(functype, [name, filhos, block_while])
                            
                            else:
                                sys.stderr.write('ERROR: \\n NOT FOUND (FUNCTION)')
                                sys.exit(1)
                        
                        elif tokenizer.next.type == "TYPE" and tokenizer.next.value == "ATAQUE":
                            
                            functype = tokenizer.next.value
                            tokenizer.selectNext()
                            
                            if tokenizer.next.value == '\n' and tokenizer.next.type == "QUEBRA_LINHA":
                                tokenizer.selectNext()
            
                                while_children = []
            
                                while tokenizer.next.type != 'END':
                                    while_children.append(Parse.ParseStatement(tokenizer))
                                    tokenizer.selectNext()
                                
                                #precisa consumir o END 
                                tokenizer.selectNext()
                                block_while = Block(while_children)
                                
                                return FuncDec(functype, [name, filhos, block_while])
                            
                            else:
                                sys.stderr.write('ERROR: \\n NOT FOUND (FUNCTION)')
                                sys.exit(1)
                                
                        elif tokenizer.next.type == "TYPE" and tokenizer.next.value == "ITEM":
                            
                            functype = tokenizer.next.value
                            tokenizer.selectNext()
                            
                            if tokenizer.next.value == '\n' and tokenizer.next.type == "QUEBRA_LINHA":
                                tokenizer.selectNext()
            
                                while_children = []
            
                                while tokenizer.next.type != 'END':
                                    while_children.append(Parse.ParseStatement(tokenizer))
                                    tokenizer.selectNext()
                                
                                #precisa consumir o END 
                                tokenizer.selectNext()
                                block_while = Block(while_children)
                                
                                return FuncDec(functype, [name, filhos, block_while])
                            
                            else:
                                sys.stderr.write('ERROR: \\n NOT FOUND (FUNCTION)')
                                sys.exit(1)
                        
                        else:
                            sys.stderr.write('ERROR: TYPE NOT FOUND')
                            sys.exit(1)
                           
                    else: 
                        sys.stderr.write('ERROR: ) NOT FOUND')
                        sys.exit(1)                
                
        if tokenizer.next.type == "RETURN" and tokenizer.next.value == "return":
            tokenizer.selectNext()
            
            expression = Parse.ParseRelExpression(tokenizer)
            
            return Return(expression)
        else:
            sys.stderr.write('ERROR: IDENTIFIER NOT FOUND')
            sys.exit(1)
       
    @staticmethod
    def run(code):
        tokenizer = Tokenizer(code, 0)
        tokenizer.selectNext()
        
        arvore = Parse.ParseBlock(tokenizer)
        if tokenizer.next.type != 'EOF':
            sys.stderr.write('ERROR: EOF NOT FOUND')
            sys.exit(1)
            
        return arvore
    
class PrePro:
    
    @staticmethod
    def filter(code):
        code_filtered = re.sub(r'#.*\n', '', code, flags=re.MULTILINE).replace("\s", "")
        return code_filtered
    
def read_file(file):                      
    with open(file, 'r') as f:
        return f.read()

string = 'test_case_6.jl'
#string = sys.argv[1]
test_files = read_file(string)
sb = SymbolTable()
Parse.run(PrePro.filter(test_files)).evaluate(sb)
