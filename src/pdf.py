from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório de Jogos por Região', align='C', ln=True)
        self.ln(10)
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln(10)
    
    def add_section(self, region_name, top_15, num_conexoes, genero_comum, frequencia):
        self.add_page()
        self.chapter_title(f'Região: {region_name}')
        self.chapter_body(
            f'Top 15 jogos mais relevantes: {", ".join(top_15)}\n\n'
            f'Número total de conexões: {num_conexoes}\n\n'
            f'Gênero mais comum: {genero_comum} (Frequência: {frequencia})\n\n'
        )

def gerar_relatorio_unico(dados_regioes):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    pdf.chapter_title('Introdução')
    pdf.chapter_body(
        'Este relatório apresenta uma análise de jogos por gênero e vendas em diversas regiões. '
        'Os dados foram processados com base em critérios específicos de vendas e popularidade.'
    )

    for regiao, dados in dados_regioes.items():
        pdf.add_section(
            region_name=regiao,
            top_15=dados['top_15'],
            num_conexoes=dados['num_conexoes'],
            genero_comum=dados['genero_comum'],
            frequencia=dados['frequencia']
        )
    
    pdf.output('output/relatorio_jogos_por_regiao.pdf')
