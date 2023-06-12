from rply import LexerGenerator, ParserGenerator

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
lg.add("BINOP", r'(RECUPERAR|ATACAR|\*)')
lg.add("END", r'FIM_TATICA')
lg.add("WHILE", r'BATALHA')
lg.add("RETURN", r'RESULTADO')
lg.add("ASPAS", r'\"')
lg.add("OPEN_PAREN", r'\(')
lg.add("CLOSE_PAREN", r'\)')
lg.add("DOUBLE_ARROW", r'>>')
lg.add("SEMI_ARROW", r'=>')
lg.add("FUNC_DEC", r'(ESTRATEGIA)')
lg.add('STRING', r'[A-Z]+')
lg.add('VAR_NAME', r'[a-zA-Z]+_[a-zA-Z]+')

lexer = lg.build()

pg = ParserGenerator(
    # Uma lista de nomes de todos os tokens, aceitos pelo parser
    ['NUMBER', 'IF', 'BOOL_OP', 'ASSIGN', 'ATRIBUTE_INT', 
     'ATRIBUTE_STR', 'QUEBRA', 'VIRGULA', 'BINOP', 'END', 'WHILE', 'RETURN', 'ASPAS', 
     'OPEN_PAREN', 'CLOSE_PAREN', 'DOUBLE_ARROW', 'SEMI_ARROW', 'FUNC_DEC', 'VAR_NAME', 'STRING'],
)

@pg.production('program : statement program')
@pg.production('program : statement')
def program(p):
    pass

@pg.production('statement : atributes_declaration')
@pg.production('statement : tipo_declaration')
@pg.production('statement : bin_op')
@pg.production('statement : assign')
@pg.production('statement : while_block')
@pg.production('statement : if_block')
@pg.production('statement : func_declaration')
@pg.production('statement : funcall')
def statement(p):
    pass

@pg.production('atributes_declaration : VAR_NAME DOUBLE_ARROW ATRIBUTE_INT ASSIGN NUMBER')
def atributes_declaration(p):
    print("var declaration:", p)

@pg.production('tipo_declaration : VAR_NAME DOUBLE_ARROW ATRIBUTE_STR ASSIGN ASPAS STRING ASPAS')
def tipo_declaration(p):
    print("item declaration:", p)

@pg.production("bin_op : VAR_NAME BINOP VAR_NAME")
def bin_op(p):
    print("binop:", p)

@pg.production("bool_op : VAR_NAME BOOL_OP NUMBER")
def bool_op(p):
    print("boolop:", p)

@pg.production("assign : VAR_NAME ASSIGN bin_op")
def assign(p):
    print("assign:", p)

@pg.production("while_block : WHILE bool_op QUEBRA program END")
def while_block(p):
    print("while_block:", p)

@pg.production("if_block : IF bool_op QUEBRA program END")
def if_block(p):
    print("if_block:", p)

@pg.production("func_declaration : FUNC_DEC VAR_NAME OPEN_PAREN func_params CLOSE_PAREN func_return_block END")
def func_declaration(p):
    print("func declaration:", p)

@pg.production("func_params : VAR_NAME SEMI_ARROW VAR_NAME func_params")
@pg.production("func_params : VAR_NAME SEMI_ARROW VAR_NAME")
def func_params(p):
    pass

@pg.production("func_return_block : program RETURN VAR_NAME")
def func_return_block(p):
    print("func return block:", p)
@pg.production("funcall : VAR_NAME ASSIGN VAR_NAME OPEN_PAREN funcall_params CLOSE_PAREN")
def funcall(p):
    print("funcall:", p)
@pg.production("funcall_params : VAR_NAME VIRGULA VAR_NAME funcall_params")
@pg.production("funcall_params : VAR_NAME")
@pg.production("funcall_params :")
def funcall_params(p):
    pass


parser = pg.build()

# EXEMPLO DE ENTRADA
DEC_ENTRY = """
pikachu_hp>>HP IGUAL 80
pikachu_attack>>ATAQUE IGUAL 18
pikachu_tipo>>TIPO IGUAL "ELETRICO"
"""

ast = parser.parse(lexer.lex(DEC_ENTRY))
