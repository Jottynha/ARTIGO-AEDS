import tkinter as tk
from tkinter import messagebox
import graph

def processar_regiao(jogos_vendas, jogos_genero, limite_vendas_regiao, regiao):
    """
    Processa os dados para uma região específica.
    """
    estatisticas = graph.criar_grafo_com_genero_por_regiao(
        jogos_vendas, jogos_genero, limite_vendas_regiao, regiao
    )
    return {
        "top_15": estatisticas["top_15"],
        "num_conexoes": estatisticas["num_conexoes"],
        "genero_comum": estatisticas["genero_mais_comum"],
        "frequencia": estatisticas["frequencia_genero"],
    }

def processar_todas_as_regioes(jogos_vendas, jogos_genero, limite_vendas_regiao, regioes):
    """
    Processa os dados para todas as regiões.
    """
    dados_para_pdf = {}
    for regiao in regioes:
        dados_para_pdf[regiao] = processar_regiao(jogos_vendas, jogos_genero, limite_vendas_regiao, regiao)
    return dados_para_pdf

def processar_selecionada(regiao, jogos_vendas, jogos_genero, limite_vendas_regiao, gerar_relatorio):
    """
    Função que processa a região selecionada e gera o relatório.
    """
    try:
        dados = {regiao: processar_regiao(jogos_vendas, jogos_genero, limite_vendas_regiao, regiao)}
        gerar_relatorio(dados)
        messagebox.showinfo("Sucesso", f"Relatório para a região {regiao} gerado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar a região {regiao}: {e}")

def iniciar_interface(regioes, jogos_vendas, jogos_genero, limite_vendas_regiao, gerar_relatorio):
    """
    Cria e exibe a interface Tkinter para seleção de regiões e geração de relatórios.
    """
    def executar_regiao(regiao):
        processar_selecionada(regiao, jogos_vendas, jogos_genero, limite_vendas_regiao, gerar_relatorio)
        janela.quit()
    def executar_todas():
        try:
            dados = processar_todas_as_regioes(jogos_vendas, jogos_genero, limite_vendas_regiao, regioes)
            gerar_relatorio(dados)
            messagebox.showinfo("Sucesso", "Relatório para todas as regiões gerado com sucesso!")
            janela.quit()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar todas as regiões: {e}")

    # JANELA PRINCIPAL
    janela = tk.Tk()
    janela.title("Análise de Vendas e Gêneros")
    janela.geometry("400x400")
    for regiao in regioes:
        botao_regiao = tk.Button(janela, text=f"Gerar Grafo da Região: {regiao}", command=lambda r=regiao: executar_regiao(r))
        botao_regiao.pack(pady=10)
    botao_todas = tk.Button(janela, text="Gerar Grafo de Todas as Regiões", command=executar_todas)
    botao_todas.pack(pady=10)
    janela.mainloop()
