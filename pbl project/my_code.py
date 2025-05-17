from mypackage.location import get_current_location
from mypackage.dijkstraalgo import custom_dijkstra
import osmnx as ox
import folium

def create_map(center):
    return folium.Map(location=center, zoom_start=14)

def add_route_to_map(m, G, path, user_coords, dest_coords, dest_name):
    folium.Marker(
        location=dest_coords,
        popup=dest_name,
        icon=folium.Icon(color='red')
    ).add_to(m)

    route_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in path]
    folium.PolyLine(
        route_coords,
        color="green",
        weight=4,
        popup=dest_name
    ).add_to(m)

def get_street_graph(center_point, dist=2000):
    return ox.graph_from_point(center_point, dist=dist, network_type='drive')

def get_nearby_amenities(center_point):
    tags = {
        'amenity': ['restaurant', 'cafe'],
        'tourism': ['hotel', 'motel', 'guest_house']
    }
    pois = ox.features_from_point(center_point, tags=tags, dist=2000)
    pois = pois[pois.geometry.geom_type == 'Point']
    return pois

def get_nearest_node(G, point):
    return ox.distance.nearest_nodes(G, point[1], point[0])

user_coords = get_current_location()
print(f"User Location: {user_coords}")

G = get_street_graph(user_coords)

pois = get_nearby_amenities(user_coords)

if pois.empty:
    print("No nearby destinations found within 2 km.")
    exit()


route_map = create_map(user_coords)
folium.Marker(
    location=user_coords,
    popup="You",
    icon=folium.Icon(color='blue')
).add_to(route_map)

origin_node = get_nearest_node(G, user_coords)


for i, (_, poi) in enumerate(pois.iterrows()):
    try:
        poi_point = (poi.geometry.y, poi.geometry.x)
        dest_node = get_nearest_node(G, poi_point)
        path = custom_dijkstra(G, origin_node, dest_node)

        name = poi.get("name") or poi.get("amenity") or poi.get("tourism") or f"POI {i+1}"
        dest_name = str(name)

        add_route_to_map(route_map, G, path, user_coords, poi_point, dest_name)

    except Exception as e:
        print(f"Skipping POI {i+1} due to error: {e}")

route_map.save("all_routes.html")
print("✅ Saved: all_routes.html")
