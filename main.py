import random
from collections import Counter

class Baralho:
    naipes = ['Copas', 'Ouros', 'Paus', 'Espadas']
    valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cartas = [(valor, naipe) for naipe in self.naipes for valor in self.valores]
        random.shuffle(self.cartas)

    def distribuir_carta(self):
        return self.cartas.pop()

class Jogador:
    def __init__(self, nome, fichas=1000):
        self.nome = nome
        self.fichas = fichas
        self.mao = []
        self.aposta_atual = 0

    def receber_carta(self, carta):
        self.mao.append(carta)

    def mostrar_mao(self):
        return self.mao

    def apostar(self, quantidade):
        if quantidade > self.fichas:
            raise ValueError(f"{self.nome} não tem fichas suficientes para apostar {quantidade}.")
        self.fichas -= quantidade
        self.aposta_atual += quantidade
        return quantidade

    def igualar_aposta(self, maior_aposta):
        quantidade = maior_aposta - self.aposta_atual
        self.apostar(quantidade)
        return quantidade

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

    def distribuir_cartas_iniciais(self):
        for _ in range(2):
            for jogador in self.jogadores:
                carta = self.baralho.distribuir_carta()
                jogador.receber_carta(carta)
                if len(jogador.mao) == 2:
                    self.board.append(jogador.mao[-1])

    def visualizar_cartas(self):
        print()
        print("Bem vindo ao jogo, suas cartas foram distribuidas, por favor, aguarde...")
        for jogador in self.jogadores:
            print()
            senha = input(f"Informe a senha para {jogador.nome} visualizar sua carta: ")
            print(f"{jogador.nome} sua carta é: {jogador.mao}")
            print(f"{jogador.nome} tem {jogador.fichas} fichas.")
            print("Por favor, decore suas cartas e prossiga as instruções...")
            opcao = 0
            while True:
                try:
                    opcao = input("Sair: [s] ou Continuar: [c]: ")
                    if opcao.lower() == 's':
                        print('\n' * 15) # intencionalmente vazio para separar as cartas
                        break
                    else:
                        print(f"{jogador.nome} sua carta é: {jogador.mao}")
                        print(f"{jogador.nome} tem {jogador.fichas} fichas.")
                        print("Por favor, decore suas cartas e prossiga as instruções...")
                        opcao = 0
                except ValueError:
                    print("Senha incorreta. Acesso negado.")
            

    def primeira_rodada_apostas(self):
        self.pote += self.jogadores[(self.dealer_pos + 1) % len(self.jogadores)].apostar(self.aposta_minima // 2)
        self.pote += self.jogadores[(self.dealer_pos + 2) % len(self.jogadores)].apostar(self.aposta_minima)
        self.maior_aposta = self.aposta_minima
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
            acao = input(f"{jogador.nome}, selecione sua ação (apostar/igualar/apassar): ")
            if acao == 'apostar':
                aposta = int(input(f"Qual o valor da sua aposta? (mínimo {self.maior_aposta}): "))
                self.pote += jogador.apostar(aposta)
                self.maior_aposta = max(self.maior_aposta, aposta)
            elif acao == 'igualar':
                self.pote += jogador.igualar_aposta(self.maior_aposta)
            else:
                pass
        else:
            passs

    def revelar_flop(self):
        self.board.extend([self.baralho.distribuir_carta() for _ in range(3)])
        print(f"Flop: {self.board}")

    def revelar_turn(self):
        self.board.append(self.baralho.distribuir_carta())
        print(f"Turn: {self.board}")

    def revelar_river(self):
        self.board.append(self.baralho.distribuir_carta())
        print(f"River: {self.board}")

    def mostrar_vencedor(self):
        melhores_maos = []
        for jogador in self.jogadores:
            todas_cartas = jogador.mostrar_mao() + self.board
            melhores_maos.append((self.classificar_mao(todas_cartas), jogador))

        melhor_mao = max(melhores_maos, key=lambda x: x[0])
        vencedores = [jogador for mao, jogador in melhores_maos if mao == melhor_mao[0]]

        for jogador in vencedores:
            print(f"O vencedor é {jogador.nome} com a mão {jogador.mostrar_mao()} e recebeu {self.pote} fichas como prêmio.")

        if len(vencedores) > 1:
            print("Empate entre: " + ", ".join([jogador.nome for jogador in vencedores]))
        else:
            print(f"O vencedor é {vencedores[0].nome} com a mão {vencedores[0].mostrar_mao()}")

        for jogador in self.jogadores:
            print(f"{jogador.nome} tem {jogador.mostrar_mao()}")
        print(f"Cartas na mesa: {self.board}")

    def is_flush(self, cartas):
        naipes = [naipe for _, naipe in cartas]
        return len(set(naipes)) == 1

    def is_straight(self, cartas):
        valores = '23456789TJQKA'
        indices = [valores.index(valor) for valor, _ in cartas]
        indices.sort()
        return all(indices[i] + 1 == indices[i + 1] for i in range(len(indices) - 1))

    def get_valor(self, cartas):
        valores = '23456789TJQKA'
        return sorted([valores.index(valor) for valor, _ in cartas], reverse=True)

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
            return (8, ordenacao_valores)  # Quadra
        elif valores == [3, 2]:
            return (7, ordenacao_valores)  # Full House
        elif flush:
            return (6, valores_indices)  # Flush
        elif straight:
            return (5, valores_indices)  # Straight
        elif valores == [3, 1, 1]:
            return (4, ordenacao_valores)  # Trinca
        elif valores == [2, 2, 1]:
            return (3, ordenacao_valores)  # Dois Pares
        elif valores == [2, 1, 1, 1]:
            return (2, ordenacao_valores)  # Par
        else:
            return (1, valores_indices)  # Carta Alta

    def iniciar_jogo(self):
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

if __name__ == "__main__":
    print()
    print("Bem-vindo ao Poker!")
    print()
    quant_jogadores = int(input("Digite o número de jogadores (2-9): "))
    jogadores = []
    senhas = []
    for i in range(quant_jogadores):
        print()
        nome = input(f"Digite o nome do jogador {i+1}: ")
        senha = input(f"Informe a senha para {nome}: ")
        jogadores.append(nome)
        senhas.append(senha)
    jogo = Poker(jogadores, senhas)
    jogo.iniciar_jogo()
