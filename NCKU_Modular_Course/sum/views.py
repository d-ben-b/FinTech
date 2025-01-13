from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def sum(request):
    return render(request, "sum.html", locals())


def ajax_sum(request):
    a = int(request.GET.get("num1"))
    b = int(request.GET.get("num2"))
    response = {
        "sum": a + b,
    }
    return JsonResponse(response)
