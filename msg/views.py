import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from django.conf import settings
from django.conf.urls.static import static
@api_view(["GET", "POST"])
def rainfall_forecast(request):
    # Allow unauthenticated GET for browser testing
    if request.method == "POST":
        api_key = request.headers.get('Authorization', '')
        if api_key != 'Bearer abc123xyz':
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    # Determine timeframe from GET or POST
    timeframe = request.GET.get("timeframe") if request.method == "GET" else request.data.get("timeframe")
    if timeframe == "week":
        data = {
            "forecast_type": "week",
            "data": [
                {"day": "Monday", "rainfall_mm": 12.3},
                {"day": "Tuesday", "rainfall_mm": 4.7},
                {"day": "Wednesday", "rainfall_mm": 8.0},
                {"day": "Thursday", "rainfall_mm": 3.5},
                {"day": "Friday", "rainfall_mm": 6.1},
                {"day": "Saturday", "rainfall_mm": 9.2},
                {"day": "Sunday", "rainfall_mm": 7.6},
            ]
        }
        return Response(data)

    elif timeframe == "month":
        data = {
            "forecast_type": "month",
            "data": [
                {"week": "Week 1", "rainfall_mm": 35.2},
                {"week": "Week 2", "rainfall_mm": 48.1},
                {"week": "Week 3", "rainfall_mm": 41.7},
                {"week": "Week 4", "rainfall_mm": 50.9},
            ]
        }
        image_url = settings.MEDIA_URL + "i1.jfif"
        response_data = data.copy()
        response_data["graph_url"] = request.build_absolute_uri(image_url)
        return Response(response_data)

    elif timeframe == "year":
        data = {
            "forecast_type": "year",
            "data": [
                {"month": "January", "rainfall_mm": 102},
                {"month": "February", "rainfall_mm": 87},
                {"month": "March", "rainfall_mm": 95},
                {"month": "April", "rainfall_mm": 110},
                {"month": "May", "rainfall_mm": 105},
                {"month": "June", "rainfall_mm": 140},
                {"month": "July", "rainfall_mm": 190},
                {"month": "August", "rainfall_mm": 160},
                {"month": "September", "rainfall_mm": 130},
                {"month": "October", "rainfall_mm": 100},
                {"month": "November", "rainfall_mm": 85},
                {"month": "December", "rainfall_mm": 75},
            ]
        }
        return Response(data)

    else:
        return Response({"error": "Invalid or missing timeframe. Use 'week', 'month', or 'year'."})



def welcome_view(request):
    return render(request, 'msg/welcome.html')

@csrf_exempt        
def get_weather(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        city = data.get("city")
    elif request.method == 'GET':
        city = request.GET.get("city")
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

    api_key = "4c10b05978794ec2a900455dbb36eac0"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        return JsonResponse(weather_data) 

    else:
        return JsonResponse({"error": "Failed to fetch weather data"}, status=400)
        

        