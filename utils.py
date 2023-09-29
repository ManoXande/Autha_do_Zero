#utils.py
import math
import pyproj
import configurations
from debug_logs import setup_custom_logger
from typing import List
import logging
from class_definitions import Vertex  

logger = logging.getLogger(__name__)

transformer = pyproj.Transformer.from_crs("EPSG:31982", "EPSG:31982", always_xy=True)
rounding_rules = configurations.ROUNDING_RULES
log_config = configurations.log

log_debug = setup_custom_logger('utils') 

rounding_rules = {"distances": 2} 

def custom_round(number, decimals):
    return round(number, decimals)

def calculate_distance(start_vertex: Vertex, end_vertex: Vertex):
    try:
        if not isinstance(start_vertex, Vertex) or not isinstance(end_vertex, Vertex):
            logger.error("Os argumentos devem ser instâncias da classe Vertex.")
            return None

        dx = end_vertex.x - start_vertex.x
        dy = end_vertex.y - start_vertex.y
        dz = end_vertex.z - start_vertex.z

        distance = math.sqrt(dx**2 + dy**2 + dz**2)

        return round(distance, rounding_rules["distances"])

    except Exception as e:
        logger.error(f"Um erro ocorreu durante o cálculo da distância: {e}")
        return None

def calculate_azimuth(start_vertex, end_vertex):
    dx = end_vertex.x - start_vertex.x
    dy = end_vertex.y - start_vertex.y
    azimuth = math.degrees(math.atan2(dy, dx))
    if azimuth < 0:
        azimuth += 360
    return round(azimuth, ROUNDING_RULES["azimuths"])  # Arredondamento diretamente aqui

def azimuth_to_gms(azimuth):
    degrees = int(azimuth)
    minutes = int((azimuth - degrees) * 60)
    seconds = ((azimuth - degrees) * 60 - minutes) * 60
    return degrees, minutes, round(seconds, ROUNDING_RULES["azimuths"])  # Arredondamento diretamente aqui

def convert_coordinates(vertex, from_epsg, to_epsg):
    from class_definitions import Vertex  # Lazy import
    transformer = pyproj.Transformer.from_crs(from_epsg, to_epsg, always_xy=True)
    x, y, z = transformer.transform(vertex.x, vertex.y, vertex.z)
    return Vertex(x, y, z)

def reorder_polygon_vertices(polygon):
    northernmost_vertex = max(polygon.vertices, key=lambda v: v.y)
    start_index = polygon.vertices.index(northernmost_vertex)
    polygon.vertices = polygon.vertices[start_index:] + polygon.vertices[:start_index]
    polygon.edges = polygon.generate_edges()
    log(f"Reordered vertices for polygon {polygon.name}.")

def calculate_centroid(self):
    x_coords = [vertex.x for vertex in vertices]
    y_coords = [vertex.y for vertex in vertices]
    centroid_x = sum(x_coords) / len(x_coords)
    centroid_y = sum(y_coords) / len(y_coords)
    return centroid_x, centroid_y

def associate_names_to_polygons(polygons, texts):
    for polygon in polygons:
        closest_text = min(texts, key=lambda txt: calculate_distance(polygon.centroid, txt))
        polygon.name = closest_text.content

def identify_adjacent_polygons(polygons):
    for polygon in polygons:
        for edge in polygon.edges:
            for other_polygon in polygons:
                if other_polygon == polygon:
                    continue
                for other_edge in other_polygon.edges:
                    if edge.start_vertex == other_edge.end_vertex and edge.end_vertex == other_edge.start_vertex:
                        edge.adjacent_polygon = other_polygon.name
                        other_edge.adjacent_polygon = polygon.name

def user_select_polygons(polygons):
    # Função para permitir que o usuário selecione polígonos
    print("Lista de polígonos disponíveis:")
    for i, polygon in enumerate(polygons):
        print(f"{i+1}. {polygon.name}")
    selected_indices = input("Selecione os polígonos que deseja processar (ex: 1,3,4): ").split(",")
    selected_polygons = [polygons[int(i)-1] for i in selected_indices]
    return selected_polygons

def associate_cogopoints_to_vertices(vertices: List, cogopoints: List):
    if not isinstance(vertices, list) or not isinstance(cogopoints, list):
        logger.error("Invalid argument type. Both vertices and cogopoints should be lists.")
        return

    if not vertices or not cogopoints:
        logger.warning("One or both of the lists are empty. Skipping association.")
        return

    for vertex in vertices:
        try:
            closest_cogopoint = min(cogopoints, key=lambda cp: calculate_distance(vertex, cp))
            vertex.cogopoint = closest_cogopoint
            vertex.id = vertex.generate_id()
        except Exception as e:
            logger.error(f"An error occurred while associating vertex and cogopoint: {e}")


