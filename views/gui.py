import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from controllers.calculator import CalculatorController
from views.styles import configure_styles
from utils.formatters import format_currency

# Paleta de cores moderna
COLORS = {
    "background": "#2d3436",
    "primary": "#0984e3",
    "secondary": "#00cec9",
    "success": "#00b894",
    "danger": "#d63031",
    "warning": "#fdcb6e",
    "text": "#dfe6e9",
    "graph_bg": "#1e272e",
    "grid_color": "#34495e",
    "card_bg": "#34495e"
}

class JurosCompostosApp:
    def __init__(self, root):
        self.root = root
        self.controller = CalculatorController()
        self.setup_ui()
        configure_styles()
        
    def setup_ui(self):
        self.root.title("🚀 Calculadora de Juros Compostos | WealthTech")
        self.root.geometry("1280x720")
        self.root.minsize(800, 600)
        self.root.configure(bg=COLORS["background"])
        
        # Crie um canvas e uma scrollbar vertical
        self.canvas = tk.Canvas(self.root, bg=COLORS["background"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        # Configure o canvas para usar a scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Crie um frame principal dentro do canvas
        self.main_frame = ttk.Frame(self.canvas, style='TFrame')
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Configure o canvas para atualizar a região de rolagem
        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        ))
        
        # Permita rolagem com o mouse
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Agora crie os frames dentro do main_frame
        self.create_frames()
        self.create_inputs()
        self.create_result_labels()
        

    def create_frames(self):
        # Frame de cabeçalho
        self.header_frame = ttk.Frame(self.main_frame, style='Header.TFrame')
        self.header_frame.pack(fill=tk.X, pady=(10, 20))
        
        # Título moderno
        ttk.Label(self.header_frame, 
                 text="CALCULADORA DE JUROS COMPOSTOS", 
                 font=('Segoe UI', 18, 'bold'),
                 foreground=COLORS["primary"],
                 background=COLORS["background"]).pack(pady=5)
        
        ttk.Label(self.header_frame, 
                 text="Simule seus investimentos com tecnologia avançada", 
                 font=('Segoe UI', 10),
                 foreground=COLORS["secondary"],
                 background=COLORS["background"]).pack()
        
        # Frame de entrada
        self.input_frame = ttk.LabelFrame(
            self.main_frame, 
            text="  PARÂMETROS DO INVESTIMENTO  ",
            style='Card.TLabelframe',
            padding=(20, 10))
        self.input_frame.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        # Frame do gráfico
        self.graph_frame = ttk.Frame(
            self.main_frame,
            style='Graph.TFrame',
            relief=tk.SOLID,
            borderwidth=1)
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        # Frame de resultados
        self.result_frame = ttk.LabelFrame(
            self.main_frame, 
            text="  RESULTADOS FINAIS  ",
            style='Card.TLabelframe',
            padding=(20, 15))
        self.result_frame.pack(fill=tk.X, padx=40, pady=(0, 30))
    
    def create_inputs(self):
        # Configuração do grid responsivo
        for i in range(3):
            self.input_frame.columnconfigure(i, weight=1, uniform='input_cols')
        
        # Capital Inicial
        ttk.Label(self.input_frame, 
                 text="CAPITAL INICIAL (R$):", 
                 style='InputHeader.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.capital_inicial = ttk.Entry(
            self.input_frame, 
            font=('Segoe UI', 11),
            style='Modern.TEntry')
        self.capital_inicial.grid(row=1, column=0, sticky=tk.EW, padx=10, pady=(0, 15))
        
        # Tipo de Taxa (agora como Combobox moderno)
        ttk.Label(self.input_frame, 
                 text="TIPO DE TAXA:", 
                 style='InputHeader.TLabel').grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        self.tipo_taxa = ttk.Combobox(
            self.input_frame,
            values=["Anual", "Mensal"],
            font=('Segoe UI', 10),
            state='readonly',
            style='Modern.TCombobox')
        self.tipo_taxa.current(0)
        self.tipo_taxa.grid(row=1, column=1, sticky=tk.EW, padx=10, pady=(0, 15))
        
        # Taxa de Juros
        ttk.Label(self.input_frame, 
                 text="TAXA DE JUROS (%):", 
                 style='InputHeader.TLabel').grid(row=0, column=2, sticky=tk.W, pady=(0, 5))
        self.taxa_juros = ttk.Entry(
            self.input_frame, 
            font=('Segoe UI', 11),
            style='Modern.TEntry')
        self.taxa_juros.grid(row=1, column=2, sticky=tk.EW, padx=10, pady=(0, 15))
        
        # Tempo
        ttk.Label(self.input_frame, 
                 text="TEMPO (ANOS):", 
                 style='InputHeader.TLabel').grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.tempo = ttk.Entry(
            self.input_frame, 
            font=('Segoe UI', 11),
            style='Modern.TEntry')
        self.tempo.grid(row=3, column=0, sticky=tk.EW, padx=10, pady=(0, 15))
        
        # Investimento Mensal
        ttk.Label(self.input_frame, 
                 text="INVESTIMENTO MENSAL (R$):", 
                 style='InputHeader.TLabel').grid(row=2, column=1, sticky=tk.W, pady=(0, 5))
        self.investimento_mensal = ttk.Entry(
            self.input_frame, 
            font=('Segoe UI', 11),
            style='Modern.TEntry')
        self.investimento_mensal.grid(row=3, column=1, sticky=tk.EW, padx=10, pady=(0, 15))
        
        # Botão de cálculo moderno
        self.calcular_btn = ttk.Button(
            self.input_frame, 
            text="CALCULAR PROJEÇÃO", 
            command=self.calcular_e_plotar,
            style='Accent.TButton')
        self.calcular_btn.grid(row=3, column=2, padx=10, pady=(0, 15), sticky=tk.E)
        
        # Valores padrão
        self.capital_inicial.insert(0, "10000")
        self.taxa_juros.insert(0, "10")
        self.tempo.insert(0, "5")
        self.investimento_mensal.insert(0, "500")
    
    def create_result_labels(self):
        # Configurar grid com colunas de peso igual
        for i in range(3):
            self.result_frame.columnconfigure(i, weight=1, uniform='result_cols')
        
        # Card de Montante Final
        montante_card = ttk.Frame(self.result_frame, style='Card.TFrame')
        montante_card.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=5)
        ttk.Label(montante_card, 
                 text="MONTANTE FINAL", 
                 style='ResultHeader.TLabel').pack(pady=(5, 10))
        self.montante_final_label = ttk.Label(
            montante_card, 
            text="R$ 0,00", 
            style='ResultValue.TLabel',
            foreground=COLORS["success"])
        self.montante_final_label.pack(pady=(0, 10))
        
        # Card de Total Investido
        investido_card = ttk.Frame(self.result_frame, style='Card.TFrame')
        investido_card.grid(row=0, column=1, sticky=tk.NSEW, padx=10, pady=5)
        ttk.Label(investido_card, 
                 text="TOTAL INVESTIDO", 
                 style='ResultHeader.TLabel').pack(pady=(5, 10))
        self.total_investido_label = ttk.Label(
            investido_card, 
            text="R$ 0,00", 
            style='ResultValue.TLabel',
            foreground=COLORS["primary"])
        self.total_investido_label.pack(pady=(0, 10))
        
        # Card de Lucro
        lucro_card = ttk.Frame(self.result_frame, style='Card.TFrame')
        lucro_card.grid(row=0, column=2, sticky=tk.NSEW, padx=10, pady=5)
        ttk.Label(lucro_card, 
                 text="LUCRO", 
                 style='ResultHeader.TLabel').pack(pady=(5, 10))
        self.lucro_label = ttk.Label(
            lucro_card, 
            text="R$ 0,00", 
            style='ResultValue.TLabel',
            foreground=COLORS["danger"])
        self.lucro_label.pack(pady=(0, 10))
    
    def calcular_e_plotar(self):
        try:
            # Obter valores
            capital = float(self.capital_inicial.get())
            taxa = float(self.taxa_juros.get())
            tempo = int(self.tempo.get())
            investimento = float(self.investimento_mensal.get())
            tipo_taxa = "anual" if self.tipo_taxa.get() == "Anual" else "mensal"
            
            # Calcular
            resultados = self.controller.calcular(
                capital, taxa, tempo, investimento, tipo_taxa
            )
            
            # Atualizar resultados
            self.atualizar_resultados(resultados)
            
            # Plotar gráfico
            self.plotar_grafico(resultados)
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {str(e)}", parent=self.root)
    
    def atualizar_resultados(self, resultados):
        self.montante_final_label.config(text=format_currency(resultados['montante_final']))
        self.total_investido_label.config(text=format_currency(resultados['total_investido']))
        
        lucro = resultados['lucro']
        cor = COLORS["success"] if lucro >= 0 else COLORS["danger"]
        self.lucro_label.config(text=format_currency(lucro), foreground=cor)
    
    def plotar_grafico(self, resultados):
        # Limpar gráfico anterior
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Configurar estilo do gráfico
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor(COLORS["graph_bg"])
        ax.set_facecolor(COLORS["graph_bg"])
        
        # Dados
        anos = resultados['anos']
        montantes = resultados['montantes']
        investimentos_totais = resultados['investimentos_totais']
        
        # Plotar linhas com gradiente
        ax.plot(anos, montantes, 
               label='Montante Acumulado', 
               color=COLORS["success"], 
               linewidth=3,
               marker='o',
               markersize=8,
               markerfacecolor=COLORS["text"])
        
        ax.plot(anos, investimentos_totais, 
               label='Total Investido', 
               color=COLORS["primary"], 
               linestyle='--', 
               linewidth=2.5)
        
        # Adicionar anotações nos pontos do montante
        for i, (x, y) in enumerate(zip(anos, montantes)):
            # Ajustar posição vertical do texto para evitar sobreposição
            offset = (max(montantes) - min(montantes)) * 0.05
            va = 'bottom' if i % 2 == 0 else 'top'
            y_offset = y + offset if va == 'bottom' else y - offset
            
            ax.annotate(f"R${y:,.2f}",
                    xy=(x, y),
                    xytext=(x, y_offset),
                    ha='center',
                    va=va,
                    fontsize=9,
                    fontweight='bold',
                    color=COLORS["text"],
                    bbox=dict(boxstyle='round,pad=0.3',
                                facecolor=COLORS["card_bg"],
                                edgecolor=COLORS["grid_color"],
                                alpha=0.8),
                    arrowprops=dict(arrowstyle='->',
                                    color=COLORS["secondary"],
                                    alpha=0.6))
        
        # Preenchimento entre as linhas
        ax.fill_between(anos, montantes, investimentos_totais, 
                       where=[m > i for m, i in zip(montantes, investimentos_totais)],
                       color=COLORS["success"], alpha=0.1)
        
        # Configurações do gráfico
        ax.set_title("PROJEÇÃO DO INVESTIMENTO", 
                   fontsize=12, 
                   pad=20,
                   color=COLORS["text"],
                   fontweight='bold')
        
        ax.set_xlabel("Anos", 
                     fontsize=10, 
                     color=COLORS["secondary"],
                     labelpad=10)
        
        ax.set_ylabel("Valor (R$)", 
                     fontsize=10, 
                     color=COLORS["secondary"],
                     labelpad=10)
        
        # Configurar eixos
        ax.spines['bottom'].set_color(COLORS["grid_color"])
        ax.spines['left'].set_color(COLORS["grid_color"])
        ax.tick_params(axis='both', colors=COLORS["text"])
        
        # Grade
        ax.grid(color=COLORS["grid_color"], linestyle='--', linewidth=0.5, alpha=0.7)
        
        # Legenda
        ax.legend(fontsize=10, 
                loc='upper left', 
                frameon=True, 
                facecolor=COLORS["graph_bg"],
                edgecolor=COLORS["grid_color"])
        
        # Formatar eixo Y como moeda
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"R${x/1000:,.0f}k" if x >= 1000 else f"R${x:,.0f}")
        )
        
        # Canvas do gráfico
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)