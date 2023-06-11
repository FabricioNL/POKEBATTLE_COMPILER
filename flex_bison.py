from rply import LexerGenerator
from rply import ParserGenerator
from rply.token import Token
from rply.errors import ParsingError

lg = LexerGenerator()

lg.add('NUMBER', r'\d+')
lg.ignore(r'\s+')
lg.add('IF', r'SE')
lg.add('BOOL_OP', r'(MAIOR|MENOR|EXATO)')
lg.add("ASSIGN", r'IGUAL')
lg.add("ATRIBUTE_INT", r'(HP|ATAQUE)')
lg.add("ATRIBUTE_STR", r'(TIPO)')
lg.add("QUEBRA", r'\\n')
lg.add("VIRGULA", r',')
lg.add("BINOP" , r'(RECUPERAR|ATACAR|\*)')
lg.add("END", r'FIM_TATICA')
lg.add("WHILE", r'BATALHA')
lg.add("RETURN", r'RESULTADO')
lg.add("ASPAS", r'\"')
lg.add("OPEN_PAREN", r'\(')
lg.add("CLOSE_PAREN", r'\)')
lg.add("DOUBLE_ARROW", r'>>')
lg.add("SEMI_ARROW", r'=>')
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
    ['NUMBER', 'IF', 'BOOL_OP', 'ASSIGN', 'ATRIBUTE_INT', 'ATRIBUTE_STR', 'QUEBRA', 'VIRGULA', 'BINOP', 'END', 'WHILE', 'RETURN', 'ASPAS', 'OPEN_PAREN', 'CLOSE_PAREN', 'DOUBLE_ARROW', 'SEMI_ARROW', 'FUNC_DEC', 'VAR_NAME'],
)

#@pg.production('main : pokemon_atributes_declaration main')
#@pg.production('main : item_declaration main')
#@pg.production('main : item_definition main')

#@pg.production('main : ')
#def main(p):
#    pass    
#
##loop declaração equipe    
#@pg.production('pokemon_atributes_declaration : ATRIBUTE VAR_NAME ASSIGN NUMBER END_STATMENT')
#def time_pokemons(p):
#    print("var declaration: "  + str(p))
#    
#
#@pg.production('item_declaration : ITEM VAR_NAME ASSIGN NUMBER END_STATMENT')
#def loop_item(p):
#    print("item declaration: "  + str(p))

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

#parser = pg.build()

#EXEMPLOS DE ENTRADA

#ast = parser.parse(lexer.lex('HP pikachu_hp IGUAL 120.')) --funcionando
#ast = parser.parse(lexer.lex('ITEM max_potion IGUAL 20.')) --funcionando


#PARA DEBUG
for token in lexer.lex(
"""pikachu_hp>>HP IGUAL 80
pikachu_attack>>ATAQUE IGUAL 18
pikachu_tipo>>TIPO IGUAL "ELETRICO"

mimikyu_hp>>HP IGUAL 60
mimikyu_attack>>ATAQUE IGUAL 30
mimikyu_tipo>>TIPO IGUAL "FANTASMA"

max_potion>>ITEM IGUAL 50
super_potion>>ITEM IGUAL 30

mimikyu_hp IGUAL pikachu_attack ATACAR mimikyu_hp
pikachu_hp IGUAL mimikyu_attack ATACAR pikachu_hp

ESTRATEGIA estrategia_base(pokemon_hp=>HP, item_name=>ITEM) HP
    SE pokemon_hp MENOR 30
        pokemon_hp IGUAL item_name RECUPERAR pokemon_hp 
    FIM_TATICA

    RESULTADO pokemon_hp
FIM_TATICA

BATALHA mimikyu_hp MAIOR 0
    pikachu_hp IGUAL estrategia_base(pikachu_hp, max_potion)
    mimikyu_hp IGUAL pikachu_attack ATACAR mimikyu_hp
    pikachu_hp IGUAL mimikyu_attack ATACAR pikachu_hp
FIM_TATICA
"""):
    
    print(token)