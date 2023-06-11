pikachu_hp::HP IGUAL 100
pikachu_attack::ATAQUE IGUAL 18
pikachu_tipo::TIPO IGUAL "ELETRICO"

mimikyu_hp::HP IGUAL 60
mimikyu_attack::ATAQUE IGUAL 30
mimikyu_tipo::TIPO IGUAL "FANTASMA"

max_potion::ITEM IGUAL 50
super_potion::ITEM IGUAL 30

mimikyu_hp IGUAL pikachu_attack ATACAR mimikyu_hp
pikachu_hp IGUAL mimikyu_attack ATACAR pikachu_hp

pikachu_hp IGUAL max_potion RECUPERAR pikachu_hp

