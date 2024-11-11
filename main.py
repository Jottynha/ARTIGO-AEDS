import csv
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.colors as mcolors
import random

# Função para ler o arquivo CSV de vendas de jogos
def ler_arquivo_vendas_csv(nome_arquivo):
    jogos = []
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        next(leitor)  # Pula o cabeçalho
        for linha in leitor:
            rank, nome, plataforma, ano, genero, publisher, na_sales, eu_sales, jp_sales, other_sales, global_sales = linha
            jogos.append({
                'nome': nome,
                'plataforma': plataforma,
                'na_sales': float(na_sales),
                'eu_sales': float(eu_sales),
                'jp_sales': float(jp_sales),
                'other_sales': float(other_sales),
                'global_sales': float(global_sales),
            })
    return jogos

# Função para ler o arquivo CSV de gêneros de jogos
def ler_arquivo_games_csv(nome_arquivo):
    jogos = []
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        next(leitor)  # Pula o cabeçalho
        for linha in leitor:
            _, title, release_date, team, rating, times_listed, num_reviews, genres, summary, reviews, plays, playing, backlogs, wishlist = linha
            jogos.append({
                'titulo': title,
                'generos': genres.split(','),  # Transforma os gêneros em uma lista
            })
    return jogos

def get_genre_colors(jogos_vendas_por_regiao):
    genres = {genre for jogo in jogos_vendas_por_regiao for genre in jogo['generos']}
    genre_colors = {genre: plt.cm.tab20(i) for i, genre in enumerate(genres)}
    return genre_colors

def criar_grafo_com_genero_por_regiao(jogos_vendas, jogos_genero, limite_vendas_por_regiao, regiao):
    G = nx.Graph()
    jogos_vendas_por_regiao = []

    # Filtra os jogos por região com vendas acima do limite e adiciona os gêneros
    for jogo_vendas in jogos_vendas:
        for jogo_genero in jogos_genero:
            if jogo_vendas['nome'].lower() == jogo_genero['titulo'].lower():  # Verifica correspondência de títulos
                vendas_regiao = jogo_vendas[f'{regiao.lower()}_sales']
                if vendas_regiao >= limite_vendas_por_regiao:
                    jogos_vendas_por_regiao.append({
                        'nome': jogo_vendas['nome'],
                        'vendas': vendas_regiao,
                        'generos': jogo_genero['generos'],
                    })
    
    # Assign unique colors to each genre
    genre_colors = get_genre_colors(jogos_vendas_por_regiao)

    # Remove iterativamente os 20 jogos que menos venderam e cria o grafo em três iterações
    for i in range(3):
        # Ordena os jogos por vendas (decrescente) e seleciona os top 15 jogos restantes
        jogos_vendas_por_regiao.sort(key=lambda x: x['vendas'], reverse=True)
        top_15_jogos = [jogo['nome'] for jogo in jogos_vendas_por_regiao[:15]]

        # Adiciona nós para os jogos no grafo
        G.clear()  # Limpa o grafo antes de redesenhá-lo
        for jogo in jogos_vendas_por_regiao:
            G.add_node(jogo['nome'], vendas=jogo['vendas'], generos=jogo['generos'])

        # Conecta os jogos que compartilham pelo menos um gênero
        for jogo1, dados1 in G.nodes(data=True):
            for jogo2, dados2 in G.nodes(data=True):
                if jogo1 != jogo2:
                    generos1 = set(dados1['generos'])
                    generos2 = set(dados2['generos'])
                    if generos1.intersection(generos2):  # Verifica se têm gêneros em comum
                        G.add_edge(jogo1, jogo2)

        # Plotting with unique genre colors
        pos = nx.spring_layout(G, k=0.1, iterations=50)  # Adjust layout

        for jogo, data in G.nodes(data=True):
            node_color = [genre_colors[genre] for genre in data['generos'] if genre in genre_colors]
            # If multiple genres exist, use the first color as primary for node
            nx.draw_networkx_nodes(G, pos, nodelist=[jogo], node_size=100, node_color=node_color[0])

        # Draw edges and labels
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")

        plt.title(f"Grafo de Jogos por Gênero - Região {regiao} - Iteração {i+1}", fontsize=16)
        plt.show()

        # Remove os 200 jogos com menos vendas para a próxima iteração
        jogos_vendas_por_regiao = jogos_vendas_por_regiao[:-200]

    return G, top_15_jogos

# Função principal atualizada para gerar o grafo por região
def main():
    limite_vendas_regiao = 0.5  # Define o limite mínimo de vendas para a região
    regioes = ['NA', 'EU', 'JP', 'Other']
    
    # Carregar os dados de vendas e gêneros
    jogos_vendas = ler_arquivo_vendas_csv('vgsales.csv')
    jogos_genero = ler_arquivo_games_csv('games.csv')
    
    for regiao in regioes:
        # Criar o grafo associando os gêneros ao sucesso na região específica
        criar_grafo_com_genero_por_regiao(jogos_vendas, jogos_genero, limite_vendas_regiao, regiao)

# Executa o programa principal
if __name__ == "__main__":
    main()
