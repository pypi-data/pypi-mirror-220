import googlemaps

def getGeodataByAddress(location, google_key, components=None):
  gmaps = googlemaps.Client(key=google_key)
  geocode_result = gmaps.geocode(location, language='de_DE', components=components)
  #print(geocode_result)
  if len(geocode_result) == 0:
    return{"type":"error","error":"Warning: Location \""+location+"\" not found. Continue but skipping job...\n"}

  for address in geocode_result:

    # get address components country, state, city from address
    for address_component in address['address_components']:
      if 'country' in address_component['types']:
        country_short = address_component['short_name']
        country_long = address_component['long_name']
      
      if 'administrative_area_level_1' in address_component['types']:
        state_short = address_component['short_name']
        state_long = address_component['long_name']
      
      if 'locality' in address_component['types']:
        city_short = address_component['short_name']
        city_long = address_component['long_name']
      
      if 'sublocality' in address_component['types']:
        sublocality_short = address_component['short_name']
        sublocality_long = address_component['long_name']
    
    if 'country' in address['types']: # it's an address of a country
      return {"type":"country","country_short":country_short, "country_long":country_long, "state_short":"", "state_long":"", "city":""}

    if 'administrative_area_level_1' in address['types']:
      return {"type":"state", "country_short":country_short, "country_long":country_long, "state_short":state_short, "state_long":state_long, "city":""}

    if 'locality' in address['types'] or 'establishment' in address['types'] or 'postal_code' in address['types']: # it's an address of a city
      return {"type":"city", "country_short":country_short, "country_long":country_long, "state_short":state_short, "state_long":state_long, "city":city_long}

    if 'sublocality' in address['types']: # it's a town
      return {"type":"city", "country_short":country_short, "country_long":country_long, "state_short":state_short, "state_long":state_long, "city":sublocality_long}

    """
    for address_component in address['address_components']:
      if 'country' in address_component['types']: # it's a country
        return {"type":"country","country_short":address['address_components'][0]['short_name'], "country_long":address['address_components'][0]['long_name'], "state_short":"", "state_long":"", "city":""}
      
      if 'administrative_area_level_1' in address_component['types']: # state
        if 'administrative_area_level_2' in address['address_components'][1]['types']: # special state like Basel-Stadt and Basel-Landschaft, we need to get the country information one level deeper
          return {"type":"state", "country_short":address['address_components'][2]['short_name'], "country_long":address['address_components'][2]['long_name'], "state_short":address['address_components'][0]['short_name'], "state_long":address['address_components'][0]['long_name'], "city":""}
        else:
          return {"type":"state", "country_short":address['address_components'][1]['short_name'], "country_long":address['address_components'][1]['long_name'], "state_short":address['address_components'][0]['short_name'], "state_long":address['address_components'][0]['long_name'], "city":""}
      
      if 'locality' in address_component['types']: # it's a city
        return {"type":"city", "country_short":address['address_components'][3]['short_name'], "country_long":address['address_components'][3]['long_name'], "state_short":address['address_components'][2]['short_name'], "state_long":address['address_components'][2]['long_name'], "city":address['address_components'][0]['long_name']}

      if 'postal_code' in address_component['types']: 
        return {"type":"city", "country_short":address['address_components'][4]['short_name'], "country_long":address['address_components'][4]['long_name'], "state_short":address['address_components'][3]['short_name'], "state_long":address['address_components'][3]['long_name'], "city":address['address_components'][1]['long_name']}
    """
  return{"type":"error","error":"Warning: No matching types found for \""+location+"\" . Continue but skipping job...\n"}