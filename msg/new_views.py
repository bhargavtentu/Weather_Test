import requests
from django.shortcuts import render
from django.http import JsonResponse


def welcome_view(request):
    return render(request, 'msg/welcome.html')

def get_weather(request):
    api_key = "4c10b05978794ec2a900455dbb36eac0"

    if request.method == "GET":
        city = request.GET.get('city')
    elif request.method == "POST":
        data = json.loads(request.body)
        city = data.get('city')
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)

    if not city:
        return JsonResponse({"error": "City parameter is required"}, status=400)

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        result = {
            "main": {
                "temp": data.get("main", {}).get("temp")
            },
            "wind": {
                "speed": data.get("wind", {}).get("speed")
            },
            "weather": [
                {
                    "main": weather.get("main")
                } for weather in data.get("weather", [])
            ]
        }
        return JsonResponse(result)
    else:
        return JsonResponse({"error": "Failed to fetch weather data"}, status=response.status_code)


       {
  "openapi": "3.0.0",
  "info": {
    "title": "Weather Plugin",
    "version": "1.0.0",
    "description": "Get the current weather for a given city"
  },
  "servers": [
    {
      "url": "https://34fe-103-123-173-19.ngrok-free.app"
    }
  ],
  "paths": {
    "/weather": {
      "post": {
        "summary": "Fetch weather details",
        "operationId": "getWeather",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "city": {
                    "type": "string",
                    "description": "Name of the city to get weather"
                  }
                },
                "required": ["city"]
              },
              "examples": {
                "example-1": {
                  "summary": "Sample input",
                  "value": {
                    "city": "New York"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "temperature": {
                      "type": "string",
                      "description": "Temperature in the city"
                    },
                    "condition": {
                      "type": "string",
                      "description": "Weather condition"
                    }
                  }
                },
                "examples": {
                  "example-1": {
                    "summary": "Sample response",
                    "value": {
                      "temperature": "27°C",
                      "condition": "Clear"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
