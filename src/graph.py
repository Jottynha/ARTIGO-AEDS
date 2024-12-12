import networkx as nx
import matplotlib.pyplot as plt

def get_genre_colors(jogos_vendas_por_regiao):
    genres = {genre for jogo in jogos_vendas_por_regiao for genre in jogo['generos']}
    genre_colors = {genre: plt.cm.tab20(i / len(genres)) for i, genre in enumerate(genres)}
    return genre_colors

def padronizar_generos(lista_generos):
    """
    Remove caracteres indesejados e normaliza os gêneros.
    Divide gêneros separados por vírgulas ou outros delimitadores.
    """
    generos_padronizados = []
    for genero in lista_generos:
        generos_divididos = genero.strip("[]").split(",")
        for g in generos_divididos:
            generos_padronizados.append(g.strip().lower())
    return generos_padronizados

def criar_grafo_com_genero_por_regiao(jogos_vendas, jogos_genero, limite_vendas_por_regiao, regiao):
    G = nx.Graph()
    jogos_vendas_por_regiao = []

    # Filtrar e combinar dados de vendas e gêneros
    for jogo_vendas in jogos_vendas:
        for jogo_genero in jogos_genero:
            if jogo_vendas['nome'].lower() == jogo_genero['titulo'].lower():
                vendas_regiao = jogo_vendas[f'{regiao.lower()}_sales']
                if vendas_regiao >= limite_vendas_por_regiao:
                    jogos_vendas_por_regiao.append({
                        'nome': jogo_vendas['nome'],
                        'vendas': vendas_regiao,
                        'generos': padronizar_generos([jogo_genero['genero']]),
                    })

    # Normalizar os gêneros e definir as cores
    genre_colors = get_genre_colors(jogos_vendas_por_regiao)

    # Remover duplicatas de jogos com base no nome
    jogos_vendas_por_regiao = list({jogo['nome']: jogo for jogo in jogos_vendas_por_regiao}.values())

    for i in range(3):
        # Ordenar e obter os jogos mais relevantes
        jogos_vendas_por_regiao.sort(key=lambda x: x['vendas'], reverse=True)
        top_30_jogos = [jogo['nome'] for jogo in jogos_vendas_por_regiao[:30]]

        max_vendas = max(jogo['vendas'] for jogo in jogos_vendas_por_regiao)
        min_vendas = min(jogo['vendas'] for jogo in jogos_vendas_por_regiao)

        # Definir tamanhos dos nós proporcionalmente às vendas
        node_sizes = {
            jogo['nome']: 100 + 900 * ((jogo['vendas'] - min_vendas) / (max_vendas - min_vendas))
            for jogo in jogos_vendas_por_regiao
        }

        G.clear()
        for jogo in jogos_vendas_por_regiao:
            G.add_node(jogo['nome'], vendas=jogo['vendas'], generos=jogo['generos'])

        # Conectar nós com gêneros em comum
        for jogo1, dados1 in G.nodes(data=True):
            for jogo2, dados2 in G.nodes(data=True):
                if jogo1 != jogo2:
                    generos1 = set(dados1['generos'])
                    generos2 = set(dados2['generos'])
                    if generos1.intersection(generos2):
                        G.add_edge(jogo1, jogo2)

        # Destacar conexões entre os 30 principais jogos
        for jogo1 in top_30_jogos:
            for jogo2 in top_30_jogos:
                if jogo1 != jogo2 and not G.has_edge(jogo1, jogo2):
                    G.add_edge(jogo1, jogo2, color='red', weight=2)

        # Desenhar o grafo
        plt.figure(figsize=(18, 18))
        pos = nx.spring_layout(G, k=2.5, iterations=100)

        # Colorir nós com base nos gêneros
        for jogo, data in G.nodes(data=True):
            node_colors = [genre_colors[genre] for genre in data['generos'] if genre in genre_colors]
            nx.draw_networkx_nodes(
                G,
                pos,
                nodelist=[jogo],
                node_size=node_sizes[jogo],
                node_color=node_colors[0] if node_colors else 'gray',
            )

        # Desenhar arestas
        edges = G.edges(data=True)
        red_edges = [(u, v) for u, v, attr in edges if attr.get('color') == 'red']
        other_edges = [(u, v) for u, v, attr in edges if attr.get('color') != 'red']

        nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='red', width=2, alpha=0.8)
        nx.draw_networkx_edges(G, pos, edgelist=other_edges, edge_color='black', alpha=0.5)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")

        # Legenda dos gêneros
        handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=genre)
                   for genre, color in genre_colors.items()]
        plt.legend(handles=handles, loc="upper right", fontsize=10, title="Gêneros")

        plt.title(f"Grafo de Jogos por Gênero - Região {regiao} - Iteração {i+1}", fontsize=16)
        plt.show()

        # Atualizar a lista para próxima iteração
        cutoff = int(len(jogos_vendas_por_regiao) * 0.4)  # Remove os 40% menos relevantes
        jogos_vendas_por_regiao = jogos_vendas_por_regiao[:-cutoff]

    return G
