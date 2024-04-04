import folium
import json
from pathlib import Path
import random

def load_location_data(file_path):
    with file_path.open('r') as file:
        return json.load(file)

def filter_locations(location_data, bbox):
    return [(loc['latitudeE7'] / 10**7, loc['longitudeE7'] / 10**7)
            for loc in location_data.get('locations', [])
            if bbox['min_lat'] <= loc.get('latitudeE7', 0) / 10**7 <= bbox['max_lat']
            and bbox['min_lon'] <= loc.get('longitudeE7', 0) / 10**7 <= bbox['max_lon']]

def create_map(locations, center, sample_size=-1):
    if sample_size != -1 and len(locations) > sample_size:
        locations = random.sample(locations, sample_size)
    
    m = folium.Map(location=center, zoom_start=12, control_scale=True, max_bounds=True,
                   max_bounds_viscosity=1.0)
    
    for lat, lon in locations:
        folium.CircleMarker(location=[lat, lon], radius=1, color='blue', fill=True, fill_color='blue').add_to(m)
    
    return m

def create_static_map(locations, center):
    m = folium.Map(location=center, zoom_start=12, control_scale=True, max_bounds=True,
                   max_bounds_viscosity=1.0)
    
    for lat, lon in locations:
        folium.Marker(location=[lat, lon], icon=folium.Icon(icon='circle', prefix='fa', icon_color='blue')).add_to(m)
    
    return m

def main():
    # Load your Google Location History data from the JSON file
    file_path = Path("C:PATH TO SOURCE FILE")
    location_data = load_location_data(file_path)

    # Define bounding box of the city of Madrid (approximate)
    madrid_community_bbox = {
        'min_lat': 40.0,
        'max_lat': 40.9,
        'min_lon': -4.5,
        'max_lon': -3.0
    }

    # Filter locations within the city of Madrid
    locations_in_madrid = filter_locations(location_data, madrid_community_bbox)

    # Sampling toggle
    sample_size = -1  # Set to -1 to disable sampling, otherwise specify the sample size

    # Calculate center of the city of Madrid
    center_lat = (madrid_community_bbox['min_lat'] + madrid_community_bbox['max_lat']) / 2
    center_lon = (madrid_community_bbox['min_lon'] + madrid_community_bbox['max_lon']) / 2
    center = [center_lat, center_lon]

    # Create map based on the value of static_map
    static_map = 0  # Change this to 1 if you want a static map

    if static_map != 1:
        m = create_map(locations_in_madrid, center, sample_size)
        m.save(f'location_history_interactive_map_madrid_sample{sample_size}.html', close_file=True)
    else:
        m = create_static_map(locations_in_madrid, center)
        m.save('location_history_static_map_madrid.html', close_file=True)

if __name__ == "__main__":
    main()
