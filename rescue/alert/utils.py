import math
from django.db.models import F
from .models import Alert  # Assuming your department model is named Department

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371  # Radius of Earth in kilometers
    return r * c

def calculate_nearest_department(user_location):
    user_lat = user_location['latitude']
    user_lon = user_location['longitude']

    # Calculate the distances from the user's location to all departments in the database
    departments = Alert.objects.annotate(
        distance=haversine(
            user_lat, user_lon, F('latitude'), F('longitude')
        )
    ).order_by('distance')

    # Get the nearest department
    nearest_department = departments.first()

    return nearest_department
