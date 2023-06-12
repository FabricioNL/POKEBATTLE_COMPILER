# POKEBATTLE_COMPILER

O objetivo desse projeto é implementar uma linguagem de programação capaz de simular batalhas pokemons. Assim como simuladores famosos como pokemon showdown [https://play.pokemonshowdown.com/], um dos principais objetivos é tornar possível o treino para batalhas competitivas sem a necessidade de outros jogares, apenas simulando estratégias.


## EBNF da linguagem
```
program = { statement } ;

statement = atributes_declaration
          | tipo_declaration
          | bin_op
          | assign
          | while_block
          | if_block
          | func_declaration
          | funcall ;

atributes_declaration = VAR_NAME ">>" ATRIBUTE_INT "IGUAL" NUMBER ;

tipo_declaration = VAR_NAME ">>" ATRIBUTE_STR "IGUAL" ASPAS STRING ASPAS ;

bin_op = VAR_NAME BINOP VAR_NAME ;

bool_op = VAR_NAME BOOL_OP NUMBER ;

assign = VAR_NAME "IGUAL" bin_op ;

while_block = "BATALHA" bool_op QUEBRA program "FIM_TATICA" ;

if_block = "SE" bool_op QUEBRA program "FIM_TATICA" ;

func_declaration = "ESTRATEGIA" VAR_NAME "(" func_params ")" func_return_block "FIM_TATICA" ;

func_params = VAR_NAME "=>" VAR_NAME { "," VAR_NAME "=>" VAR_NAME } ;

func_return_block = program "RESULTADO" VAR_NAME ;

funcall = VAR_NAME "IGUAL" VAR_NAME "(" funcall_params ")" ;

funcall_params = VAR_NAME { "," VAR_NAME } ;

```

## Exemplo de código

```
pikachu_hp>>HP IGUAL 80
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
  
```
