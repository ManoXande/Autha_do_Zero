#autocad_interactions.py
from pyautocad import Autocad  # Assumindo que 'Autocad' é do pacote pyautocad
from class_definitions import Cogopoint, Polygon, Text, Vertex  # Assumindo que estas classes estão definidas em 'class_definitions.py'

acad = Autocad()

def initialize_selection_set():
    selectionSetName = 'SS1'
    selection_set = None

    for i in range(acad.ActiveDocument.SelectionSets.Count):
        if acad.ActiveDocument.SelectionSets.Item(i).Name == selectionSetName:
            selection_set = acad.ActiveDocument.SelectionSets.Item(i)
            break

    if selection_set is None:
        selection_set = acad.ActiveDocument.SelectionSets.Add(selectionSetName)
    else:
        selection_set.Clear()

    selection_set.SelectOnScreen()
    return selection_set

def read_entities_from_selection_set(selection_set):
    entities = []
    try:
        for entity in selection_set:
            entity_data = extract_coordinates(entity)
            if entity_data:
                if entity_data['Type'] == 'Polyline':
                    entities.append(convert_polyline(entity_data))
                elif entity_data['Type'] == 'CogoPoint':
                    entities.append(convert_cogopoint(entity_data))
                elif entity_data['Type'] == 'Text':
                    entities.append(convert_text(entity_data))
        return entities
    except Exception as e:
        print(f"An error occurred while fetching entities: {e}")
        return []

def extract_coordinates(entity):
    try:
        entity_name = entity.EntityName
        if entity_name == 'AcDbPolyline':
            coords = [round(coord, 3) for coord in entity.Coordinates]
            vertices_groups = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
            return {'Type': 'Polyline', 'Coordinates': vertices_groups}
        elif entity_name == 'AeccDbCogoPoint':
            properties = ['Easting', 'Northing', 'Elevation', 'RawDescription', 'Number']
            extracted_properties = {prop: round(float(getattr(entity, prop)), 3) if isinstance(getattr(entity, prop), float) else getattr(entity, prop) for prop in properties}
            return {'Type': 'CogoPoint', **extracted_properties}
        elif entity_name == 'AcDbText' or entity_name == 'AcDbMText':
            properties = ['InsertionPoint', 'TextString']
            extracted_properties = {prop: getattr(entity, prop) for prop in properties}
            extracted_properties['InsertionPoint'] = tuple(round(coord, 3) for coord in extracted_properties['InsertionPoint'][:2])
            return {'Type': 'Text', **extracted_properties}
        else:
            return None
    except Exception as e:
        print(f"Exception caught: {e}")  # Debugging line
        raise e

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