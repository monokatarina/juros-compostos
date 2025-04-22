class InvestmentError(Exception):
    """Classe base para erros de investimento"""
    pass

class InvalidInputError(InvestmentError):
    """Erro quando valores de entrada são inválidos"""
    pass