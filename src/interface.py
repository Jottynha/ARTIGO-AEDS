import tkinter as tk
from tkinter import messagebox
import graph
import pdf

def processar_regiao(jogos_vendas, jogos_genero, limite_vendas_regiao, regiao):
    """
    Processa os dados para uma região específica.
    """
    try:
        grafo = graph.criar_grafo_com_genero_por_regiao(
            jogos_vendas, jogos_genero, limite_vendas_regiao, regiao
        )
        return grafo
    except Exception as e:
        print(f"Erro ao processar a região {regiao}: {e}")
        raise

def processar_todas_as_regioes(jogos_vendas, jogos_genero, limite_vendas_regiao, regioes):
    """
    Processa os dados para todas as regiões.
    """
    for regiao in regioes:
        processar_regiao(jogos_vendas, jogos_genero, limite_vendas_regiao, regiao)

def gerar_relatorio(jogos_vendas):
    """
    Gera o relatório em PDF usando os dados processados.
    """
    try:
        dados_processados = pdf.processar_dados(jogos_vendas)
        pdf.gerar_relatorio(dados_processados)
        messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar o relatório: {e}")

        # Exemplo de função gerar_relatorio (substitua pela sua implementação)


def iniciar_interface(regioes, jogos_vendas, jogos_genero, limite_vendas_regiao):
    """
    Cria e exibe a interface Tkinter para seleção de regiões, geração de grafos e relatório.
    """
    def executar_regiao(regiao):
        try:
            processar_regiao(jogos_vendas, jogos_genero, limite_vendas_regiao, regiao)
            messagebox.showinfo("Sucesso", f"Grafo da região {regiao} gerado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar a região {regiao}: {e}")

    def executar_todas():
        try:
            processar_todas_as_regioes(jogos_vendas, jogos_genero, limite_vendas_regiao, regioes)
            messagebox.showinfo("Sucesso", "Grafos para todas as regiões gerados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar todas as regiões: {e}")

    def gerar_relatorio_interface():
        """
        Gera o relatório em PDF ao clicar no botão.
        """
        gerar_relatorio(jogos_vendas)

    # JANELA PRINCIPAL
    janela = tk.Tk()
    janela.title("Análise de Vendas e Gêneros")
    janela.geometry("400x500")
    for regiao in regioes:
        botao_regiao = tk.Button(janela, text=f"Gerar Grafo da Região: {regiao}",
                                 command=lambda r=regiao: executar_regiao(r))
        botao_regiao.pack(pady=10)
    botao_todas = tk.Button(janela, text="Gerar Grafo de Todas as Regiões", command=executar_todas)
    botao_todas.pack(pady=10)
    botao_relatorio = tk.Button(janela, text="Gerar Relatório em PDF", command=gerar_relatorio_interface)
    botao_relatorio.pack(pady=10)

    janela.mainloop()
