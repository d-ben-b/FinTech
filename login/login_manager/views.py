from .models import User
import json
from django.db import transaction
from django.http import JsonResponse
# Login Function


def Login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        try:
            user = User.objects.get(username=username, password=password)
            with transaction.atomic():
                user.state = True  # 登入後將 state 設為 True
                user.save()
            return JsonResponse({"success": True, "message": "Login successful!"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid name or password."}, status=400)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

# Register Function


def Register(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if not username or not password or not email:
            return JsonResponse({"success": False, "message": "All fields are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "message": "Username already exists!"}, status=400)
        elif User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "Email already exists!"}, status=400)
        else:
            User.objects.create(username=username,
                                password=password, email=email, state=False)
            return JsonResponse({"success": True, "message": "Registration successful!"}, status=200)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


# Logout Function


def Logout(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        try:
            user = User.objects.get(username=username, state=True)
            with transaction.atomic():
                user.state = False  # 登出後將 state 設為 False
                user.save()
            return JsonResponse({"success": True, "message": "Logout successful!"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "User is not logged in or does not exist."}, status=400)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


def Check(request):
    print(request.body)
    data = json.loads(request.body)
    print(data)

    username = data.get("username")
    if request.method == "POST":
        user = User.objects.get(username=username)
        if user.state:
            return JsonResponse({"success": True, "message": "User is logged in."}, status=200)
        else:
            return JsonResponse({"success": False, "message": "User is not logged in."}, status=400)
