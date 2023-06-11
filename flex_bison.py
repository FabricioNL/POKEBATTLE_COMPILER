from rply import LexerGenerator
from rply import ParserGenerator
from rply.token import Token
from rply.errors import ParsingError

lg = LexerGenerator()

lg.add('NUMBER', r'\d+')
lg.ignore(r'\s+')
lg.add('TIPO', r'(NORMAL|FOGO|AGUA|ELETRICO|GRAMA|GELO|LUTADOR|VENENO|TERRA|VOADOR|PSIQUICO|INSETO|PEDRA|FANTASMA|DRAGAO|AÇO|FADA|SOMBRIO)')
lg.add('ITEM', r'ITEM')
lg.add('IF', r'SE')
lg.add('BOOL_OP', r'(MAIOR|MENOR)')
lg.add("ASSIGN", r'IGUAL')
lg.add("ACTION", r'(USAR)')
lg.add("ATRIBUTE", r'(HP|ATAQUE|POKEMON|ITENS|HABILIDADE)')
lg.add("END_STATMENT", r'\.')
lg.add("QUEBRA", r'\\n')
lg.add("WHILE", r'ENQUANTO')
lg.add("END_FUNCTION", r'\:')
lg.add("FUNC_DEC", r'(ESTRATEGIA)')
lg.add('VAR_NAME', r'[a-zA-Z_]+')


lexer = lg.build()

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def __repr__(self):
        return f'{self.value} ({self.children})'

pg = ParserGenerator(
    # Uma lista de nomes de todos os tokens, aceitos pelo parser
    ['TIPO', 'POKEMON', 'ITEM', 'BOOL_OP', 'ASSIGN', 'EQUIPE', 'ATRIBUTE', 'END_STATMENT', 'WHILE', 'END_FUNCTION', 'VAR_DEC', 'VAR_NAME', 'STRING', 'NUMBER'],
)

@pg.production('main : pokemon_atributes_declaration main')
@pg.production('main : item_declaration main')
#@pg.production('main : item_definition main')

@pg.production('main : ')
def main(p):
    pass    

#loop declaração equipe    
@pg.production('pokemon_atributes_declaration : ATRIBUTE VAR_NAME ASSIGN NUMBER END_STATMENT')
def time_pokemons(p):
    print("var declaration: "  + str(p))
    

@pg.production('item_declaration : ITEM VAR_NAME ASSIGN NUMBER END_STATMENT')
def loop_item(p):
    print("item declaration: "  + str(p))

#loop definição de variaveis
#@pg.production('pokemon_definition : ATRIBUTE VAR_NAME ASSIGN NUMBER END_STATMENT')
#def pokemon_definition(p):
#    print("pokemon_definition: "  + str(p))
    
#@pg.production('item_definition : ATRIBUTE VAR_NAME END_FUNCTION loop_item END_STATMENT')
#def item_definition(p):
#    print("item_definition: "  + str(p))


   
#@pg.production('loop_item :')
#def empty_loop_item(p):
#    pass

##PRECISA QUE TENHA VARIAS CONDIÇÕES DE IF COMBINADAS
#@pg.production('loop_if_statement : if_statement loop_if_statement')
#def loop_if_statement(p):
#    print("loop_if_statement: "  + str(p))
#
#@pg.production('if_statement : IF VAR_NAME BOOL_OP NUMBER ACTION ITEM END_STATMENT')
#def if_statement(p):
#    print("if_statement: "  + str(p))
#    
#@pg.production('loop_if_statement :')
#def empty_loop_if_statement(p):
#    return []
#
#@pg.production('func_declaration : FUNC_DEC VAR_NAME END_FUNCTION QUEBRA loop_if_statement')
#def func_declaration(p):
#    print("func_declaration: "  + str(p))
#    
#@pg.production('loop_func_declaration : func_declaration loop_func_declaration')
#def loop_func_declaration(p):
#    print("loop_func_declaration: "  + str(p))
#
#@pg.production('loop_func_declaration :')
#def empty_loop_func_declaration(p):
#    return []

#@pg.production('begin_battle : WHILE  END_FUNCTION QUEBRA loop_function_call')
#def begin_battle(p):
#    print("begin_battle: "  + str(p))

#@pg.error
#def error_handler(token):
#    raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())

parser = pg.build()

#EXEMPLOS DE ENTRADA

#ast = parser.parse(lexer.lex('HP pikachu_hp IGUAL 120.')) --funcionando
#ast = parser.parse(lexer.lex('ITEM max_potion IGUAL 20.')) --funcionando


#PARA DEBUG
for token in lexer.lex('ITEM max_potion IGUAL 20.'):
    #pass
    print(token)