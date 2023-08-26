import requests
import json
from datetime import date

accuweatherAPIKey = '7PGxc3bOpHnVxzfghpyyodewRAVG9sdG'

daysOfTheWeek = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']

def getCoordinates():
    url_geoplugin  = 'http://www.geoplugin.net/json.gp'

    reqLocale = requests.get(url_geoplugin)

    if reqLocale.status_code != 200:
        print("Não foi possível obter a localização.")
        return None
    else:
        try:
            locale = json.loads(reqLocale.text)
            coordinates = {}
            coordinates['lat'] = locale['geoplugin_latitude']
            coordinates['long'] = locale['geoplugin_longitude']
            return coordinates
        except:
            return None

def getCurrentCode(lat, long):
    locationApi = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={accuweatherAPIKey}&q={lat}%2C{long}&language=pt-br"

    reqCodLocale = requests.get(locationApi)

    if reqCodLocale.status_code != 200:
        print("Não foi possível obter código do local.")
        return None
    else:
        try: 
            locationResp = json.loads(reqCodLocale.text)
            infoLocal = {}
            
            infoLocal['localName'] = f"{locationResp['LocalizedName']}, {locationResp['AdministrativeArea']['LocalizedName']}/{locationResp['Country']['ID']}"
            infoLocal['localCode'] = locationResp['Key']

            return infoLocal
        except: 
            return None

def getLocalWeather(localCode, localName):
    currentConditionUrl = f"http://dataservice.accuweather.com/currentconditions/v1/{localCode}?apikey={accuweatherAPIKey}&language=pt-br"

    reqCurrCondition = requests.get(currentConditionUrl)

    if reqCurrCondition.status_code != 200:
        print("Não foi possível obter o clima atual.")
        return None
    else:
        try: 
            currContionResp = json.loads(reqCurrCondition.text)
            infoWeather = {}
            
            infoWeather['weatherText'] = currContionResp[0]['WeatherText']
            infoWeather['temperature'] = currContionResp[0]['Temperature']['Metric']['Value']
            infoWeather['localName'] = localName
            
            return infoWeather
        except: 
            return None

def getFiveDayWeather(localCode):
    dailyAPIUrl = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{localCode}?apikey={accuweatherAPIKey}&language=pt-br&metric=true"

    reqCurrCondition = requests.get(dailyAPIUrl)

    if reqCurrCondition.status_code != 200:
        print("Não foi possível obter o clima atual.")
        return None
    else:
        try: 
            dailyResp = json.loads(reqCurrCondition.text)
            infoFiveDaysWeather = []

            for day in dailyResp['DailyForecasts']:
                dayWeather = {}
                dayWeather['max'] = day['Temperature']['Maximum']['Value']
                dayWeather['min'] = day['Temperature']['Minimum']['Value']
                dayWeather['weather'] = day['Day']['IconPhrase']
                weekDay = int(date.fromtimestamp(day['EpochDate']).strftime('%w'))
                dayWeather['day'] = daysOfTheWeek[weekDay]

                infoFiveDaysWeather.append(dayWeather)
            return infoFiveDaysWeather
        except: 
            return None

def viewInfoWeekWeather():
    fiveDayForecast = getFiveDayWeather(local['localCode'])
    for day in fiveDayForecast:
        print(day['day'])
        print(f"Mínima: {day['min']} \xb0C")
        print(f"Máxima: {day['max']} \xb0C")
        print(f"Clima: {day['weather']}")
        print("--------------------------------")


try:
    coordinates = getCoordinates()
    local = getCurrentCode(coordinates['lat'], coordinates['long'])
    weather =  getLocalWeather(local['localCode'], local['localName'])
    print("Clima atual em: ", weather['localName'])
    print(f"Clima atual: {weather['weatherText']}")
    print(f"Temperatura: {weather['temperature']} \xb0C")
    print("\n Clima para hoje e para os próximos dias: \n")
    viewInfoWeekWeather()

except:
    print("Erro ao processar a solicitação.")