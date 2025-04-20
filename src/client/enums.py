from enum import Enum


class EmbrapaParams(str, Enum):
    """Embrapa enum based in all available categories"""
    PRODUCAO = 'PRODUCAO'
    PROCESSAMENTO = 'PROCESSAMENTO'
    COMERCIALIZACAO = 'COMERCIALIZACAO'
    IMPORTACAO = 'IMPORTACAO'
    EXPORTACAO = 'EXPORTACAO'
