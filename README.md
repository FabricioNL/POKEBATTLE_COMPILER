# POKEBATTLE_COMPILER

O objetivo desse projeto é implementar uma linguagem de programação capaz de simular batalhas pokemons. Assim como simuladores famosos como pokemon showdown [https://play.pokemonshowdown.com/], um dos principais objetivos é tornar possível o treino para batalhas competitivas sem a necessidade de outros jogares, apenas simulando estratégias.

Uma apresentação sobre a linguagem pode ser acessada no link a seguir: [clique aqui](https://www.canva.com/design/DAFlo3A9Dmc/4UswNXZCTWYhu-jiVRHO7A/edit?utm_content=DAFlo3A9Dmc&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

## Como utilizar

Para utilizar a linguagem, é importante utilizar o compiler.py presente no repositório. Assim, basta criar um arquivo com o código escrito em POKEBATTLE seguindo a EBNF da linguagem e rodar o script do compilador passando o caminho do arquivo de texto como entrada.

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
A linguagem desenvolvida permite o desenvolvimento de LOOPs, operações binárias, condicionais, operações aritméticas, declarações de função e de variáveis. Todas as operações de batalha, como RECUPERAR HP ou Atacar outro pokemon funcionam como operações aritméticas em outras linguagens.

O arquivo abaixo representa o test_case_5.jl, presente no repositório. Também há outros testes no repositório para verificar o funcionamento individual das partes da linguagem.

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

Saída esperada:

```
pikachu atacou mimikyu
mimikyu perdeu 18 de HP
mimikyu atacou pikachu
pikachu perdeu 30 de HP
pokebattle iniciada!
pikachu atacou mimikyu
mimikyu perdeu 18 de HP
mimikyu atacou pikachu
pikachu perdeu 30 de HP
trainer utilizou item_name
pokemon recuperou 50 de HP
pikachu atacou mimikyu
mimikyu perdeu 18 de HP
mimikyu atacou pikachu
pikachu perdeu 30 de HP
pikachu atacou mimikyu
mimikyu perdeu 18 de HP
mimikyu atacou pikachu
pikachu perdeu 30 de HP
mimikyu desmaiou!
```
