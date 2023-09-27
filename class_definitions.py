#class_definitions.py
from utils import calculate_azimuth, calculate_distance, associate_cogopoints_to_vertices

# Lazily import utils functions within classes
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
        from utils import calculate_distance, calculate_azimuth  # Lazy import
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.distance = calculate_distance(self.start_vertex, self.end_vertex)
        self.azimuth = calculate_azimuth(self.start_vertex, self.end_vertex)
        self.adjacent_polygon = None

class Polygon:
    def __init__(self, vertices):
        from utils import associate_cogopoints_to_vertices  # Lazy import
        self.vertices = vertices
        associate_cogopoints_to_vertices(self.vertices)
        self.edges = self.generate_edges()
        self.name = None
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

class Text:
    def __init__(self, x, y, content, text_type='txt'):
        self.x = x
        self.y = y
        self.content = content
        self.text_type = text_type  # 'txt' or 'mtext'
