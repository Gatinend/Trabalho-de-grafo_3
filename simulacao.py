import time
from collections import deque

from caminhoes import Caminhao
from grafo import Grafo
from no import Arvore

# 1) Monta o grafo e lê arquivos


G = Grafo()
G.ler_vertices("vertices.txt")
G.ler_arestas("aresta.txt")
G.mostrar_grafo_detalhado()

# 2) Pergunta ao usuário onde começa o fogo
inicio = input("Escolha um vértice para começar o fogo: ").strip()
if inicio not in G.nos or not isinstance(G.nos[inicio], Arvore):
    raise ValueError(f"{inicio} não é uma árvore válida no grafo.")

# 3) Inicializa set de ativos (árvores que estão queimando)
ativos = set([inicio])
fila = deque([inicio])

no0 = G.nos[inicio]
no0.queimando = True
no0.tempo_queima = 0
# potência_restante deve existir em Arvore; se for VariavelLimitada, use .valor
no0.potencia_restante = no0.potencia_queima.valor  

# 4) Configura caminhões
qtd = int(input("Quantos caminhões por posto de brigadista? "))
cap = int(input("Capacidade de água dos caminhões: "))
caminhoes = []
for i in range(qtd):
    print(f"\n--- Caminhão {i+1} ---")
    nome = input("  Nome: ").strip()
    pos = input("  Posição inicial: ").strip()
    if pos not in G.nos:
        raise ValueError(f"{pos} não existe no grafo.")
    cam = Caminhao(nome=nome, posicao=pos, capacidade=cap)
    caminhoes.append(cam)

# 5) Loop de simulação
tempo = 0
while ativos:
    print(f"\n--- Tempo {tempo} ---")
    novos = []

    # 5.1) Propaga fogo
    for nome in list(ativos):
        no = G.nos[nome]
        print(f"Árvore {nome} queima; potência restante: {no.potencia_restante}")

        # reduz potência
        no.potencia_restante -= 1

        # se acabou a potência
        if no.potencia_restante <= 0:
            print(f"Árvore {nome} totalmente queimada!")
            no.queimando = False
            no.set_estado_final("queimado")
            ativos.remove(nome)
            continue

        # espalha para vizinhos
        # se adjacentes for dict, iterar .items(); se for lista, usar o que estiver definido
        
        for viz_nome, peso in no.adjacentes:
            viz = G.nos[viz_nome]
            if (
                isinstance(viz, Arvore) 
                and not viz.queimando 
                and viz._estado_final is None  # ← Aqui está a proteção contra reacender
            ):
                tempo_queimando = tempo - no.tempo_queima
                if tempo_queimando >= (peso // 2):
                    print(f"Fogo se espalhou de {nome} para {viz_nome}")
                    viz.queimando = True
                    viz.tempo_queima = tempo
                    viz.potencia_restante = viz.potencia_queima.valor
                    novos.append(viz_nome)
            else:
                if isinstance(viz, Arvore):
                    print(f"{viz_nome} já foi {viz._estado_final} e não pode queimar de novo.")

    ativos.update(novos)

    # 5.2) Atualiza movimento de cada caminhão
    for cam in caminhoes:
        cam.atualizar_movimento(G, caminhoes, ativos)

    tempo += 1
    time.sleep(1)  # opcional: pausa de 1s entre passos

# 6) Relatório final
apagados = [n for n,no in G.nos.items() if isinstance(no, Arvore) and no._estado_final=="apagado"]
queimados = [n for n,no in G.nos.items() if isinstance(no, Arvore) and no._estado_final=="queimado"]

print("\nNós salvos (apagados):")
for n in apagados:
    print(f" - {n}")

print("\nNós perdidos (queimados):")
for n in queimados:
    print(f" - {n}")

print(f"\nDuração total da simulação: {tempo} unidades de tempo")