from autocad_interactions import fetch_polygons, fetch_texts, fetch_cogopoints
from polygon import Polygon
from text import Text
from cogopoint import Cogopoint
from locale_utils import set_locale
from rounding_rules import set_rounding_rules
from logger_utils import setup_custom_logger
from polygon_utils import associate_names_to_polygons
from user_interaction import user_select_polygons
from adjacent_polygons import identify_adjacent_polygons
from report_utils import generate_description, generate_table
from systems_of_coordinates import SYSTEMS_OF_COORDINATES

# Setup logger
logger = setup_custom_logger('main')

def main():
    # Initialize
    logger.info("Initializing...")
    set_locale('pt_BR')
    set_rounding_rules()
    
    # Fetching data from AutoCAD
    logger.info("Fetching data from AutoCAD...")
    polygons_data = fetch_polygons()
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
        desc = generate_description(polygon, SYSTEMS_OF_COORDINATES['EPSG:31982'])
        table = generate_table(polygon)
        # Save or print the generated reports (desc and table)
    
    logger.info("Process completed.")

if __name__ == "__main__":
    main()
