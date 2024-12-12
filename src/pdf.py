from fpdf import FPDF

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