
from extras import VariavelLimitada


class No:
    def __init__(self, nome):
        self.nome = nome
        self.adjacentes = []  # (vizinho, peso)

    def adicionar_vizinho(self, vizinho, peso):
        self.adjacentes.append((vizinho, peso))


class Agua(No):
    def __init__(self, nome):
        super().__init__(nome)
        self.reabastece = True
        self.adjacentes = [] 


class Arvore(No):
    def __init__(self, nome, potencia_queima):
        # Inicializa apenas com o nome
        super().__init__(nome)
        # Potência de queima como VariavelLimitada
        self.potencia_queima    = VariavelLimitada(potencia_queima)
        self.potencia_restante  = self.potencia_queima.valor
        self.tempo_queima       = None
        self._queimando         = False
        self._estado_final      = None
        # adjacentes já herdado de No

    @property
    def queimando(self):
        return self._queimando

    @queimando.setter
    def queimando(self, valor):
        """
        Controla a transição de estado de queima:
        - Sempre permite apagar (True -> False).
        - Só permite iniciar queima (False -> True) se não tiver estado final.
        """
        if valor is False:
            # Sempre permite apagar
            self._queimando = False
        else:  # valor is True
            if self._estado_final is None:
                # Permite iniciar queima apenas se sem estado final
                self._queimando = True
            else:
                # Não permite reacender após ter estado final
                motivo = self._estado_final
                print(f"{self.nome} já foi {motivo} e não pode queimar de novo.")

    def set_estado_final(self, motivo):
        """Define o motivo final do estado, 'apagado' ou 'queimado'."""
        if motivo in ("apagado", "queimado"):
            self._estado_final = motivo
        else:
            raise ValueError("Motivo deve ser 'apagado' ou 'queimado'")


class Brigadista(No):
    def __init__(self, nome):
        super().__init__(nome)
        self.adjacentes = [] 
        self.reabastece = True
        