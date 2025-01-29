import requests

def get_geolocation_ipinfo(ip):
    """Get geolocation for an IP using ipinfo.io API."""
    API_TOKEN = "***"  # Replace with your actual API token
    url = f"https://ipinfo.io/{ip}/json?token={API_TOKEN}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "ip": ip,
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country"),
            "latitude": data.get("loc").split(",")[0] if data.get("loc") else None,
            "longitude": data.get("loc").split(",")[1] if data.get("loc") else None
        }
    else:
        return {"ip": ip, "error": "Failed to retrieve data"}

