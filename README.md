# POKEBATTLE_COMPILER

O repositório tem por objetivo criar um compilador para uma linguagem de programação baseada em batalhas pokemon. Nela você consegue definir equipes, regras e estratégias para simular uma batalha.

## EBNF da linguagem
```
LETTER = ("a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" |
            "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" |
             "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J' | "K" | "L" | "M" | "N" | "O" | "P" 
             | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" )

DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 )

TIPO = ( NORMAL | FOGO | AGUA | ELETRICO | GRAMA | GELO | LUTADOR | VENENO | 
        TERRA | VOADOR | PSIQUICO | INSETO | PEDRA | FANTASMA | DRAGAO | AÇO | 
        FADA | SOMBRIO )

POKEMON_OPTIONS = ("Dragonite" | "Eevee" | "Garchomp" | "Glaceon" | "Empoleon" | "Togekiss" | 
        "Charizard" | "Ho-oh" | "Pikachu" | "Entei" | "Suicune" | "Blastoise" | "Mimikyu" |
        "Lucario" | "Corsola" | "Emolga" | "Serviper" | "Torterra" | "Altaria" | "Absol" | "Palkia" |
        "Darkari", "Gallade", "Lapras", "Milotic", "Spiritomb", "Roserade")

STRING = LETTER {LETTER}
NUMBER = DIGIT {DIGIT}

VALUE = STRING | NUMBER 
IDENTIFIER = (LETTER)

BOOL_OPERATIONS = ("IGUAL" | "MAIOR" | "MENOR"| "E"| "OU")

ATRIBUTE = ("HP", "ATAQUE", "POKEMON", "ITENS", "HABILIDADE", "TIME", "OPONENTE")

ASSIGNMENT = ATRIBUTE, STRING, "TEM", NUMBER | STRING, "."

TEAM_DECLARATION = STRING, "TEM", {",", POKEMON,  POKEMON_OPTIONS}, "."

IF_DECLARATION = "SE", BOOLEAN_EXPRESSION , THEN_EXPRESSION, "."

THEN_EXPRESSION = (ESCOLHER, POKEMON) | (USAR, ITENS, IDENTIFIER) | (CAUSAR, NUMBER, "x", IDENTIFIER)

BOOLEAN_EXPRESSION = (ATRIBUTE, "OPONENTE", BOOL_OPERATIONS, TIPO) | (IDENTIFIER, BOOL_OPERATIONS, NUMBER)

FUNCTION_DECLARATION = ("GOLPE" | "ESTRATEGIA"), STRING, ":", IF_DECLARATION

LOOP_DECLARATION = "ENQUANTO BATALHA", ":", ["ESTRATEGIA", FUNCTION_NAME, "."]
``` 

## Exemplo de código

```
OPONENTE Garchomp, Lucario, Milotic, Roserade, Spiritomb.

HP garchomp_hp TEM 200.
ATAQUE garchomp_attack TEM 180.
HABILIDADE garchomp_special TEM DragonClaw.
TIPO garchomp_type TEM DRAGON.

.
.
.

#agora devem ser iniciada as regras da batalha. Você cria as regras como se a máquina devesse 
#seguir com base nos acontecimentos, como um manual de batalha.

#definindo todos os setups de trocas do jogo. Funciona como definir funções.

ESTRATEGIA BASE:
    SE TIPO OPONENTE IGUAL DRAGAO, ESCOLHER Glaceon. 
    SE TIPO OPONENTE IGUAL LUTADOR, ESCOLHER Togekiss.
    SE TIPO OPONENTE IGUAL AGUA, ESCOLHER Mimikyu.

    SE glaceon_hp IGUAL 0, USAR revive.
    SE lapras_hp IGUAL 0, USAR revive.
    SE mimikyu_hp IGUAL 0, USAR revive.

    SE glaceon_hp MAIOR 0 E MENOR 50, USAR potion.
    SE gallade_hp MAIOR 0 E MENOR 120, USAR max_potion.

#voce tambem pode criar funcoes de ataque. Caso nao crie, o ataque tera o ataque base 

GOLPE WoodHammer:
    
    SE mimikyu_hp MENOR 60, CAUSAR 10x mimikyu_attack.
    SE TIPO OPONENTE WATER, CAUSAR 5x mimikyu_attack.

#A batalha é feita por turnos. Uma vez sua e outra do oponente. No turno 0 é feito o processo
#de escolha dos pokemons.
   

ENQUANTO BATALHA:
    ESTRATEGIA BASE.
    TURNO OPONENTE.
    TURNO JOGADOR.
```
