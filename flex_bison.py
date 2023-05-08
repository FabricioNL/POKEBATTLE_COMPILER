from rply import LexerGenerator
from rply import ParserGenerator
from rply.token import Token

lg = LexerGenerator()

lg.add('NUMBER', r'\d+')
lg.ignore(r'\s+')
lg.add('TIPO', r'(NORMAL|FOGO|AGUA|ELETRICO|GRAMA|GELO|LUTADOR|VENENO|TERRA|VOADOR|PSIQUICO|INSETO|PEDRA|FANTASMA|DRAGAO|AÇO|FADA|SOMBRIO)')
lg.add('POKEMON', r'(Dragonite|Eevee|Garchomp|Glaceon|Empoleon|Togekiss|Charizard|Ho-oh|Pikachu|Entei|Suicune|Blastoise|Mimikyu|Lucario|Corsola|Emolga|Serviper|Torterra|Altaria|Absol|Palkia|Gallade|Lapras|Milotic|Spiritomb|Roserade)')
lg.add('ITEM', r'(Revive|Potion|Super_Potion|Hyper_Potion)')
lg.add('BOOL_OP', r'(IGUAL|MAIOR|MENOR|E|OU)')
lg.add("ASSIGN", r'TEM')
lg.add("EQUIPE", r'(TIME|OPONENTE)')
lg.add("ATRIBUTE", r'(HP|ATAQUE|POKEMON|ITENS|HABILIDADE)')
lg.add("END_STATMENT", r'\.')

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


parser = pg.build()

#ast = parser.parse(lexer.lex('TIME POKEMON Glaceon POKEMON Togekiss.'))
ast = parser.parse(lexer.lex('TIME POKEMON Glaceon POKEMON Togekiss.'))


for token in lexer.lex('HP pikachu_hp TEM 120.'):
    pass
    print(token)