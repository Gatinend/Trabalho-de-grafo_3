class VariavelLimitada:
    def __init__(self, maximo):
        # Define o valor máximo que essa variável pode ter
        self.maximo = maximo
        
        # Define o valor mínimo (padrão: zero)
        self.minimo = 0
        
        # Valor atual da variável, começa com o valor máximo
        self._valor = maximo

    @property
    def valor(self):
        # Getter: retorna o valor atual da variável
        return self._valor

    @valor.setter
    def valor(self, novo_valor):
        # Setter: define o novo valor da variável, garantindo que esteja dentro dos limites
        # Usa min/max para "travar" dentro dos limites definidos
        self._valor = max(self.minimo, min(self.maximo, novo_valor))

    def definir_minimo(self, novo_minimo):
        # Atualiza o valor mínimo permitido
        self.minimo = novo_minimo
        
        # Se o valor atual estiver abaixo do novo mínimo, ajusta para o mínimo
        if self._valor < self.minimo:
            self._valor = self.minimo

    def __str__(self):
        # Representação em string: mostra valor atual, máximo e mínimo
        return f"{self.valor}/{self.maximo} (mín: {self.minimo})"
    
    def definir_maximo(self, novo_maximo):
        # Atualiza o valor máximo permitido
        self.maximo = novo_maximo

        # Se o valor atual estiver acima do novo máximo, ajusta para o máximo
        if self._valor > self.maximo:
            self._valor = self.maximo