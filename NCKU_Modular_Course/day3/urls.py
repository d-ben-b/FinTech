from django.urls import path
from .views import fetch_stock_performance

urlpatterns = [
    path(
        "api/stock-analyze/<str:stock_id>/<str:option>/<int:period>",
        fetch_stock_performance,
        name="fetch_stock_performance",
    ),
]
