from autocad_interactions import initialize_selection_set, extract_coordinates
from class_definitions import Polygon, Text, Cogopoint, Edge, Vertex
from configurations import set_locale, set_rounding_rules
from debug_logs import setup_custom_logger
from report_generation import generate_description, generate_table
from utils import associate_names_to_polygons, user_select_polygons, identify_adjacent_polygons

def main():
    # Initialize Logger and Environment
    logger = setup_custom_logger('main')
    
    try:
        logger.info("Initializing...")
        set_locale('pt_BR')
        set_rounding_rules()
        
        # Initialize Selection Set and Fetch Data
        logger.info("Initializing selection set...")
        selection_set = initialize_selection_set()
        
        logger.info("Extracting entities...")
        polygons = []
        texts = []
        cogopoints = []
        
        if selection_set is not None:
            for entity in selection_set:
                entity_data = extract_coordinates(entity)
                if entity_data:
                    print(f"Debug: Entity data is {entity_data}")  # Debugging line
                    
                    if entity_data['Type'] == 'Polyline':
                        polygons.append(Polygon(entity_data))
                    elif entity_data['Type'] == 'CogoPoint':
                        cogopoint_data = {
                            'x': entity_data.get('Easting'),
                            'y': entity_data.get('Northing'),
                            'z': entity_data.get('Elevation'),
                            'point_number': entity_data.get('Number'),
                            'description': entity_data.get('RawDescription'),
                        }
                        cogopoints.append(Cogopoint(**cogopoint_data))
                    elif entity_data['Type'] == 'Text':
                        entity_data_filtered = {key: entity_data[key] for key in entity_data if key != 'Type'}
                        texts.append(Text(**entity_data_filtered))

        if polygons and cogopoints:
            print(f"Debug: Polygons data is {polygons}")  # Debugging line
            print(f"Debug: Cogopoints data is {cogopoints}")  # Debugging line
            associate_cogopoints_to_vertices(polygons, cogopoints)
        else:
            logger.warning("Skipping associate_cogopoints_to_vertices due to missing data.")
        
        logger.info("Associating names and Cogopoints to polygons...")
        associate_names_to_polygons(polygons, texts)
        
        logger.info("Allowing user to select polygons...")
        selected_polygons = user_select_polygons(polygons)
        
        logger.info("Identifying adjacent polygons...")
        print(f"Debug: Selected Polygons data is {selected_polygons}")
        identify_adjacent_polygons(selected_polygons)
        
        logger.info("Generating reports...")
        for polygon in selected_polygons:
            desc = generate_description(polygon, 'EPSG:31982')
            table = generate_table(polygon)
            
            print("Generated Memorial:")
            print(desc)
            print("Generated Table:")
            print(table)
        
        logger.info("Process completed.")
        
    except Exception as e:  # Now this is correctly placed
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

  