from django.urls import path
from .views import fetch_stock_performance, ceiling_floor

urlpatterns = [
    path(
        "api/stock-analyze/<str:stock_id>/<str:option>/<int:period>",
        fetch_stock_performance,
        name="fetch_stock_performance",
    ),
    path(
        "api/ceiling-floor/<str:stockSymbol>/<str:start_date>/<int:MA>/<str:MA_type>/<int:method_type>",
        ceiling_floor,
        name="ceiling-floor",)
]
