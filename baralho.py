class Baralho:
  naipes_unicode = {
      'Espadas': '\u2660',
      'Copas': '\u2665',
      'Ouros': '\u2666',
      'Paus': '\u2663'
  }

  naipes = ['Copas', 'Ouros', 'Paus', 'Espadas']
  valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

  def __init__(self):
      self.cartas = [(valor, naipe) for naipe in self.naipes for valor in self.valores]
      random.shuffle(self.cartas)

  def distribuir_carta(self):
      return self.cartas.pop()

  def imprimir_naipe(nome_naipe):
      codigo_unicode = naipes_unicode.get(nome_naipe)
      if codigo_unicode:
          print(codigo_unicode)
      else:
          print("Naipe não encontrado.")

