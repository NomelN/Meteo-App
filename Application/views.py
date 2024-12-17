from django.shortcuts import render
import requests
import datetime
from MeteoApp import settings


# Create your views here.
def index(request):
    API_KEY = settings.METEO_API_KEY
    current_weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={{}}&appid={API_KEY}'
    forecast_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={{lat}}&lon={{lon}}&exclude=current,minutely,hourly,alerts&appid={API_KEY}'
    
    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    
        response = requests.get(current_weather_url.format(city, api_key)).json()
        
        lat, lon = response['coord']['lat'], response['coord']['lon']
        
        forecast_response = requests.get(forecast_url.format(lat=lat, lon=lon, api_key=api_key)).json()

        weather_data = {
            'city': city,
            'temperature': round(response['main']['temp'] - 273.15, 2),
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }

        daily_forecasts = []
        for daily_data in forecast_response['daily'][:5]:
            daily_forecasts.append({
                'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
                'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
                'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
                'description': daily_data['weather'][0]['description'],
                'icon': daily_data['weather'][0]['icon'],
            })

        return weather_data, daily_forecasts
    
