#report_generation.py
from jinja2 import Environment, FileSystemLoader
import configurations
import utils

env = Environment(loader=FileSystemLoader('./templates'))

rounding_rules = configurations.ROUNDING_RULES
default_memorial_template = configurations.DEFAULT_MEMORIAL_TEMPLATE
default_table_template = configurations.DEFAULT_TABLE_TEMPLATE

azimuth_gms = utils.azimuth_to_gms(...)


def load_template(template_type, template_name):
    return env.get_template(f"{template_name}_{template_type}.jinja2")

def generate_description(polygon, system_of_coordinates):
    descriptions = []
    template_initial = load_template('initial', DEFAULT_MEMORIAL_TEMPLATE)
    template_other = load_template('other', DEFAULT_MEMORIAL_TEMPLATE)
    template_final = load_template('final', DEFAULT_MEMORIAL_TEMPLATE)
    
    for i, edge in enumerate(polygon.edges):
        # Convertendo o azimute para o formato GMS e arredondando
        degrees, minutes, seconds = azimuth_to_gms(round(edge.azimuth, ROUNDING_RULES.get("azimuths", 2)))
        
        # Arredondando as distâncias
        distance = round(edge.distance, ROUNDING_RULES.get("distances", 2))
        
        context = {
            "current_vertex_name": edge.start_vertex.id,
            "current_vertex": (round(edge.start_vertex.x, ROUNDING_RULES.get("coordinates", 3)), 
                               round(edge.start_vertex.y, ROUNDING_RULES.get("coordinates", 3))),
            "current_vertex_elevation": round(edge.start_vertex.z, ROUNDING_RULES.get("coordinates", 3)),
            "adjacent_text": edge.adjacent_polygon,
            "degrees": degrees,
            "minutes": minutes,
            "seconds": seconds,
            "distance": distance,
            "next_vertex_name": edge.end_vertex.id,
            "next_vertex": (round(edge.end_vertex.x, ROUNDING_RULES.get("coordinates", 3)), 
                            round(edge.end_vertex.y, ROUNDING_RULES.get("coordinates", 3))),
            "next_vertex_elevation": round(edge.end_vertex.z, ROUNDING_RULES.get("coordinates", 3))
        }
        
        if i == 0:
            description = template_initial.render(context)
        else:
            description = template_other.render(context)
        
        descriptions.append(description)
    
    final_context = {
        "system_of_coordinates": system_of_coordinates
    }
    
    final_description = template_final.render(final_context)
    descriptions.append(final_description)
    
    return "\n".join(descriptions)

def generate_table(polygon):
    table_rows = []
    template_table = load_template('table', DEFAULT_TABLE_TEMPLATE)
    
    for edge in polygon.edges:
        # Arredondando as distâncias e azimutes
        distance = round(edge.distance, ROUNDING_RULES.get("distances", 2))
        azimuth = round(edge.azimuth, ROUNDING_RULES.get("azimuths", 2))
        
        # Convertendo o azimute para graus, minutos e segundos
        degrees = int(azimuth)
        minutes = int((azimuth - degrees) * 60)
        seconds = ((azimuth - degrees) * 60 - minutes) * 60
        
        context = {
            "current_vertex_name": edge.start_vertex.id,
            "current_vertex": (
                round(edge.start_vertex.x, ROUNDING_RULES.get("coordinates", 3)),
                round(edge.start_vertex.y, ROUNDING_RULES.get("coordinates", 3)),
                round(edge.start_vertex.z, ROUNDING_RULES.get("coordinates", 3))
            ),
            "next_vertex_name": edge.end_vertex.id,
            "next_vertex": (
                round(edge.end_vertex.x, ROUNDING_RULES.get("coordinates", 3)),
                round(edge.end_vertex.y, ROUNDING_RULES.get("coordinates", 3)),
                round(edge.end_vertex.z, ROUNDING_RULES.get("coordinates", 3))
            ),
            "distance": distance,
            "degrees": degrees,
            "minutes": minutes,
            "seconds": seconds
        }
        
        table_row = template_table.render(**context)
        table_rows.append(table_row)
    
    return "\n".join(table_rows)

