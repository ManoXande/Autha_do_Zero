#main.py
from autocad_interactions import fetch_texts, fetch_polygons, fetch_cogopoints
from class_definitions import Polygon, Text, Cogopoint
from configurations import set_coordinate_system, set_locale, set_rounding_rules
from debug_logs import setup_custom_logger
from report_generation import generate_description, generate_table
from utils import associate_names_to_polygons, user_select_polygons, identify_adjacent_polygons



# Setup logger
def main():
    logger = setup_custom_logger('main')
    try:
        # Initialize
        logger.info("Initializing...")
        set_locale('pt_BR')
        set_rounding_rules()
        
        # Fetching data from AutoCAD
        logger.info("Fetching data from AutoCAD...")
        polygons_data = fetch_polygons()
        if not polygons_data:
            logger.error("No polygon data found. Exiting.")
            return
        
        texts_data = fetch_texts()
        cogopoints_data = fetch_cogopoints()
        
        # Create Polygon, Text, and Cogopoint objects
        polygons = [Polygon(data) for data in polygons_data]
        texts = [Text(data) for data in texts_data]
        cogopoints = [Cogopoint(data) for data in cogopoints_data]
        
        # Associate names and Cogopoints to polygons
        associate_names_to_polygons(polygons, texts)
        
        # Allow the user to select polygons
        selected_polygons = user_select_polygons(polygons)
        
        # Identify adjacent polygons
        identify_adjacent_polygons(selected_polygons)
        
        # Generate reports
        for polygon in selected_polygons:
            desc = generate_description(polygon, 'EPSG:31982')
            table = generate_table(polygon)
            # Save or print the generated reports (desc and table)
        
        logger.info("Process completed.")
        
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
