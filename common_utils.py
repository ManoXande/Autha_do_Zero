import math
from pyproj import Transformer  # Supondo que você esteja usando pyproj para transformações de coordenadas

# Constantes para arredondamento (Estas podem ser importadas de um arquivo de configuração)
ROUNDING_RULES = {
    "distances": 2,
    "azimuths": 2,
}

def custom_round(number, decimals):
    return round(number, decimals)

def calculate_distance(start_vertex, end_vertex):
    dx = end_vertex.x - start_vertex.x
    dy = end_vertex.y - start_vertex.y
    dz = end_vertex.z - start_vertex.z
    distance = math.sqrt(dx**2 + dy**2 + dz**2)
    return round(distance, ROUNDING_RULES["distances"])

def calculate_azimuth(start_vertex, end_vertex):
    dx = end_vertex.x - start_vertex.x
    dy = end_vertex.y - start_vertex.y
    azimuth = math.degrees(math.atan2(dy, dx))
    if azimuth < 0:
        azimuth += 360
    return round(azimuth, ROUNDING_RULES["azimuths"])

def azimuth_to_gms(azimuth):
    degrees = int(azimuth)
    minutes = int((azimuth - degrees) * 60)
    seconds = ((azimuth - degrees) * 60 - minutes) * 60
    return degrees, minutes, round(seconds, ROUNDING_RULES["azimuths"])

def convert_coordinates(vertex, from_epsg, to_epsg):
    transformer = Transformer.from_crs(from_epsg, to_epsg)
    x, y, z = transformer.transform(vertex.x, vertex.y, vertex.z)
    return (x, y, z)

# O log pode ser implementado de acordo com a sua necessidade
def log(message):
    print(message)  # Exemplo simples de função de log
