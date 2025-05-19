import heapq

def dijkstra_completo(grafo, origem):
    dist = {no: float('inf') for no in grafo}
    pai = {no: None for no in grafo}
    dist[origem] = 0

    heap = [(0, origem)]  # (distância, vértice)

    while heap:
        atual_dist, u = heapq.heappop(heap)

        if atual_dist > dist[u]:
            continue

        for v, peso in grafo[u]:
            if dist[u] + peso < dist[v]:
                dist[v] = dist[u] + peso
                pai[v] = u
                heapq.heappush(heap, (dist[v], v))

    return dist, pai

def dijkstra_tempo(grafo, origem, destino):
    dist, _ = dijkstra_completo(grafo, origem)
    return dist.get(destino, float('inf'))

def dijkstra_trajeto(grafo, origem, destino):
    _, pai = dijkstra_completo(grafo, origem)
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = pai[atual]
    caminho = caminho[::-1]  # Inverte o caminho
    
    if not caminho or caminho[0] != origem:
        return []  # caminho não válido
    return caminho


