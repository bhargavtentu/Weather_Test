from django.urls import path
from .views import welcome_view,get_weather,rainfall_forecast
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', welcome_view, name='welcome'),
    path("weather", get_weather, name="get_weather"),
    path('api/rainfall_forecast/', rainfall_forecast),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
