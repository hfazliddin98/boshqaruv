from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home(request):
    context = {}
    return render(request, 'asosiy/home.html', context)
