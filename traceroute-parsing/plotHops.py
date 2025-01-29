import json
import folium
from folium.plugins import PolyLineTextPath

# Load geolocated traceroutes
input_file_path = "output.json"

with open(input_file_path, "r") as file:
    all_traceroutes = json.load(file)

# Initialize a folium map
hop_map = folium.Map(location=[0, 0], zoom_start=2)

# Define Morandi color palette
colors = ["#c0cad1", "#b5bdb2", "#c7c1c9", "#a27678", "#e7d9d6"]

# Add paths for each traceroute separately
for index, traceroute in enumerate(all_traceroutes):
    path_coordinates = []  # Store lat/lon for drawing animated paths
    
    for hop in traceroute:
        if hop["latitude"] and hop["longitude"]:  # Ensure valid coordinates
            lat, lon = float(hop["latitude"]), float(hop["longitude"])
            path_coordinates.append([lat, lon])

            # Add marker for the hop
            folium.Marker(
                location=[lat, lon],
                popup=f"IP: {hop['ip']}, {hop.get('city', 'Unknown')}, {hop.get('country', 'Unknown')}",
                tooltip=hop["ip"]
            ).add_to(hop_map)

    # Draw ONLY animated arrows between hops (no static lines)
    if len(path_coordinates) > 1:
        # Select a Morandi color based on the traceroute index
        path_color = colors[index % len(colors)]

        # Add moving arrows along the path (no PolyLine)
        PolyLineTextPath(
            folium.PolyLine(
                locations=path_coordinates,
                color=path_color,
                weight=0,
                opacity=1  # Slight transparency
            ).add_to(hop_map),
            ">",
            repeat=True,  # Continuously moving arrows
            offset=15,
            attributes={"fill": path_color, "font-size": "8"}
        ).add_to(hop_map)

# Save the map as an HTML file
map_file = "traceroute_paths.html"
hop_map.save(map_file)

print(f"Traceroute map with only moving arrows saved as {map_file}. Open it in your browser.")
