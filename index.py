import requests
import json

accuweatherAPIKey = '7PGxc3bOpHnVxzfghpyyodewRAVG9sdG'

def getCoordinates():
    url_geoplugin  = 'http://www.geoplugin.net/json.gp'

    reqLocale = requests.get(url_geoplugin)

    if reqLocale.status_code != 200:
        print("Não foi possível obter a localização.")
    else:
        locale = json.loads(reqLocale.text)
        coordinates = {}
        coordinates['lat'] = locale['geoplugin_latitude']
        coordinates['long'] = locale['geoplugin_longitude']
        return coordinates

def getCurrentCode(lat, long):
    locationApi = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={accuweatherAPIKey}&q={lat}%2C{long}&language=pt-br"

    reqCodLocale = requests.get(locationApi)

    if reqCodLocale.status_code != 200:
        print("Não foi possível obter código do local.")
    else:
        locationResp = json.loads(reqCodLocale.text)
        infoLocal = {}
        
        infoLocal['localName'] = f"{locationResp['LocalizedName']}, {locationResp['AdministrativeArea']['LocalizedName']}/{locationResp['Country']['ID']}"
        infoLocal['localCode'] = locationResp['Key']

        return infoLocal

def getLocalWeather(localCode, localName):
    currentConditionUrl = f"http://dataservice.accuweather.com/currentconditions/v1/{localCode}?apikey={accuweatherAPIKey}&language=pt-br"

    reqCurrCondition = requests.get(currentConditionUrl)

    if reqCurrCondition.status_code != 200:
        print("Não foi possível obter o clima local.")
    else:
        currContionResp = json.loads(reqCurrCondition.text)
        infoWeather = {}
        
        infoWeather['weatherText'] = currContionResp[0]['WeatherText']
        infoWeather['temperature'] = currContionResp[0]['Temperature']['Metric']['Value']
        infoWeather['localName'] = localName
        
        return infoWeather

coordinates = getCoordinates()

local = getCurrentCode(coordinates['lat'], coordinates['long'])

weather =  getLocalWeather(local['localCode'], local['localName'])

print("Clima atual em: ", weather['localName'])
print(f"Clima atual: {weather['weatherText']}")
print(f"Temperatura: {weather['temperature']} \xb0C")
