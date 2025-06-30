#!/usr/bin/env python3
import sys
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 + 
         math.cos(math.radians(lat1)) * 
         math.cos(math.radians(lat2)) * 
         math.sin(dlon/2)**2)
    return R * 2 * math.asin(math.sqrt(a))

if len(sys.argv) != 4:
    sys.exit("Usage: mapper.py <lat_center> <lon_center> <distance_km>")

lat_c, lon_c, max_dist = map(float, sys.argv[1:])

for line in sys.stdin:
    try:
        parts = line.strip().split(",")
        if len(parts) < 4:
            continue
        value = float(parts[1])
        lat = float(parts[2])
        lon = float(parts[3])
        distance = haversine(lat_c, lon_c, lat, lon)
        if distance <= max_dist:
            print(value)
    except Exception:
        continue