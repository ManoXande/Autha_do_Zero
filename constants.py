#constants.py

# SISTEMA DE COORDENADAS

# Default EPSG code
DEFAULT_EPSG = 'EPSG:31982'

# EPSG codes for commonly used coordinate systems in Brazil (UTM)
EPSG_CODES_UTM = {
    '1': 'EPSG:4674 (SIRGAS 2000)',
    '2': 'EPSG:4326 (WGS 84)',
    '3': 'EPSG:31982 (SIRGAS 2000 / UTM zone 22S)',
    '4': 'EPSG:31983 (SIRGAS 2000 / UTM zone 23S)',
    '5': 'EPSG:31984 (SIRGAS 2000 / UTM zone 24S)',
    '6': 'EPSG:31985 (SIRGAS 2000 / UTM zone 25S)'
}

# EPSG codes for geographic coordinate systems in Brazil (Decimal Degrees)
GEOGRAPHIC_EPSG_CODES_DECIMAL = {
    '1': 'EPSG:4674 (SIRGAS 2000)',
    '2': 'EPSG:4326 (WGS 84)',
    '3': 'EPSG:31982 (SIRGAS 2000 / UTM zone 22S)',
    '4': 'EPSG:31983 (SIRGAS 2000 / UTM zone 23S)',
    '5': 'EPSG:31984 (SIRGAS 2000 / UTM zone 24S)',
    '6': 'EPSG:31985 (SIRGAS 2000 / UTM zone 25S)'
}

# EPSG codes for geographic coordinate systems in Brazil (Degrees, Minutes, Seconds)
GEOGRAPHIC_EPSG_CODES_DMS = {
    '1': 'EPSG:4674 (SIRGAS 2000)',
    '2': 'EPSG:4326 (WGS 84)',
    '3': 'EPSG:31982 (SIRGAS 2000 / UTM zone 22S)',
    '4': 'EPSG:31983 (SIRGAS 2000 / UTM zone 23S)',
    '5': 'EPSG:31984 (SIRGAS 2000 / UTM zone 24S)',
    '6': 'EPSG:31985 (SIRGAS 2000 / UTM zone 25S)'
}

# TEMPLATES DE RELATÓRIOS 

# Template padrão para a região de Chapecó - SC
TEMPLATE_CHAPECO_SC = {
    'initial': """Inicia-se a descrição deste perímetro no vértice {{ current_vertex_name }},
    georreferenciado no Sistema Geodésico Brasileiro, DATUM - SIRGAS2000, MC-51°W,
    de coordenadas N {{ current_vertex[1] }}m e E {{ current_vertex[0] }}m de altitude {{ current_vertex_elevation }}m;
    deste segue confrontando com {{ adjacent_text }}, com azimute de {{ degrees }}°{{ minutes }}'{{ seconds }}\"
    por uma distância de {{ distance }}m até o vértice {{ next_vertex_name }},
    de coordenadas N {{ next_vertex[1] }}m e E {{ next_vertex[0] }}m de altitude {{ next_vertex_elevation }}m;""",
    
    'other': """Deste segue confrontando com {{ adjacent_text }},
    com azimute de {{ degrees }}°{{ minutes }}'{{ seconds }}\" por uma distância de {{ distance }}m
    até o vértice {{ next_vertex_name }}, de coordenadas N {{ next_vertex[1] }}m e E {{ next_vertex[0] }}m
    de altitude {{ next_vertex_elevation }}m;""",
    
    'final': """Todas as coordenadas aqui descritas estão georreferenciadas ao Sistema Geodésico Brasileiro
    e encontram-se representadas no Sistema UTM, referenciadas ao Meridiano Central nº 51 WGr,
    tendo como Datum o SIRGAS2000. Todos os azimutes e distâncias, área e perímetro foram calculados no plano de projeção UTM.""",
    
    'header': """{{ lot_number }} da QUADRA “XX”, com área de {{ area }}m² ({{ area_text }}),
    com a seguinte descrição:""",
    
    'table': """Lado {{ current_vertex_name }}->{{ next_vertex_name }}:
    {{ current_vertex_name }}({{ current_vertex[0] }}, {{ current_vertex[1] }}, {{ current_vertex_elevation }}) ->
    {{ next_vertex_name }}({{ next_vertex[0] }}, {{ next_vertex[1] }}, {{ next_vertex_elevation }}),
    Distância: {{ distance }} m, Azimute: {{ degrees }}°{{ minutes }}'{{ seconds }}\";"""
}

# Template placeholder para outra região (por exemplo, São Paulo - SP)
TEMPLATE_SAO_PAULO_SP = {
    'initial': """Inicia-se a descrição deste perímetro no ponto ...""",  # Modifique conforme o padrão da região
    'other': """Deste segue ...""",  # Modifique conforme o padrão da região
    'final': """Todas as coordenadas aqui informadas ...""",  # Modifique conforme o padrão da região
    'header': """Lote {{ lot_number }} da QUADRA ...""",  # Modifique conforme o padrão da região
    'table': """Lado {{ current_vertex_name }} até {{ next_vertex_name }}: ...""",  # Modifique conforme o padrão da região
}

# Dicionário contendo os templates para cada padrão/região
TEMPLATES = {
    'Chapeco_SC': TEMPLATE_CHAPECO_SC,
    'Sao_Paulo_SP': TEMPLATE_SAO_PAULO_SP  # Adicione outros padrões aqui conforme necessário
}
