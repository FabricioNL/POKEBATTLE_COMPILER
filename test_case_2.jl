pikachu_hp::HP IGUAL 100
pikachu_attack::ATAQUE IGUAL 18

mimikyu_hp::HP IGUAL 60
mimikyu_attack::ATAQUE IGUAL 30

ENQUANTO pikachu_hp MAIOR 0
    mimikyu_hp IGUAL pikachu_attack ATACAR mimikyu_hp
    pikachu_hp IGUAL mimikyu_attack ATACAR pikachu_hp
    println(pikachu_hp)
FIM_TATICA