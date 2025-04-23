import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from controllers.calculator import CalculatorController
from views.styles import configure_styles
from utils.formatters import format_currency

class JurosCompostosApp:
    def __init__(self, root):
        self.root = root
        self.controller = CalculatorController()
        self.setup_ui()
        configure_styles()
        
    def setup_ui(self):
        self.root.title("💰 Calculadora de Juros Compostos Premium")
        self.root.geometry("1200x800")
        self.root.minsize(400, 300) # Tamanho mínimo da janela
        
        # Frames principais
        self.create_frames()
        self.create_inputs()
        self.create_result_labels()
        
    def create_frames(self):
        # Frame de cabeçalho
        self.header_frame = ttk.Frame(self.root, padding=(10, 5)) 
        self.header_frame.pack(fill=tk.X)
        
        # Frame de entrada
        self.input_frame = ttk.LabelFrame(self.root, text="📊 Parâmetros do Investimento", padding=10)
        self.input_frame.pack(fill=tk.X, padx=20, pady=(0, 10)) 
        
        # Frame do gráfico
        self.graph_frame = ttk.Frame(self.root)
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Frame de resultados
        self.result_frame = ttk.LabelFrame(self.root, text="📈 Resultados Finais", padding=10)
        self.result_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Cabeçalho
        title_font = tk.font.Font(size=10, weight='bold')
        ttk.Label(self.header_frame, text="Calculadora de Juros Compostos", 
                font=title_font, foreground="#2c3e50").pack()
        ttk.Label(self.header_frame, text="Simule seus investimentos com juros compostos", 
                foreground="#7f8c8d").pack(pady=(0, 10))
    
    def create_inputs(self):
        # Variável para controle do tipo de taxa
        self.tipo_taxa = tk.StringVar(value="anual")
        
        # Grid configuration
        for i in range(2): # Configurar colunas do grid
            self.input_frame.columnconfigure(i, weight=1)
        
        # Capital Inicial
        ttk.Label(self.input_frame, text="Capital Inicial (R$):", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.capital_inicial = ttk.Entry(self.input_frame, font=('Helvetica', 11))
        self.capital_inicial.grid(row=1, column=0, sticky=tk.EW, padx=5, pady=(0, 10))
        
        # Tipo de Taxa
        ttk.Label(self.input_frame, text="Tipo de Taxa:", style='Header.TLabel').grid(row=0, column=1, sticky=tk.W, pady=5)
        taxa_frame = ttk.Frame(self.input_frame)
        taxa_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=(0, 10)) # Configurar frame para os botões de taxa
        ttk.Radiobutton(taxa_frame, text="Anual", variable=self.tipo_taxa, value="anual").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(taxa_frame, text="Mensal", variable=self.tipo_taxa, value="mensal").pack(side=tk.LEFT)
        
        # Taxa de Juros
        ttk.Label(self.input_frame, text="Taxa de Juros (%):", style='Header.TLabel').grid(row=0, column=2, sticky=tk.W, pady=5)
        self.taxa_juros = ttk.Entry(self.input_frame, font=('Helvetica', 11))
        self.taxa_juros.grid(row=1, column=2, sticky=tk.EW, padx=5, pady=(0, 10))
        
        # Tempo
        ttk.Label(self.input_frame, text="Tempo (anos):", style='Header.TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.tempo = ttk.Entry(self.input_frame, font=('Helvetica', 11))
        self.tempo.grid(row=3, column=0, sticky=tk.EW, padx=5, pady=(0, 10))
        
        # Investimento Mensal
        ttk.Label(self.input_frame, text="Investimento Mensal (R$):", style='Header.TLabel').grid(row=2, column=1, sticky=tk.W, pady=5)
        self.investimento_mensal = ttk.Entry(self.input_frame, font=('Helvetica', 11))
        self.investimento_mensal.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=(0, 10))
        
        # Botão de cálculo
        self.calcular_btn = ttk.Button(
            self.input_frame, 
            text="CALCULAR", 
            command=self.calcular_e_plotar,
            style='TButton'
        )
        self.calcular_btn.grid(row=3, column=2, columnspan=2, pady=(0, 10), sticky=tk.E)
        
        # Valores padrão
        self.capital_inicial.insert(0, "10000")
        self.taxa_juros.insert(0, "10")
        self.tempo.insert(0, "5")
        self.investimento_mensal.insert(0, "500")
    
    def create_result_labels(self):
        # Configurar grid
        for i in range(3):
            self.result_frame.columnconfigure(i, weight=1)
        
        # Labels de resultados
        ttk.Label(self.result_frame, text="Montante Final:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.montante_final_label = ttk.Label(self.result_frame, text="R$ 0,00", style='Result.TLabel', foreground='#27ae60')
        self.montante_final_label.grid(row=1, column=0, sticky=tk.W)
        
        ttk.Label(self.result_frame, text="Total Investido:", style='Header.TLabel').grid(row=0, column=1, sticky=tk.W)
        self.total_investido_label = ttk.Label(self.result_frame, text="R$ 0,00", style='Result.TLabel', foreground='#3498db')
        self.total_investido_label.grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(self.result_frame, text="Lucro:", style='Header.TLabel').grid(row=0, column=2, sticky=tk.W)
        self.lucro_label = ttk.Label(self.result_frame, text="R$ 0,00", style='Result.TLabel', foreground='#e74c3c')
        self.lucro_label.grid(row=1, column=2, sticky=tk.W)
    
    def calcular_e_plotar(self):
        try:
            # Obter valores
            capital = float(self.capital_inicial.get())
            taxa = float(self.taxa_juros.get())
            tempo = int(self.tempo.get())
            investimento = float(self.investimento_mensal.get())
            tipo_taxa = self.tipo_taxa.get()
            
            # Calcular
            resultados = self.controller.calcular(
                capital, taxa, tempo, investimento, tipo_taxa
            )
            
            # Atualizar resultados
            self.atualizar_resultados(resultados)
            
            # Plotar gráfico
            self.plotar_grafico(resultados)
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {str(e)}")
    
    def atualizar_resultados(self, resultados):
        self.montante_final_label.config(text=format_currency(resultados['montante_final']))
        self.total_investido_label.config(text=format_currency(resultados['total_investido']))
        
        lucro = resultados['lucro']
        cor = '#27ae60' if lucro >= 0 else '#e74c3c'
        self.lucro_label.config(text=format_currency(lucro), foreground=cor)
    
    def plotar_grafico(self, resultados):
        # Limpar gráfico anterior
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Criar figura
        fig, ax = plt.subplots(figsize=(6, 4))  # Aumentar o tamanho do gráfico
        fig.patch.set_facecolor('#f5f5f5')  # Fundo mais claro para contraste
        
        # Plotar dados
        anos = resultados['anos']
        montantes = resultados['montantes']
        investimentos_totais = resultados['investimentos_totais']
        
        ax.plot(
            anos, 
            montantes, 
            label='Montante Acumulado', 
            color='#2ecc71', 
            linewidth=2
        )
        ax.plot(
            anos, 
            investimentos_totais, 
            label='Total Investido', 
            color='#3498db', 
            linestyle='--', 
            linewidth=2
        )
        # Adicionar pontos no gráfico
        ax.scatter(anos, montantes, color='#27ae60', s=60, label='Pontos Montante', edgecolors='black')
        ax.scatter(anos, investimentos_totais, color='#2980b9', s=60, label='Pontos Investido', edgecolors='black')
        
        # Adicionar rótulos nos pontos
        for x, y in zip(anos, montantes):
            ax.text(x, y, f"R${y:,.2f}", fontsize=10, fontweight='bold', color='#2c3e50', ha='center', va='bottom')
        for x, y in zip(anos, investimentos_totais):
            ax.text(x, y, f"R${y:,.2f}", fontsize=10, fontweight='bold', color='#2c3e50', ha='center', va='top')
        
        # Configurar gráfico
        ax.set_title("Evolução do Investimento ao Longo do Tempo", fontsize=10, color='#34495e')
        ax.set_xlabel("Anos", fontsize=10, color='#34495e')
        ax.set_ylabel("Valor (R$)", fontsize=10, color='#34495e')
        ax.legend(fontsize=10, loc='upper left', frameon=True, facecolor='white', edgecolor='gray')
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # Formatar eixo Y como moeda
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"R${x/1000:,.0f}k" if x >= 1000 else f"R${x:,.0f}")
        )
        
        # Exibir no tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.graph_frame.update_idletasks()
        self.graph_frame.pack_propagate(False)  # Manter o tamanho do frame do gráfico fixo
        self.graph_frame.config(width=800, height=200)  # Definir tamanho fixo do frame do gráfico
