from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('fetch_market_data/<str:symbol>/', views.fetch_market_data, name="fetch_market_data"),
]
