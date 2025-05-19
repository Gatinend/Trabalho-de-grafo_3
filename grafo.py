
from no import Brigadista, Agua, Arvore

class Grafo:
    def __init__(self):
        self.nos = {}  # mapeia nome (str) -> objeto No

    def adicionar_no(self, nome, tipo, potencia):
        if nome not in self.nos:
            if tipo == 0:
                self.nos[nome] = Brigadista(nome)
            elif tipo == 1:
                self.nos[nome] = Agua(nome)
            elif tipo == 2:
                self.nos[nome] = Arvore(nome, potencia)

    def adicionar_aresta(self, origem, destino, peso):
        if origem in self.nos and destino in self.nos:
            self.nos[origem].adicionar_vizinho(destino, peso)
            self.nos[destino].adicionar_vizinho(origem, peso)

    def ler_vertices(self, caminho_arquivo):
        """
        Cada linha: NOME POTENCIA TIPO
        """
        with open(caminho_arquivo, 'r') as f:
            for linha in f:
                partes = linha.strip().split()
                if len(partes) != 3:
                    continue
                nome, pot_str, tipo_str = partes
                potencia = int(pot_str)
                tipo     = int(tipo_str)

                # Só árvores usam a potência real
                if tipo == 2:
                    self.adicionar_no(nome, tipo, potencia)
                else:
                    self.adicionar_no(nome, tipo, 0)

    def ler_arestas(self, caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            for linha in f:
                partes = linha.strip().split()
                if len(partes) != 3:
                    continue
                origem, destino, peso_str = partes
                peso = int(peso_str)
                self.adicionar_aresta(origem, destino, peso)
                
    def mostrar_grafo_detalhado(self):
        """
        Mostra cada nó, seu tipo, estado e vizinhos com pesos.
        """
        print("\n=== Nós do Grafo ===")
        for nome, no in self.nos.items():
            tipo = type(no).__name__
            info = ""
            if isinstance(no, Arvore):
                fogo = "🔥" if no.queimando else "🌳"
                info = f" | Potência: {no.potencia_queima.valor} | Queimando: {no.queimando}"
                tipo += f" {fogo}"
            elif isinstance(no, Brigadista):
                tipo += " 💧"
            elif isinstance(no, Agua):
                tipo += " 💦"
            print(f"{nome} [{tipo}]{info}")
            for viz, peso in no.adjacentes:
                print(f"  └─ {viz} (peso {peso})")

                
    def get_dict_adjacencia(self):
        """
        Retorna o grafo no formato de dicionário de adjacência:
        {
            "A": [("B", 3), ("C", 1)],
            "B": [("C", 2)],
            ...
        }
        """
        return {nome: no.adjacentes[:] for nome, no in self.nos.items()}