import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

matriz = np.array([
    [0, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    [20, 0, 40, 50, 60, 70, 80, 90, 100, 120],
    [30, 40, 0, 60, 70, 80, 90, 100, 110, 120],
    [40, 50, 60, 0, 80, 90, 100, 110, 120, 130],
    [50, 60, 70, 80, 0, 100, 110, 120, 130, 140],
    [60, 70, 80, 90, 100, 0, 120, 130, 140, 150],
    [70, 80, 90, 100, 110, 120, 0, 140, 150, 160],
    [80, 90, 100, 110, 120, 130, 140, 0, 160, 170],
    [90, 100, 110, 120, 130, 140, 150, 160, 0, 180],
    [100, 110, 120, 130, 140, 150, 160, 170, 180, 0]
])

locais = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']


def greedy_nearest(matriz_distancias, inicio):
    n = len(matriz_distancias)
    seen = [False] * n
    route = [inicio]
    seen[inicio] = True
    total = 0

    print("==== ROTEAMENTO: HEURÍSTICA DO VIZINHO MAIS PRÓXIMO ====")
    print(f"Ponto de partida: {locais[inicio]}")
    print("\nSequência construída:")

    atual = inicio
    for step in range(n - 1):
        best_dist = float('inf')
        best_neighbor = -1

        for neighbor in range(n):
            if not seen[neighbor] and matriz_distancias[atual][neighbor] < best_dist:
                best_dist = matriz_distancias[atual][neighbor]
                best_neighbor = neighbor

        route.append(best_neighbor)
        seen[best_neighbor] = True
        total += best_dist

        print(f"Passo {step + 1}: {locais[atual]} -> {locais[best_neighbor]} (km: {best_dist})")

        atual = best_neighbor

    back_dist = matriz_distancias[route[-1]][inicio]
    total += back_dist
    route.append(inicio)

    print(f"Retorno ao início: {locais[route[-2]]} -> {locais[inicio]} (km: {back_dist})")

    return route, total


def draw_route(route, matriz_distancias):
    G = nx.Graph()
    for l in locais:
        G.add_node(l)

    for i in range(len(route) - 1):
        src = locais[route[i]]
        dst = locais[route[i + 1]]
        w = matriz_distancias[route[i]][route[i + 1]]
        G.add_edge(src, dst, weight=w)

    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='lightcoral')
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    edges = list(G.edges())
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=2, edge_color='orange', alpha=0.8)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title('Rota obtida pela heurística')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    x = list(range(len(route)))
    y = [0] * len(route)
    plt.plot(x, y, 's-', linewidth=3, markersize=9)
    for i, idx in enumerate(route):
        plt.text(i, 0.05, locais[idx], ha='center', va='bottom', fontsize=12, fontweight='bold')
    for i in range(len(route) - 1):
        d = matriz_distancias[route[i]][route[i + 1]]
        xm = (i + i + 1) / 2
        plt.text(xm, -0.05, f'{d}', ha='center', va='top', fontsize=10,
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8))
    plt.title('Ordem de visita')
    plt.xlabel('Posição na rota')
    plt.yticks([])
    plt.grid(visible=True, alpha=0.25)
    plt.tight_layout()
    plt.show()


start_city = 0
rota, distancia_total = greedy_nearest(matriz, start_city)

print("\n==== RESUMO DA ROTA CALCULADA ====\n")
rota_nomes = [locais[i] for i in rota]
print("Sequência final:", ' -> '.join(rota_nomes))
print(f"Distância total (km): {distancia_total}")

print("\nTrechos detalhados:")
for i in range(len(rota) - 1):
    o = rota[i]
    d = rota[i + 1]
    trecho = matriz[o][d]
    print(f"  {locais[o]} -> {locais[d]} : {trecho} km")

draw_route(rota, matriz)