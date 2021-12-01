""" 
Snippet to remove and move selected attributes in a json string

Input: File containing Json string in the following format:
{'type': 'FeatureCollection',
 'features': [
  {'type': 'Feature',
  'properties': {'GEO_ID': '0500000US01017',
    'STATE': '01',
    'COUNTY': '017',
    'NAME': 'Chambers',
    'LSAD': 'County',
    'CENSUSAREA': 596.531},
  'geometry': {'type': 'Polygon',
    'coordinates': [[[-85.184131, 32.870525],
      [-85.123421, 32.772248],
      [-85.13204, 32.764211],
      [-85.136776, 32.746512],
      [-85.285043, 32.730731],
      [-85.593151, 32.72853],
      [-85.593177, 33.10734],
      [-85.232378, 33.108077],
      [-85.223261, 33.06258],
      [-85.221868, 33.055538],
      [-85.184131, 32.870525]]]},
  'id': '01017'},
  {...},
  ...]}

Requirement: 
1. Remove a give list of attributes (e.g. GEO_ID, STATE, COUNTY etc.)
2. Move key value pairs for 'geometry' and 'id' into 'properties'
3. Save a subset of entries in a new file
"""

import json

# Open file for read
with open('data.json') as data_file:
    data = json.load(data_file)

# List of attributes to be removed
lstAttrRem = ['GEO_ID','STATE', 'COUNTY', 'NAME', 'LSAD', 'CENSUSAREA']

# List of attributes to be removed
lstAttrMov = ['id', 'geometry']

for prop in data['features']:
  # Remove attributes
    for attr in lstAttrRem:
        if attr in prop['properties']:
            del prop['properties'][attr]
  
  # Move attributes
    for attr in lstAttrMov:
        prop['properties'][attr] = prop[attr]
        del prop[attr]

# Create new json with require subset
newJson = {'type': 'FeatureCollection'}
newJsonLst = []

# List of ids for the subset to be saved
lstId = ['01017','01001','01045','01083']

for prop in data['features']:
    if prop['properties']['id'] in lstId:
        newJsonLst.append(prop)

newJson['features'] = newJsonLst

# Save file
with open('geojson-counties-fips-mod.json', 'w') as data_file:
    data = json.dump(data, data_file)