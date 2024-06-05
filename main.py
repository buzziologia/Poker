import random
from collections import Counter
from baralho import Baralho
from jogador import Jogador
from poker import Poker



if __name__ == "__main__":
    print(r"""
                  ██████                                                      
████████████      █             █     █████    █████   ██████████   ████████████  
█████████████    ██    ██████   ███   █████   ████     ██████████   █████████████ 
█████    █████ ████ █████  ████ ███   █████ █████      ████         ████     █████
█████    ████  █   ████      ███   █  ██████████       ██████████   ████     ████ 
█████████████      ██          ██  █  █████████        ██████████   █████████████ 
███████████    █   ██          █   █  █████ █████      ████         ██████████    
█████          █ ██ █████  ████ ████  █████  █████     ████         ██████████    
█████            ██    ██████   ███   █████   █████    ██████████   ████   █████  
█████             █      █      █     █████    █████   ██████████   ████    █████ 
                         ██ ████ █                                                    
        """)
    print("===============================================================================          ")
    print(r"""
.------..------..------.        .------..------..------..------..------.
|B.--. ||E.--. ||M.--. | .-.    |V.--. ||I.--. ||N.--. ||D.--. ||O.--. |
| :(): || (\/) || (\/) |((5))   | :(): || (\/) || :(): || :/\: || :/\: |
| ()() || :\/: || :\/: | '-.-.  | ()() || :\/: || ()() || (__) || :\/: |
| '--'B|| '--'E|| '--'M|  ((1)) | '--'V|| '--'I|| '--'N|| '--'D|| '--'O|
`------'`------'`------'   '-'  `------'`------'`------'`------'`------'
    """)
    print("===============================================================================          ")
    print()
    digite_enter = input("Digite Enter para iniciar o jogo: ")
    print()
    if digite_enter == "" or digite_enter == "Enter":
        quant_jogadores = int(input("Por favor, selecione o número de jogadores (2-9): "))
        jogadores = []
        senhas = []
        for i in range(quant_jogadores):
            print()
            nome = input(f"    Digite o nome do jogador {i+1}: ")
            senha = input(f"    Informe uma senha para {nome}: ")
            jogadores.append(nome)
            senhas.append(senha)
        jogo = Poker(jogadores, senhas)
        jogo.iniciar_jogo()
