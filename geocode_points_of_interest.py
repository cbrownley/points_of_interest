#!/Users/clinton/anaconda/envs/geo/bin/python
from geopy.geocoders import GoogleV3, Nominatim
from geopy.exc import GeocoderTimedOut

import pandas as pd

google_locator = GoogleV3(api_key="AIzaSyDTjpk83jIE__CRUhdrtx28veVBgbvtoW8")

def geocode_address(address, geolocator):
    """Geocode an address using the Google Maps v3 API\nhttps://developers.google.com/maps/documentation/geocoding/"""
    # https://stackoverflow.com/questions/27914648/geopy-catch-timeout-error
    try:
        location = geolocator.geocode(address, exactly_one=True, timeout=5)
    except GeocoderTimedOut as e:
        print("GeocoderTimedOut: geocode failed on input %s with message %s" % (address, e.msg))
    except AttributeError as e:
        print("AttributeError: geocode failed on input %s with message %s" % (address, e.msg))
    if location:
        address_geo = location.address
        latitude = location.latitude
        longitude = location.longitude
        return address_geo, latitude, longitude
    else:
        print("Geocoder couldn't geocode the following address: %s" % address)


def convert_state_to_two_letter(state_abbreviation):
    if state_abbreviation == 'California':
        state_abbreviation = 'CA'
    if state_abbreviation == 'Idaho':
        state_abbreviation = 'ID'
    if state_abbreviation == 'Boulder' or state_abbreviation == 'Tahoe,':
        state_abbreviation = 'NV'
    else:
        state_abbreviation = state_abbreviation
    return state_abbreviation


df = pd.read_json('western_attractions/western_attractions.json', orient='records')
df['state'] = df['address'].apply(lambda address: convert_state_to_two_letter(address.split()[-2]))

geo_results = []
for index, row in df.iterrows():
    #if index < 4:
    try:
        result = geocode_address(row.loc['address'], google_locator)
        d = {'index': index, 'address_geo': result[0], 'latitude': result[1], 'longitude': result[2]}
        if d['address_geo'] is not None:
            geo_results.append(d)
            print(d)
    except:
        print(row)
        continue

# http://pbpython.com/pandas-list-dict.html
geo = pd.DataFrame(geo_results)
geo.set_index('index', inplace=True)

df_geo = df.merge(geo, how='inner', left_index=True, right_index=True)

df_geo.to_csv('western_attractions_geocoded.csv', index=False)
df_geo.to_json('western_attractions_geocoded.json', orient='records')
