#common_utils.py
import math 
from configurations import ROUNDING_RULES

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

# O log pode ser implementado de acordo com a sua necessidade
def log(message):
    print(message)  # Exemplo simples de função de log

class Cogopoint:
    def __init__(self, x, y, z, point_number, description):
        self.x = x
        self.y = y
        self.z = z
        self.point_number = point_number
        self.description = description

class Vertex:
    def __init__(self, x, y, z=None, cogopoint=None):
        self.x = x
        self.y = y
        self.z = z
        self.cogopoint = cogopoint
        self.id = self.generate_id()

    def generate_id(self):
        if self.cogopoint:
            return f"{self.cogopoint.description}{self.cogopoint.point_number}"
        return None

class Edge:
    def __init__(self, start_vertex, end_vertex):
        self.start_vertex = start_vertex  # Vertex object with possible Cogopoint
        self.end_vertex = end_vertex  # Vertex object with possible Cogopoint
        self.distance = calculate_distance(self.start_vertex, self.end_vertex)
        self.azimuth = calculate_azimuth(self.start_vertex, self.end_vertex)
        self.adjacent_polygon = None  # To be identified later

class Polygon:
    def __init__(self, vertices):
        self.vertices = vertices  # List of Vertex objects
        associate_cogopoints_to_vertices(self.vertices)
        self.edges = self.generate_edges()
        self.name = None  # To be associated later
        self.centroid = self.calculate_centroid()
        self.is_closed = self.check_if_closed()

    def check_if_closed(self):
        return self.vertices[0] == self.vertices[-1]

    def generate_edges(self):
        edges = []
        for i in range(len(self.vertices)):
            start_vertex = self.vertices[i]
            end_vertex = self.vertices[(i + 1) % len(self.vertices)]
            edges.append(Edge(start_vertex, end_vertex))
        return edges

    def calculate_centroid(self):
        # Simplified method, to be refined
        x_coords = [vertex.x for vertex in self.vertices]
        y_coords = [vertex.y for vertex in self.vertices]
        centroid_x = sum(x_coords) / len(x_coords)
        centroid_y = sum(y_coords) / len(y_coords)
        return centroid_x, centroid_y

class Text:
    def __init__(self, x, y, content, text_type='txt'):
        self.x = x
        self.y = y
        self.content = content
        self.text_type = text_type  # 'txt' or 'mtext'