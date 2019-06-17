# Housing information retrieval system of registered MLS Listings in the GTA
# Full stack application available upon request
# ~~
# Run with Python3
# Respoken by Kamran Choudhry

import geocoder
import requests
import unicodecsv as csv
import time

container = {}
g = geocoder.ip('me')           # current location using local ip

# hardcoded coordinates for the GTA
LongitudeMin = 43.484288
LongitudeMax = 43.697341
LatitudeMin = -79.825757
LatitudeMax = -79.539214

url = "https://www.realtor.ca/api/Listing.svc/PropertySearch_Post"              # API Deprecated

PropertySearchType = {
    1: "Residential",
    2: "Recreational",
    3: "Condo/Strata",
    8: "Multi Family",
    4: "Agriculture",
    5: "Parking",
    6: "Vacant Land"
}

LandSizeRange = ["0-10", "10-50", "50-100", "100-320", "320-640", "640-1000", "1000-0"]
interval = 250000
intervals = 2
max_results = 200

for PropertySearch in PropertySearchType.keys():
    Prices = list((i * interval, i * interval + interval) for i in range(intervals))
    for PriceMin, PriceMax in Prices:
        print('Looking for {} ({}$-{}$)...'.format(
            PropertySearchType[PropertySearch],
            PriceMin,
            PriceMax
        ))
        payload = {
            "CultureId": "1",
            "ApplicationId": "1",
            "RecordsPerPage": max_results,
            "MaximumResults": max_results,
            "PropertySearchTypeId": PropertySearch,
            "PriceMin": PriceMin,
            "PriceMax": PriceMax,
            "LandSizeRange": "0-0",
            "TransactionTypeId": "2",
            "StoreyRange": "0-0",
            "BedRange": "0-0",
            "BathRange": "0-0",
            "LongitudeMin": LongitudeMin,
            "LongitudeMax": LongitudeMax,
            "LatitudeMin": LatitudeMin,
            "LatitudeMax": LatitudeMax,
            "SortOrder": "A",
            "SortBy": "1",
            "viewState": "m",
            "Longitude": g.lng,
            "Latitude": g.lat,
            "ZoomLevel": "8",
        }
        while True:
            try:
                r = requests.post(url, data=json.dumps(payload))
                break
            except:
                print(PriceMin, PriceMax)
                time.sleep(1)
                print('Connection Failed...')
                pass
        if r.ok:
            results = r.json()['Results']
            print('Found {} results!'.format(len(results)))
            if len(results) == max_results:
                half = (PriceMax - PriceMin) / 2
                Prices.append([PriceMin, int(PriceMin + half)])
                Prices.append([int(PriceMin + half), PriceMax])
                print('Price split {}$-{}$'.format(PriceMin, PriceMax))
                
            for result in results:
                data = {
                    'lng': result['Property']['Address']['Longitude'],
                    'lat': result['Property']['Address']['Latitude'],
                    'address': result['Property']['Address']['AddressText'],
                    'postal': result['PostalCode'],
                    'property_type': result['Property']['Type'],
                    'price': result['Property']['Price'],
                    'mls': result['MlsNumber'],
                    'bathrooms': result['Building'].get('BathroomTotal', 0),
                    'bedrooms': result['Building'].get('Bedrooms', 0),
                    'PriceMin': payload['PriceMin'],
                    'PriceMax': payload['PriceMax'],
                    'PropertySearch': PropertySearchType[PropertySearch],
                    'LandSize': result['Land'].get('SizeTotal'),
                    'url': 'https://www.realtor.ca' + result['RelativeDetailsURL']
                }
                container[result['MlsNumber']] = data
                #print(data['address'])

#with open('mls.csv', 'wb') as f:
   # writer = csv.DictWriter(f, fieldnames=next(iter(container.values())), dialect='excel')
   # writer.writeheader()
   # for row in container.values():
       # writer.writerow(row)
print(container.values())
