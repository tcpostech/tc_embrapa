from enum import Enum


class ViticultureCategory(str, Enum):
    """Embrapa enum based in all available categories"""
    PRODUCAO = 'PRODUCAO'
    PROCESSAMENTO = 'PROCESSAMENTO'
    COMERCIALIZACAO = 'COMERCIALIZACAO'
    IMPORTACAO = 'IMPORTACAO'
    EXPORTACAO = 'EXPORTACAO'


class ViticultureSubCategory(str, Enum):
    """Embrapa enum based in all available subcategories"""
    Producao = 'Producao'
    ProcessaViniferas = 'ProcessaViniferas'
    ProcessaAmericanas = 'ProcessaAmericanas'
    ProcessaMesa = 'ProcessaMesa'
    ProcessaSemclass = 'ProcessaSemclass'
    Comercio = 'Comercio'
    ImpVinhos = 'ImpVinhos'
    ImpEspumantes = 'ImpEspumantes'
    ImpFrescas = 'ImpFrescas'
    ImpPassas = 'ImpPassas'
    ImpSuco = 'ImpSuco'
    ExpVinho = 'ExpVinho'
    ExpEspumantes = 'ExpEspumantes'
    ExpUva = 'ExpUva'
    ExpSuco = 'ExpSuco'
