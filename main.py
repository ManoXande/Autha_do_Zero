#main.py
import autocad_interactions
import class_definitions
import configurations
import debug_logs
import report_generation
import utils

texts = autocad_interactions.fetch_texts(...)
polygons = autocad_interactions.fetch_polygons(...)
cogopoints = autocad_interactions.fetch_cogopoints(...)

polygon = class_definitions.Polygon(...)
text = class_definitions.Text(...)
cogopoint = class_definitions.Cogopoint(...)

configurations.set_locale(...)
configurations.set_rounding_rules(...)

logger = debug_logs.setup_custom_logger(...)

description = report_generation.generate_description(...)
table = report_generation.generate_table(...)

utils.associate_names_to_polygons(...)
utils.user_select_polygons(...)
utils.identify_adjacent_polygons(...)

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
