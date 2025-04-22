from tkinter import ttk

def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configurações de estilo
    style.configure('TFrame', background='#ecf0f1')
    style.configure('TLabel', background='#ecf0f1', font=('Helvetica', 10))
    style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=5)
    style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'), foreground='#2c3e50')
    style.configure('TEntry', font=('Helvetica', 11), padding=5)
    
    style.map('TButton',
            foreground=[('active', 'white'), ('pressed', 'white')],
            background=[('active', '#3498db'), ('pressed', '#2980b9')])
    
    style.configure('Result.TLabel', font=('Helvetica', 12, 'bold'))