"""
URL configuration for space_flight_control_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from flight.views import FlightViewSet

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path(
        "api/v1/flight/",
        FlightViewSet.as_view(
            {
                "post": "post_flight",
            }
        ),
        name="post_flight",
    ),
    path(
        "api/v1/flight/status",
        FlightViewSet.as_view(
            {
                "post": "post_flight_status",
            }
        ),
        name="post_flight_status",
    ),
    path(
        "api/v1/passenger/",
        FlightViewSet.as_view(
            {
                "post": "post_passenger",
            }
        ),
        name="post_passenger",
    ),
    path(
        "api/v1/ticket/",
        FlightViewSet.as_view(
            {
                "post": "get_ticket",
            }
        ),
        name="get_ticket",
    ),
    path(
        "api/v1/delayed/",
        FlightViewSet.as_view(
            {
                "get": "get_delayed",
            }
        ),
        name="get_delayed",
    ),

    path(
        "api/v1/log/",
        FlightViewSet.as_view(
            {
                "get": "get_log_file",
            }
        ),
        name="get_log_file",
    ),
    path(
        "api/v1/log/status/",
        FlightViewSet.as_view(
            {
                "get": "get_log_file_status",
            }
        ),
        name="get_log_file_status",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
