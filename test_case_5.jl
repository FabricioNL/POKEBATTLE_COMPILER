pikachu_hp::HP IGUAL 80
pikachu_attack::ATAQUE IGUAL 18
pikachu_tipo::TIPO IGUAL "ELETRICO"

mimikyu_hp::HP IGUAL 60
mimikyu_attack::ATAQUE IGUAL 30
mimikyu_tipo::TIPO IGUAL "FANTASMA"

max_potion::ITEM IGUAL 50
super_potion::ITEM IGUAL 30

println(mimikyu_hp)
println(pikachu_hp)

mimikyu_hp IGUAL pikachu_attack ATACAR mimikyu_hp
pikachu_hp IGUAL mimikyu_attack ATACAR pikachu_hp

ESTRATEGIA estrategia_base(pokemon_hp::HP, item_name::ITEM)::HP
    SE pokemon_hp MENOR 30
        pokemon_hp IGUAL item_name RECUPERAR pokemon_hp 
    FIM_TATICA

    RESULTADO pokemon_hp
FIM_TATICA

ENQUANTO mimikyu_hp MAIOR 0
    println(mimikyu_hp)
    println(pikachu_hp)
    pikachu_hp IGUAL estrategia_base(pikachu_hp, max_potion)
    mimikyu_hp IGUAL pikachu_attack ATACAR mimikyu_hp
    pikachu_hp IGUAL mimikyu_attack ATACAR pikachu_hp
FIM_TATICA
