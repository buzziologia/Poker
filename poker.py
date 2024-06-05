class Poker:
    def __init__(self, nomes_jogadores, senhas):
        if len(nomes_jogadores) > 9:
            raise ValueError("O número máximo de jogadores é 9.")
        self.baralho = Baralho()
        self.jogadores = [Jogador(nome) for nome in nomes_jogadores]
        self.board = []
        self.dealer_pos = 0
        self.aposta_minima = 10
        self.pote = 0
        self.maior_aposta = 0

    def iniciar_jogo(self):
        while len([jogador for jogador in self.jogadores if jogador.fichas > 0]) > 1:
            self.distribuir_cartas_iniciais()
            self.visualizar_cartas()
            self.primeira_rodada_apostas()
            self.revelar_flop()
            self.rodada_apostas()
            self.revelar_turn()
            self.rodada_apostas()
            self.revelar_river()
            self.rodada_apostas()
            self.mostrar_vencedor()
            for jogador in self.jogadores:
                if jogador.fichas <= 0:
                    print(f"{jogador.nome} está sem fichas e foi eliminado.")
                    self.jogadores.remove(jogador)

    def distribuir_cartas_iniciais(self):
        for _ in range(2):
            for jogador in self.jogadores:
                carta = self.baralho.distribuir_carta()
                jogador.receber_carta(carta)
                if len(jogador.mao) == 2:
                    self.board.append(jogador.mao[-1])

    def visualizar_cartas(self):
        print()
        print("===============================================================================")
        print(r"""
.------..------..------..------..------.        .------..------..------..------.
|P.--. ||O.--. ||K.--. ||E.--. ||R.--. | .-.    |G.--. ||A.--. ||M.--. ||E.--. |
| :/\: || :/\: || :/\: || (\/) || :(): |((5))   | :/\: || (\/) || (\/) || (\/) |
| (__) || :\/: || :\/: || :\/: || ()() | '-.-.  | :\/: || :\/: || :\/: || :\/: |
| '--'P|| '--'O|| '--'K|| '--'E|| '--'R|  ((1)) | '--'G|| '--'A|| '--'M|| '--'E|
`------'`------'`------'`------'`------'   '-'  `------'`------'`------'`------'

        """)
        print("===============================================================================")
        print("Bem-vindo ao jogo, suas cartas foram distribuídas")
        for jogador in self.jogadores:
            senha_correta = False
            while not senha_correta:
                senha = input(f"Informe a senha para {jogador.nome} visualizar sua carta: ")
                if senha == jogador.nome:
                    print(f"{jogador.nome} suas cartas são: {jogador.mostrar_mao()}")  # Correção aqui
                    print(f"{jogador.nome} tem {jogador.fichas} fichas.")
                    print()
                    print("Por favor, decore suas cartas e prossiga as instruções...")
                    opcao = 0
                    while True:
                        try:
                            opcao = input("Sair: [s] ou Continuar: [c]: ")
                            if opcao.lower() == 's':
                                print('\n' * 50)  # intencionalmente vazio para separar as cartas
                                break
                            else:
                                print('\n' * 50)  # intencionalmente vazio para separar as cartas
                                break
                        except ValueError:
                            print("Senha incorreta. Tente novamente.")
                    senha_correta = True
                else:
                    print("Senha incorreta. Tente novamente.")



    def primeira_rodada_apostas(self):
        self.pote += self.jogadores[(self.dealer_pos + 1) % len(self.jogadores)].apostar(self.aposta_minima // 2)
        self.pote += self.jogadores[(self.dealer_pos + 2) % len(self.jogadores)].apostar(self.aposta_minima)
        self.maior_aposta = self.aposta_minima
        print("===============================================================================")
        print(r"""
.------..------..------..------..------.        .------..------..------..------.
|P.--. ||O.--. ||K.--. ||E.--. ||R.--. | .-.    |G.--. ||A.--. ||M.--. ||E.--. |
| :/\: || :/\: || :/\: || (\/) || :(): |((5))   | :/\: || (\/) || (\/) || (\/) |
| (__) || :\/: || :\/: || :\/: || ()() | '-.-.  | :\/: || :\/: || :\/: || :\/: |
| '--'P|| '--'O|| '--'K|| '--'E|| '--'R|  ((1)) | '--'G|| '--'A|| '--'M|| '--'E|
`------'`------'`------'`------'`------'   '-'  `------'`------'`------'`------'

        """)
        print("===============================================================================")
        print("A primeira rodada de apostas foi iniciada.")
        print()

        for jogador in self.jogadores:
            aposta = int(input(f"{jogador.nome}, faça sua aposta (mínimo {self.maior_aposta}): "))
            self.pote += jogador.apostar(aposta)
            self.maior_aposta = max(self.maior_aposta, aposta)
        self.rodada_apostas(inicio=(self.dealer_pos + 3) % len(self.jogadores))

    def rodada_apostas(self, inicio=0):
        for i in range(len(self.jogadores)):
            jogador = self.jogadores[(inicio + i) % len(self.jogadores)]
            self.tratar_aposta_jogador(jogador)

    def tratar_aposta_jogador(self, jogador):
        if jogador.fichas >= self.maior_aposta - jogador.aposta_atual:
            print()
            print(f"{jogador.nome}, você tem {jogador.fichas} fichas.")
            acao = int(input("Selecione sua ação (1.Apostar | 2.Igualar | 3.Passar): "))
            if acao == 1:
                aposta = int(input(f"Qual o valor da sua aposta? (mínimo {self.maior_aposta}): "))
                self.pote += jogador.apostar(aposta)
                self.maior_aposta = max(self.maior_aposta, aposta)
            elif acao == 2:
                self.pote += jogador.igualar_aposta(self.maior_aposta)
            else:
                pass
        else:
            pass

    def revelar_flop(self):
        flop_cartas = [self.baralho.distribuir_carta() for _ in range(3)]  # Distribui 3 cartas do baralho para o flop
        self.board.extend(flop_cartas)  # Adiciona as cartas do flop ao tabuleiro
        print()
        print("===============================================================================")
        print(r"""
.------..------..------..------..------.        .------..------..------..------.
|P.--. ||O.--. ||K.--. ||E.--. ||R.--. | .-.    |G.--. ||A.--. ||M.--. ||E.--. |
| :/\: || :/\: || :/\: || (\/) || :(): |((5))   | :/\: || (\/) || (\/) || (\/) |
| (__) || :\/: || :\/: || :\/: || ()() | '-.-.  | :\/: || :\/: || :\/: || :\/: |
| '--'P|| '--'O|| '--'K|| '--'E|| '--'R|  ((1)) | '--'G|| '--'A|| '--'M|| '--'E|
`------'`------'`------'`------'`------'   '-'  `------'`------'`------'`------'
        """)
        print("===============================================================================")
        print("Revelando Flop.")
        print()
        for valor, naipe in flop_cartas:
            carta_unicode = ""
            if naipe in Baralho.naipes_unicode:
                carta_unicode += Baralho.naipes_unicode[naipe]  # Obter o unicode do naipe
            else:
                carta_unicode += "N"  # Se o naipe não for encontrado, exibir "N"

            if valor == '10':
                carta_unicode += "10"  # Apenas adicionar o valor 10
            else:
                carta_unicode += valor
            print(carta_unicode)

        print()
        print("Iniciando novas apostas")
        print("===============================================================================")

    def revelar_turn(self):
        turn_carta = self.baralho.distribuir_carta()  # Distribui uma carta do baralho para o turn
        self.board.append(turn_carta)  # Adiciona a carta do turn ao tabuleiro
        print()
        print("===============================================================================")
        print(r"""
.------..------..------..------..------.        .------..------..------..------.
|P.--. ||O.--. ||K.--. ||E.--. ||R.--. | .-.    |G.--. ||A.--. ||M.--. ||E.--. |
| :/\: || :/\: || :/\: || (\/) || :(): |((5))   | :/\: || (\/) || (\/) || (\/) |
| (__) || :\/: || :\/: || :\/: || ()() | '-.-.  | :\/: || :\/: || :\/: || :\/: |
| '--'P|| '--'O|| '--'K|| '--'E|| '--'R|  ((1)) | '--'G|| '--'A|| '--'M|| '--'E|
`------'`------'`------'`------'`------'   '-'  `------'`------'`------'`------'
            """)
        print("===============================================================================")
        print("Revelando Turn.")
        print()
        for valor, naipe in self.board:
            carta_unicode = ""
            if naipe in Baralho.naipes_unicode:
                carta_unicode += Baralho.naipes_unicode[naipe]  # Obter o unicode do naipe
            else:
                carta_unicode += "N"  # Se o naipe não for encontrado, exibir "N"

            if valor == '10':
                carta_unicode += "10"  # Apenas adicionar o valor 10
            else:
                carta_unicode += valor
            print(carta_unicode)


    def revelar_river(self):
        river_carta = self.baralho.distribuir_carta()  # Distribui uma carta do baralho para o river
        self.board.append(river_carta)  # Adiciona a carta do river ao tabuleiro
        print()
        print("===============================================================================")
        print(r"""
.------..------..------..------..------.        .------..------..------..------.
|P.--. ||O.--. ||K.--. ||E.--. ||R.--. | .-.    |G.--. ||A.--. ||M.--. ||E.--. |
| :/\: || :/\: || :/\: || (\/) || :(): |((5))   | :/\: || (\/) || (\/) || (\/) |
| (__) || :\/: || :\/: || :\/: || ()() | '-.-.  | :\/: || :\/: || :\/: || :\/: |
| '--'P|| '--'O|| '--'K|| '--'E|| '--'R|  ((1)) | '--'G|| '--'A|| '--'M|| '--'E|
`------'`------'`------'`------'`------'   '-'  `------'`------'`------'`------'
            """)
        print("===============================================================================")
        print("Revelando River.")
        print()
        for valor, naipe in self.board:
            carta_unicode = ""
            if naipe in Baralho.naipes_unicode:
                carta_unicode += Baralho.naipes_unicode[naipe]  # Obter o unicode do naipe
            else:
                carta_unicode += "N"  # Se o naipe não for encontrado, exibir "N"

            if valor == '10':
                carta_unicode += "10"  # Apenas adicionar o valor 10
            else:
                carta_unicode += valor
            print(carta_unicode)

    def mostrar_vencedor(self):
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
.------..------..------..------..------..------..------..------.
|P.--. ||A.--. ||R.--. ||A.--. ||B.--. ||E.--. ||N.--. ||S.--. |
| :/\: || (\/) || :(): || (\/) || :(): || (\/) || :(): || :/\: |
| (__) || :\/: || ()() || :\/: || ()() || :\/: || ()() || :\/: |
| '--'P|| '--'A|| '--'R|| '--'A|| '--'B|| '--'E|| '--'N|| '--'S|
`------'`------'`------'`------'`------'`------'`------'`------'
            """)
        print("===============================================================================          ")
        melhores_maos = []
        for jogador in self.jogadores:
            if jogador.fichas > 0:
                todas_cartas = jogador.mao
                todas_cartas += self.board
                melhores_maos.append((self.classificar_mao(todas_cartas), jogador))

        melhor_mao = max(melhores_maos, key=lambda x: (x[0][0], x[0][1]))
        vencedores = [jogador for mao, jogador in melhores_maos if mao == melhor_mao[0]]

        for jogador in vencedores:
            print()
            print(f"O vencedor é {jogador.nome} com a mão {jogador.mostrar_mao()} e recebeu {self.pote} fichas como prêmio.")

        if len(vencedores) > 1:
            print("Empate entre: " + ", ".join([jogador.nome for jogador in vencedores]))
        else:
            print()

        for jogador in self.jogadores:
            if jogador.fichas > 0:
                print()
                print(f"{jogador.nome} tem {jogador.mostrar_mao()}")

        print()
        print(f"Cartas na mesa: {', '.join([self.baralho.naipes_unicode[naipe] + valor if valor != '10' else self.baralho.naipes_unicode[naipe] + valor for valor, naipe in self.board])}")
        print()

        # Remover jogadores sem fichas após cada rodada
        self.jogadores = [jogador for jogador in self.jogadores if jogador.fichas > 0]

        # Final do jogo: determinar o vencedor final
        jogador_vencedor = self.jogadores[0]
        print(f"O vencedor final é {jogador_vencedor.nome} com {jogador_vencedor.fichas} fichas!")



    def is_flush(self, cartas):
        naipes = [naipe for _, naipe in cartas]
        return len(set(naipes)) == 1

    def is_straight(self, cartas):
        valores = '23456789TJQKA'
        indices = []
        for valor, _ in cartas:
            if valor in valores:
                indices.append(valores.index(valor))
            else:
                # Se o valor da carta não estiver presente em valores, retornar False
                return False
        indices.sort()
        return all(indices[i] + 1 == indices[i + 1] for i in range(len(indices) - 1))


    def get_valor(self, cartas):
        valores = '23456789TJQKA'
        indices = []
        for valor, _ in cartas:
            if valor in valores:
                indices.append(valores.index(valor))
            else:
                # Se o valor da carta não estiver presente em valores, retornar False
                return False
        return sorted(indices, reverse=True)


    def contar_valores(self, cartas):
        valores = [valor for valor, _ in cartas]
        return Counter(valores)

    def classificar_mao(self, cartas):
        valores_contados = self.contar_valores(cartas)
        valores = sorted(valores_contados.values(), reverse=True)
        ordenacao_valores = sorted(valores_contados.keys(), key=lambda x: (valores_contados[x], x), reverse=True)
        flush = self.is_flush(cartas)
        straight = self.is_straight(cartas)
        valores_indices = self.get_valor(cartas)

        if straight and flush and ordenacao_valores[0] == 'A':
            return (10, valores_indices)  # Royal Flush
        elif straight and flush:
            return (9, valores_indices)  # Straight Flush
        elif valores == [4, 1]:
            return (8, valores_indices)  # Quadra
        elif valores == [3, 2]:
            return (7, valores_indices)  # Full House
        elif flush:
            return (6, valores_indices)  # Flush
        elif straight:
            return (5, valores_indices)  # Straight
        elif valores == [3, 1, 1]:
            return (4, valores_indices)  # Trinca
        elif valores == [2, 2, 1]:
            return (3, valores_indices)  # Dois Pares
        elif valores == [2, 1, 1, 1]:
            return (2, valores_indices)  # Par
        else:
            return (1, valores_indices)  # Carta Alta




