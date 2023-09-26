from pyautocad import Autocad, APoint  # Assuming you're using pyautocad
from class_definitions import Vertex, Polygon, Text, Cogopoint
from debug_logs import log
from common_utils import custom_round, calculate_distance, calculate_azimuth

acad = Autocad()

def read_polylines():
    polylines = []
    for entity in acad.iter_objects('Polyline'):
        vertices = []
        is_closed = entity.is_closed  # Verifica se a polilinha é fechada
        for i in range(entity.Count):
            point = entity.GetPoint(i)
            vertex = Vertex(point.x, point.y, point.z)
            vertices.append(vertex)
        polygon = Polygon(vertices, is_closed=is_closed)
        polylines.append(polygon)
    log(f"{len(polylines)} polylines read from AutoCAD.")
    return polylines

def associate_cogopoints_to_vertices(vertices, cogopoints):
    # Esboço da função para associar COGO Points aos vértices
    pass

def read_texts():
    texts = []
    # Sample code to read text and mtext from AutoCAD using pyautocad
    for entity in acad.iter_objects(['Text', 'MText']):
        point = APoint(entity.InsertionPoint)
        text = Text(point.x, point.y, entity.TextString)
        texts.append(text)
    log(f"{len(texts)} texts read from AutoCAD.")
    return texts

def read_cogopoints():
    cogopoints = []
    for entity in acad.iter_objects('Point'):
        point_number = entity.GetAttribute("PointNumber")
        description = entity.GetAttribute("Description")
        cogopoint = Cogopoint(entity.x, entity.y, entity.z, point_number, description)
        cogopoints.append(cogopoint)
    log(f"{len(cogopoints)} COGO Points read from AutoCAD.")
    return cogopoints

# Additional functions like write_to_autocad() can be added here as well.
