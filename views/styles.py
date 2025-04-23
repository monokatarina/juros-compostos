import tkinter as tk
from tkinter import ttk

# Paleta de cores moderna e tecnológica
COLORS = {
    "background": "#2d3436",
    "primary": "#0984e3",
    "secondary": "#00cec9",
    "success": "#00b894",
    "danger": "#d63031",
    "warning": "#fdcb6e",
    "text": "#dfe6e9",
    "text_secondary": "#b2bec3",
    "graph_bg": "#1e272e",
    "grid_color": "#34495e",
    "card_bg": "#34495e",
    "entry_bg": "#ffffff",
    "entry_fg": "#2d3436"
}

def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')

    # Configuração geral
    style.configure(
        '.', 
        background=COLORS["background"], 
        foreground=COLORS["text"],
        font=('Segoe UI', 9),
        borderwidth=1
    )

    # Frames
    style.configure('TFrame', background=COLORS["background"])
    style.configure('Header.TFrame', background=COLORS["background"])
    style.configure(
        'Graph.TFrame', 
        background=COLORS["graph_bg"],
        relief=tk.SOLID,
        borderwidth=1
    )

    # Cards
    style.configure(
        'Card.TFrame', 
        background=COLORS["card_bg"],
        relief=tk.RAISED,
        borderwidth=1
    )
    style.configure(
        'Card.TLabelframe', 
        background=COLORS["card_bg"],
        foreground=COLORS["secondary"],
        font=('Segoe UI', 10, 'bold'),
        relief=tk.FLAT,
        borderwidth=0
    )
    style.configure(
        'Card.TLabelframe.Label', 
        background=COLORS["card_bg"],
        foreground=COLORS["secondary"]
    )

    # Botões
    style.configure(
        'TButton',
        font=('Segoe UI', 10),
        borderwidth=1,
        relief='flat',
        padding=6
    )
    style.configure(
        'Accent.TButton',
        background=COLORS["primary"],
        foreground='white',
        font=('Segoe UI', 10, 'bold'),
        borderwidth=0,
        padding=10
    )
    style.map(
        'Accent.TButton',
        background=[
            ('active', COLORS["secondary"]), 
            ('pressed', COLORS["success"]),
            ('disabled', COLORS["grid_color"])
        ],
        foreground=[
            ('active', 'white'), 
            ('pressed', 'white'),
            ('disabled', COLORS["text_secondary"])
        ]
    )

    # Entradas
    style.configure(
        'TEntry',
        fieldbackground=COLORS["entry_bg"],
        foreground=COLORS["entry_fg"],
        borderwidth=2,
        relief='flat',
        padding=5
    )
    style.configure(
        'Modern.TEntry',
        fieldbackground=COLORS["entry_bg"],
        foreground=COLORS["entry_fg"],
        font=('Segoe UI', 10),
        borderwidth=1,
        relief='solid',
        padding=8
    )

    # Combobox
    style.configure(
        'TCombobox',
        fieldbackground=COLORS["entry_bg"],
        foreground=COLORS["entry_fg"],
        padding=5
    )
    style.configure(
        'Modern.TCombobox',
        fieldbackground=COLORS["entry_bg"],
        foreground=COLORS["entry_fg"],
        font=('Segoe UI', 10),
        padding=8
    )
    style.map(
        'TCombobox',
        fieldbackground=[('readonly', COLORS["entry_bg"])],
        selectbackground=[('readonly', COLORS["entry_bg"])]
    )

    # Labels
    style.configure(
        'InputHeader.TLabel',
        font=('Segoe UI', 9, 'bold'),
        foreground=COLORS["secondary"],
        background=COLORS["card_bg"]
    )
    style.configure(
        'ResultHeader.TLabel',
        font=('Segoe UI', 10, 'bold'),
        foreground=COLORS["text"],
        background=COLORS["card_bg"]
    )
    style.configure(
        'ResultValue.TLabel',
        font=('Segoe UI', 14, 'bold'),
        background=COLORS["card_bg"]
    )
    style.configure(
        'Title.TLabel',
        font=('Segoe UI', 18, 'bold'),
        foreground=COLORS["primary"],
        background=COLORS["background"]
    )
    style.configure(
        'Subtitle.TLabel',
        font=('Segoe UI', 10),
        foreground=COLORS["secondary"],
        background=COLORS["background"]
    )

    # Progressbar
    style.configure(
        'TProgressbar',
        thickness=20,
        troughcolor=COLORS["grid_color"],
        background=COLORS["primary"],
        lightcolor=COLORS["primary"],
        darkcolor=COLORS["primary"]
    )

    # Separador
    style.configure('TSeparator', background=COLORS["grid_color"])

    # Scrollbar
    style.configure(
        'TScrollbar',
        gripcount=0,
        background=COLORS["grid_color"],
        troughcolor=COLORS["background"],
        bordercolor=COLORS["background"],
        arrowcolor=COLORS["text"],
        width=14
    )
    style.map(
        'TScrollbar',
        background=[('active', COLORS["secondary"])]
    )