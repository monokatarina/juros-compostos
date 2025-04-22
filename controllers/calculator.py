from models.calculations import calcular_juros_compostos
import numpy as np

class CalculatorController:
    def calcular(self, capital, taxa, tempo, investimento_mensal, tipo_taxa):
        """
        Realiza todos os cálculos necessários
        
        Args:
            capital: Valor inicial
            taxa: Taxa de juros em porcentagem
            tempo: Tempo em anos
            investimento_mensal: Valor investido mensalmente
            tipo_taxa: 'anual' ou 'mensal'
            
        Returns:
            dict: Dicionário com todos os resultados
        """
        # Validar entradas
        if capital < 0 or taxa < 0 or tempo <= 0 or investimento_mensal < 0:
            raise ValueError("Valores devem ser positivos")
        
        # Converter taxa se necessário
        taxa_mensal = tipo_taxa == "mensal"
        
        # Calcular para cada ano
        anos = np.arange(0, tempo + 1)
        montantes = []
        investimentos_totais = []
        
        for ano in anos:
            montante = calcular_juros_compostos(
                capital, taxa, ano, investimento_mensal, taxa_mensal
            )
            total_investido = capital + (ano * 12 * investimento_mensal)
            
            montantes.append(montante)
            investimentos_totais.append(total_investido)
        
        # Resultados finais
        return {
            'anos': anos,
            'montantes': montantes,
            'investimentos_totais': investimentos_totais,
            'montante_final': montantes[-1],
            'total_investido': investimentos_totais[-1],
            'lucro': montantes[-1] - investimentos_totais[-1]
        }