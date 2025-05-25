"""
Enums for api communication with database and external communication
"""
from enum import Enum


class CategoryEnum(str, Enum):
    """Embrapa enum based in all available categories"""
    PRODUCAO = 'PRODUCAO'
    PROCESSAMENTO = 'PROCESSAMENTO'
    COMERCIALIZACAO = 'COMERCIALIZACAO'
    IMPORTACAO = 'IMPORTACAO'
    EXPORTACAO = 'EXPORTACAO'


class SubCategoryEnum(str, Enum):
    """Embrapa enum based in all available subcategories"""
    PRODUCAO = 'Producao'
    PROCESSAVINIFERAS = 'ProcessaViniferas'
    PROCESSAAMERICANAS = 'ProcessaAmericanas'
    PROCESSAMESA = 'ProcessaMesa'
    PROCESSASEMCLASS = 'ProcessaSemclass'
    COMERCIO = 'Comercio'
    IMPVINHOS = 'ImpVinhos'
    IMPESPUMANTES = 'ImpEspumantes'
    IMPFRESCAS = 'ImpFrescas'
    IMPPASSAS = 'ImpPassas'
    IMPSUCO = 'ImpSuco'
    EXPVINHO = 'ExpVinho'
    EXPESPUMANTES = 'ExpEspumantes'
    EXPUVA = 'ExpUva'
    EXPSUCO = 'ExpSuco'


class ProcessModeEnum(str, Enum):
    """Enumeration for processing external data mode"""
    API = 'API'
    FILE = 'FILE'
