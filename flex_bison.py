from rply import LexerGenerator
from rply import ParserGenerator
from rply.token import Token
from rply.errors import ParsingError



lg = LexerGenerator()

lg.add('NUMBER', r'\d+')
lg.ignore(r'\s+')
lg.add('TIPO', r'(NORMAL|FOGO|AGUA|ELETRICO|GRAMA|GELO|LUTADOR|VENENO|TERRA|VOADOR|PSIQUICO|INSETO|PEDRA|FANTASMA|DRAGAO|AÇO|FADA|SOMBRIO)')
lg.add('POKEMON', r'(Dragonite|Eevee|Garchomp|Glaceon|Empoleon|Togekiss|Charizard|Ho-oh|Pikachu|Entei|Suicune|Blastoise|Mimikyu|Lucario|Corsola|Emolga|Serviper|Torterra|Altaria|Absol|Palkia|Gallade|Lapras|Milotic|Spiritomb|Roserade)')
lg.add('ITEM', r'(Revive|Potion|Super_Potion|Hyper_Potion)')
lg.add('IF', r'SE')
lg.add('BOOL_OP', r'(IGUAL|MAIOR|MENOR|E|OU)')
lg.add("ASSIGN", r'TEM')
lg.add("ACTION", r'(ESCOLHER|USAR)')
lg.add("EQUIPE", r'(TIME|OPONENTE)')
lg.add("ATRIBUTE", r'(HP|ATAQUE|POKEMON|ITENS|HABILIDADE)')
lg.add("END_STATMENT", r'\.')
lg.add("QUEBRA", r'\\n')
lg.add("WHILE", r'ENQUANTO BATALHA')
lg.add("END_FUNCTION", r'\:')
lg.add("FUNC_DEC", r'(GOLPE|ESTRATEGIA)')

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

    
@pg.production('time_pokemons : EQUIPE loop_pokemon END_STATMENT')
def time_pokemons(p):
    print("time_pokemons: "  + str(p))

@pg.production('loop_pokemon : ATRIBUTE POKEMON loop_pokemon')
def loop_pokemon(p):
    print("loop_pokemon: "  + str(p))
    

@pg.production('loop_pokemon :')
def empty_loop_pokemon(p):
    return []

@pg.production('pokemon_definition : ATRIBUTE VAR_NAME ASSIGN NUMBER END_STATMENT')
def pokemon_definition(p):
    print("pokemon_definition: "  + str(p))
    
@pg.production('item_definition: ATRIBUTE VAR_NAME END_FUNCTION loop_item END_STATMENT')
def item_definition(p):
    print("item_definition: "  + str(p))
    
@pg.production('loop_item : NUMBER ITEM loop_item')
def loop_item(p):
    print("loop_item: "  + str(p))
    
@pg.production('loop_item :')
def empty_loop_item(p):
    return []

#PRECISA QUE TENHA VARIAS CONDIÇÕES DE IF COMBINADAS
@pg.production('if_statement : IF VAR_NAME BOOL_OP NUMBER ACTION ITEM END_STATMENT')
def if_statement(p):
    print("if_statement: "  + str(p))
    
@pg.production('loop_if_statement : if_statement loop_if_statement')
def loop_if_statement(p):
    print("loop_if_statement: "  + str(p))
    
@pg.production('loop_if_statement :')
def empty_loop_if_statement(p):
    return []

@pg.production('func_declaration : FUNC_DEC VAR_NAME END_FUNCTION QUEBRA loop_if_statement')
def func_declaration(p):
    print("func_declaration: "  + str(p))
    
@pg.production('loop_func_declaration : func_declaration loop_func_declaration')
def loop_func_declaration(p):
    print("loop_func_declaration: "  + str(p))

@pg.production('loop_func_declaration :')
def empty_loop_func_declaration(p):
    return []


@pg.production('begin_battle : WHILE  END_FUNCTION QUEBRA loop_function_call')
def begin_battle(p):
    print("begin_battle: "  + str(p))

@pg.error
def error_handler(token):
    raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())

parser = pg.build()

#ast = parser.parse(lexer.lex('TIME POKEMON Glaceon POKEMON Togekiss.'))
ast = parser.parse(lexer.lex('HP pikachu_hp TEM 120.'))


#for token in lexer.lex('HP pikachu_hp TEM 120.'):
#    pass
#    print(token)