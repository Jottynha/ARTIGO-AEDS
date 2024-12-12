import csv

def ler_arquivo_vendas_csv(nome_arquivo):
    jogos = []
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        next(leitor) 
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

def ler_arquivo_games_csv(nome_arquivo):
    jogos = []
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        next(leitor) 
        for linha in leitor:
            _, title, release_date, team, rating, times_listed, num_reviews, genres, summary, reviews, plays, playing, backlogs, wishlist = linha
            jogos.append({
                'titulo': title,
                'generos': genres.split(','),  # Transforma os gêneros em uma lista
            })
    return jogos