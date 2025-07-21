# filepath: /home/mcuser/Mother/scripts/generate_map.py
import folium
import os

# Center the map (latitude, longitude)
m = folium.Map(location=[51.5, -0.1], zoom_start=12)

# Optionally add a marker
folium.Marker([51.5, -0.1], popup="Center").add_to(m)

# Save to map.html in the same directory as your GUI script
map_path = os.path.join(os.path.dirname(__file__), "map.html")
m.save(map_path)