from fpdf import FPDF
from collections import Counter
import os

class RelatorioPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Relatório de Análise de Vendas e Gêneros", border=False, ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

    def adicionar_regiao(self, regiao, dados):
        self.add_page()
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, f"Região: {regiao}", ln=True)
        self.ln(10)

        self.set_font("Arial", size=12)

        self.cell(0, 10, "Top 15 Jogos:", ln=True)
        if isinstance(dados.get("top_15"), list):
            for jogo in dados["top_15"]:
                self.cell(0, 10, f"- {jogo}", ln=True)
        else:
            self.cell(0, 10, "Dados indisponíveis", ln=True)

        self.ln(5)
        self.cell(0, 10, f"Número de Conexões: {dados.get('num_conexoes', 'N/A')}", ln=True)
        self.cell(0, 10, f"Gênero Mais Comum: {dados.get('genero_comum', 'N/A')}", ln=True)

        self.cell(0, 10, "Frequência de Gêneros:", ln=True)
        if isinstance(dados.get("frequencia"), dict):
            for genero, freq in dados["frequencia"].items():
                self.cell(0, 10, f"- {genero}: {freq}", ln=True)
        else:
            self.cell(0, 10, "Dados indisponíveis", ln=True)

        self.ln(10)
        self.cell(0, 10, f"Vendas Totais na Região: {dados.get('total_vendas', 'N/A'):.2f}M", ln=True)

        self.cell(0, 10, "Jogos por Gênero:", ln=True)
        if isinstance(dados.get("jogos_por_genero"), dict):
            for genero, jogos in dados["jogos_por_genero"].items():
                self.cell(0, 10, f"- {genero}: {len(jogos)} jogos", ln=True)
        else:
            self.cell(0, 10, "Dados indisponíveis", ln=True)


# GERAR RELATORIO PDF
def gerar_relatorio(dados):
    pdf = RelatorioPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for regiao, estatisticas in dados.items():
        if not isinstance(estatisticas, dict):
            print(f"Aviso: Dados inválidos para a região {regiao}. Pulando...")
            continue
        pdf.adicionar_regiao(regiao, estatisticas)

    nome_arquivo = "output/relatorio_vendas_generos.pdf"
    os.makedirs("output", exist_ok=True)
    pdf.output(nome_arquivo)

    print(f"Relatório gerado com sucesso: {nome_arquivo}")


def processar_dados(jogos):
    regioes = ["na_sales", "eu_sales", "jp_sales", "other_sales"]
    resultado = {}

    for regiao in regioes:
        jogos_por_regiao = [jogo for jogo in jogos if jogo.get(regiao, 0) > 0]
        total_vendas = sum(jogo.get(regiao, 0) for jogo in jogos_por_regiao)

        # Verificar se a chave 'genero' existe
        generos = Counter(jogo['genero'] for jogo in jogos_por_regiao if 'genero' in jogo and jogo['genero'])
        genero_comum = generos.most_common(1)[0][0] if generos else "N/A"

        jogos_por_genero = {}
        for jogo in jogos_por_regiao:
            genero = jogo.get('genero')
            if genero:
                if genero not in jogos_por_genero:
                    jogos_por_genero[genero] = []
                jogos_por_genero[genero].append(jogo['nome'])

        top_15 = sorted(jogos_por_regiao, key=lambda x: x.get(regiao, 0), reverse=True)[:15]

        resultado[regiao.upper()] = {
            "top_15": [jogo['nome'] for jogo in top_15],
            "num_conexoes": len(jogos_por_regiao),
            "frequencia": dict(generos),
            "genero_comum": genero_comum,
            "total_vendas": total_vendas,
            "jogos_por_genero": jogos_por_genero
        }

    return resultado


def gerar_relatorio(dados):
    """
    Gera um relatório em PDF com base nos dados fornecidos.
    """
    pdf = RelatorioPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for regiao, estatisticas in dados.items():
        if not isinstance(estatisticas, dict):
            print(f"Aviso: Dados inválidos para a região {regiao}. Pulando...")
            continue
        pdf.adicionar_regiao(regiao, estatisticas)

    nome_arquivo = "output/relatorio_vendas_generos.pdf"
    pdf.output(nome_arquivo)

    print(f"Relatório gerado com sucesso: {nome_arquivo}")