"""
Utilities for Embrapa external communication
"""

URL = 'http://vitibrasil.cnpuv.embrapa.br/download/{}.csv'
FILE_PATH = 'files/{}.csv'

menus = {
    'PRODUCAO': ['Producao'],
    'PROCESSAMENTO': ['ProcessaViniferas', 'ProcessaAmericanas', 'ProcessaMesa', 'ProcessaSemclass'],
    'COMERCIALIZACAO': ['Comercio'],
    'IMPORTACAO': ['ImpVinhos', 'ImpEspumantes', 'ImpFrescas', 'ImpPassas', 'ImpSuco'],
    'EXPORTACAO': ['ExpVinho', 'ExpEspumantes', 'ExpUva', 'ExpSuco']
}

new_cols = {'cultivar': 'product', 'País': 'country', 'produto': 'product'}
