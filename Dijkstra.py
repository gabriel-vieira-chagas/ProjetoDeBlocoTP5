import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

distancias = np.array([
    [0, 10, 5, 7, 3, 2],
    [10, 0, 8, 1, 4, 9],
    [5, 8, 0, 2, 1, 3],
    [7, 1, 2, 0, 5, 6],
    [3, 4, 1, 5, 0, 4],
    [2, 9, 3, 6, 4, 0]
])

nos = ['A', 'B', 'C', 'D', 'E', 'F']


def dijkstra(matriz, origem):
    n = len(matriz)
    dist = [float('inf')] * n
    dist[origem] = 0
    visto = [False] * n
    anterior = [-1] * n

    for _ in range(n):
        menor = float('inf')
        idx_menor = -1
        for i in range(n):
            if not visto[i] and dist[i] < menor:
                menor = dist[i]
                idx_menor = i

        if idx_menor == -1:
            break

        visto[idx_menor] = True

        for v in range(n):
            peso = matriz[idx_menor][v]
            if peso > 0 and not visto[v]:
                nova_dist = dist[idx_menor] + peso
                if nova_dist < dist[v]:
                    dist[v] = nova_dist
                    anterior[v] = idx_menor

    return dist, anterior


def reconstruir_caminhos(anterior, origem):
    caminhos = {}
    n = len(anterior)
    for i in range(n):
        if i == origem:
            caminhos[i] = [origem]
            continue
        path = []
        atual = i
        while atual != -1:
            path.append(atual)
            atual = anterior[atual]
        path.reverse()
        caminhos[i] = path
    return caminhos


def montar_arvore(anterior, matriz):
    G = nx.Graph()
    n = len(anterior)
    for i in range(n):
        G.add_node(nos[i])
    for i in range(n):
        if anterior[i] != -1:
            w = int(matriz[anterior[i]][i])
            G.add_edge(nos[anterior[i]], nos[i], weight=w)
    return G


inicio = 0
distancias_minimas, anteriores = dijkstra(distancias, inicio)
caminhos = reconstruir_caminhos(anteriores, inicio)
arvore = montar_arvore(anteriores, distancias)

print("===================== RESULTADOS DO ALGORITMO DE DIJKSTRA =====================\n")
print(f"Cidade de origem: {nos[inicio]}\n")

print("Distancia mais curtas a partir de A: ")
for i, cidade in enumerate(nos):
    print(f"{nos[inicio]} -> {cidade}: {distancias_minimas[i]}")

print("\nCaminhos mais curtos: ")
for i, cidade in enumerate(nos):
    caminho_str = ' -> '.join([nos[n] for n in caminhos[i]])
    print(f"{nos[inicio]} -> {cidade}: {caminho_str}")

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
pos_tree = nx.spring_layout(arvore)
labels_tree = nx.get_edge_attributes(arvore, 'weight')
nx.draw(arvore, pos_tree, with_labels=True, node_size=800,
        node_color='lightblue', font_size=12, font_weight='bold')
nx.draw_networkx_edge_labels(arvore, pos_tree, edge_labels=labels_tree)
plt.title('Arvore Geradora | Caminhos Mais Curtos a partir de A')

plt.subplot(1, 2, 2)
grafo_total = nx.Graph()
n = len(nos)
for i in range(n):
    for j in range(i + 1, n):
        if distancias[i][j] > 0:
            peso = int(distancias[i][j])
            grafo_total.add_edge(nos[i], nos[j], weight=peso)
pos_total = nx.spring_layout(grafo_total)
labels_total = nx.get_edge_attributes(grafo_total, 'weight')
nx.draw(grafo_total, pos_total, with_labels=True, node_size=800,
        node_color='lightgreen', font_size=12, font_weight='bold')
nx.draw_networkx_edge_labels(grafo_total, pos_total, edge_labels=labels_total)
plt.title('Grafo Completo | Todas as Conexões')

plt.tight_layout()
plt.show()

print("\n===================== INFORMAÇÕES DA ARVORE GERADORA =====================")
print(f"Numero de arestas na arvore: {arvore.number_of_edges()}")
print(f"Numero de nós na arvore: {arvore.number_of_nodes()}")
print(f"Arestas da arvore geradora: {list(arvore.edges(data=True))}")