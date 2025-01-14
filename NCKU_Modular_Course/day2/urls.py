from django.urls import path
from .views import fetch_stock_data, fetch_stock_performance

urlpatterns = [
    path("api/stock/<str:stock_id>/", fetch_stock_data, name="fetch_stock_data"),
    path(
        "api/stock-performance/<str:stock_id>/<int:n_months>/",
        fetch_stock_performance,
        name="fetch_stock_performance",
    ),
]
