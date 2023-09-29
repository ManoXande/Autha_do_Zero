#autocad_interactions.py
from pyautocad import Autocad
from class_definitions import Vertex, Polygon, Cogopoint, Text
import logging

acad = Autocad()

def initialize_selection_set():
    try:
        logger = logging.getLogger('main')
        selectionSetName = 'SS1'
        selection_set = None

        logger.info("Checking existing selection sets...")
        for i in range(acad.ActiveDocument.SelectionSets.Count):
            if acad.ActiveDocument.SelectionSets.Item(i).Name == selectionSetName:
                selection_set = acad.ActiveDocument.SelectionSets.Item(i)
                break

        if selection_set is None:
            logger.info("Creating new selection set...")
            selection_set = acad.ActiveDocument.SelectionSets.Add(selectionSetName)
        else:
            logger.info("Clearing existing selection set...")
            selection_set.Clear()

        logger.info("Performing selection on screen...")
        selection_set.SelectOnScreen()
        
        return selection_set  # Make sure to return the selection_set object
    except Exception as e:
        logger.error(f"An error occurred while initializing the selection set: {e}")
        return []  # Return an empty list in case of an exception


def extract_coordinates(entity):
    try:
        if hasattr(entity, 'EntityName'):
            entity_name = entity.EntityName
            
            # Para polilinhas
            if entity_name == 'AcDbPolyline' and all(hasattr(entity, attr) for attr in ['Coordinates']):
                coords = [round(coord, 3) for coord in entity.Coordinates]
                vertices_groups = [(coords[i], coords[i+1]) for i in range(0, len(coords), 2)]
                return {'Type': 'Polyline', 'Coordinates': vertices_groups}
            
            # Para pontos Cogo
            elif entity_name == 'AeccDbCogoPoint' and all(hasattr(entity, attr) for attr in ['Easting', 'Northing', 'Elevation', 'RawDescription', 'Number']):
                properties = ['Easting', 'Northing', 'Elevation', 'RawDescription', 'Number']
                extracted_properties = {prop: round(float(getattr(entity, prop)), 3) if isinstance(getattr(entity, prop), float) else getattr(entity, prop) for prop in properties}
                return {'Type': 'CogoPoint', **extracted_properties}
            
            # Para texto
            elif entity_name in ['AcDbText', 'AcDbMText'] and all(hasattr(entity, attr) for attr in ['InsertionPoint', 'TextString']):
                x, y = entity.InsertionPoint[:2]
                content = entity.TextString
                return {'Type': 'Text', 'x': x, 'y': y, 'content': content}
            
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Exception caught: {e}")
        return None

def convert_polyline(data):
    vertices = [Vertex(x, y) for x, y in data['Coordinates']]
    return Polygon(vertices)

def convert_cogopoint(data):
    return Cogopoint(data['Easting'], data['Northing'], data['Elevation'], data['Number'], data['RawDescription'])

def convert_text(data):
    x, y = data['InsertionPoint']
    return Text(x, y, data['TextString'])

def fetch_polygons():
    selection_set = initialize_selection_set()
    return [entity for entity in read_entities_from_selection_set(selection_set) if isinstance(entity, Polygon)]

def fetch_cogopoints():
    selection_set = initialize_selection_set()
    return [entity for entity in read_entities_from_selection_set(selection_set) if isinstance(entity, Cogopoint)]

def fetch_texts():
    selection_set = initialize_selection_set()
    return [entity for entity in read_entities_from_selection_set(selection_set) if isinstance(entity, Text)]



git config --global user.email "cao.agrimensura@gmail.com"
  git config --global user.name "ManoXande"