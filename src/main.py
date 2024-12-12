import read
import pdf
import interface



def main():
    """
    Função Principal
    """
    limite_vendas_regiao = 1.4  # MÍNIMO DE VENDAS
    regioes = ['NA', 'EU', 'JP', 'Other']
    jogos_vendas = read.ler_arquivo_vendas_csv('dataset/vgsales.csv')
    jogos_genero = read.ler_arquivo_games_csv('dataset/games.csv')
    interface.iniciar_interface(
        regioes,
        jogos_vendas,
        jogos_genero,
        limite_vendas_regiao,
        pdf.gerar_relatorio
    )

if __name__ == "__main__":
    main()
