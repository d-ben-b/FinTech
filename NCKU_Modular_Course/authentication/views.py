# Create your views here.
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def dashboard_view(request):
    return JsonResponse({"message": "Welcome to the dashboard!"})


def main_view(request):
    if not request.user.is_authenticated:
        return redirect("http://localhost:5173/login")
    return JsonResponse({"message": "You are on the main page"})


class CheckAuthAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return JsonResponse({"message": "Authenticated"}, status=200)
