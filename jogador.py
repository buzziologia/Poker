class Jogador:
  def __init__(self, nome, fichas=1000):
      self.nome = nome
      self.fichas = fichas
      self.mao = []
      self.aposta_atual = 0

  def receber_carta(self, carta):
      self.mao.append(carta)

  def mostrar_mao(self):
      mao_unicode = ""
      for valor, naipe in self.mao:
          carta_unicode = ""
          if naipe in Baralho.naipes_unicode:
              carta_unicode += Baralho.naipes_unicode[naipe]  # Obter o unicode do naipe
          else:
              carta_unicode += "N"  # Se o naipe não for encontrado, exibir "N"

          if valor == '10':
              carta_unicode += "10"  # Apenas adicionar o valor 10
          else:
              carta_unicode += valor
          mao_unicode += carta_unicode + " "
      return mao_unicode

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
