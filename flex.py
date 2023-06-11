from rply import LexerGenerator

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

entrada = """pikachu_hp>>HP IGUAL 80
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
FIM_TATICA""" 

for token in lexer.lex(entrada):
    print(token)