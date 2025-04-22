def calcular_juros_compostos(capital_inicial, taxa_juros, tempo, investimento_periodico, taxa_mensal=False):
    """
    Calcula o montante acumulado com juros compostos e aportes periódicos
    
    Args:
        capital_inicial: Valor inicial
        taxa_juros: Taxa em porcentagem (ex: 10 para 10%)
        tempo: Tempo em anos
        investimento_periodico: Valor investido mensalmente
        taxa_mensal: Se True, taxa é mensal; se False, é anual
        
    Returns:
        float: Montante acumulado
    """
    if taxa_mensal:
        taxa_decimal = taxa_juros / 100
    else:
        taxa_decimal = taxa_juros / 100 / 12  # Converter anual para mensal
    
    meses = tempo * 12
    montante = capital_inicial
    
    for mes in range(1, meses + 1):
        montante *= (1 + taxa_decimal)
        montante += investimento_periodico
    
    return montante