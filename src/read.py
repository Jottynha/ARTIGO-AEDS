import csv

def normalizar_genero(genero):
    """
    Normaliza o gênero para padronização.
    Remove espaços extras e converte para letras minúsculas.
    """
    return genero.strip().lower() if genero else "desconhecido"

def ler_arquivo_vendas_csv(nome_arquivo):
    """
    Lê o arquivo de vendas e retorna uma lista de jogos com os gêneros normalizados.
    """
    jogos = []
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        next(leitor)  # Ignora o cabeçalho
        for linha in leitor:
            rank, nome, plataforma, ano, genero, publisher, na_sales, eu_sales, jp_sales, other_sales, global_sales = linha
            jogos.append({
                'nome': nome.strip(),
                'plataforma': plataforma.strip(),
                'genero': normalizar_genero(genero),
                'na_sales': float(na_sales),
                'eu_sales': float(eu_sales),
                'jp_sales': float(jp_sales),
                'other_sales': float(other_sales),
                'global_sales': float(global_sales),
            })
    return jogos

def ler_arquivo_games_csv(nome_arquivo, jogos_vendas):
    """
    Lê o arquivo de games e retorna uma lista de jogos.
    Se um jogo não tiver gênero na lista de games, ele utiliza o gênero da lista de vendas.
    """
    jogos = []
    # Cria um dicionário para mapear os nomes aos gêneros de jogos_vendas
    mapeamento_generos = {jogo['nome']: jogo['genero'] for jogo in jogos_vendas}

    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        next(leitor)  # Ignora o cabeçalho
        for linha in leitor:
            _, title, release_date, team, rating, times_listed, num_reviews, genres, summary, reviews, plays, playing, backlogs, wishlist = linha
            
            # Verifica se há gêneros no arquivo atual
            genero = normalizar_genero(genres) if genres.strip() else None
            
            # Caso não tenha gênero, usa o gênero de jogos_vendas
            if not genero or genero == "desconhecido":
                genero = mapeamento_generos.get(title.strip(), "desconhecido")
            
            jogos.append({
                'titulo': title.strip(),
                'genero': genero,
                'data_lancamento': release_date.strip(),
                'equipe': team.strip(),
                'classificacao': rating.strip(),
                'generos': genero,  # Normalizado ou preenchido
            })
    return jogos
