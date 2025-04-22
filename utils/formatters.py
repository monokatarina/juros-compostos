def format_currency(value):
    """
    Formata um valor numérico como moeda brasileira
    
    Args:
        value: Valor numérico
        
    Returns:
        str: Valor formatado como "R$ X.XXX,XX"
    """
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")