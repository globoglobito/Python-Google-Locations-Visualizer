import folium
import json
from pathlib import Path
import random

# Load your Google Location History data from the JSON file
file_path = Path("C:\\Users\\bruno\\Downloads\\Location History (Timeline)\\Records.json")
with file_path.open('r') as file:
    location_data = json.load(file)

# Define bounding box of the city of Madrid (approximate)
madrid_community_bbox = {
    'min_lat': 40.0,
    'max_lat': 40.9,
    'min_lon': -4.5,
    'max_lon': -3.0
}


# Filter locations within the city of Madrid using list comprehension
locations_in_madrid = [(loc['latitudeE7'] / 10**7, loc['longitudeE7'] / 10**7)
                            for loc in location_data.get('locations', [])
                            if madrid_community_bbox['min_lat'] <= loc.get('latitudeE7', 0) / 10**7 <= madrid_community_bbox['max_lat']
                            and madrid_community_bbox['min_lon'] <= loc.get('longitudeE7', 0) / 10**7 <= madrid_community_bbox['max_lon']]


# Sampling toggle
sample_size = -1  # Set to -1 to disable sampling, otherwise specify the sample size

if sample_size != -1 and len(locations_in_madrid) > sample_size:
    locations_in_madrid = random.sample(locations_in_madrid, sample_size)

# Calculate center of the city of Madrid
center_lat = (madrid_community_bbox['min_lat'] + madrid_community_bbox['max_lat']) / 2
center_lon = (madrid_community_bbox['min_lon'] + madrid_community_bbox['max_lon']) / 2

# Create map based on the value of static_map
static_map = 0  # Change this to 1 if you want a static map

if static_map != 1:
    # Create an interactive Folium map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, control_scale=True, max_bounds=True,
                   max_bounds_viscosity=1.0)  # Centered on the city of Madrid, limited to the bounds of the city of Madrid

    # Add CircleMarkers to represent sampled locations within the city of Madrid
    for lat, lon in locations_in_madrid:
        folium.CircleMarker(location=[lat, lon], radius=1, color='blue', fill=True, fill_color='blue').add_to(m)

    # Save map to HTML file
    m.save(f'location_history_interactive_map_madrid_sample{sample_size}.html', close_file=True)
else:
    # Create a static map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, control_scale=True, max_bounds=True,
                   max_bounds_viscosity=1.0)  # Centered on the city of Madrid, limited to the bounds of the city of Madrid

    # Add markers to the static map
    for lat, lon in locations_in_madrid:
        folium.Marker(location=[lat, lon], icon=folium.Icon(icon='circle', prefix='fa', icon_color='blue')).add_to(m)

    # Save static map to HTML file
    m.save('location_history_static_map_madrid.html', close_file=True)