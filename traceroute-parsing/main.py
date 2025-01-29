import glob
import json
import sys
import lib
from contextlib import redirect_stdout
from lib.Traceroute import RIPETraceroute
from requestGeo import get_geolocation_ipinfo

# Define the output file path
output_file_path = 'output.json'


ip_cache = {}

def get_geolocation_cached(ip):
    """Return geolocation from cache if available; otherwise, request from API."""
    if ip in ip_cache:
        return ip_cache[ip]  # Return cached result

    # Otherwise, make API request
    geolocation = get_geolocation_ipinfo(ip)  # Replace with actual API function

    # Store result in cache
    ip_cache[ip] = geolocation

    return geolocation

with open(output_file_path, "w") as output_file:
    all_traceroutes = []

    for tr_filename in glob.glob("*/*/*/*.json"):
        print(f"Processing {tr_filename}...")

        # Generate lines from the current JSON file
        for tr_line in lib.generate_lines(tr_filename):
            # Parse the JSON line into a RIPETraceroute object
            tr = RIPETraceroute(json.loads(tr_line))

            # Filter hops to remove unresponsive ones (***)
            filtered_hops = [hop for hop in tr.hops if hop.addr != "***"]

            # Get geolocation data for each valid hop, using caching
            geolocated_hops = [get_geolocation_cached(hop.addr) for hop in filtered_hops]

            # Store this traceroute as a separate path
            if geolocated_hops:
                all_traceroutes.append(geolocated_hops)

    json.dump(all_traceroutes, output_file, indent=4)

print(f"Geolocated data saved to {output_file_path}")