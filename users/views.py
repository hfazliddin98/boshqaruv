from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from users.choices import RoleChoice
from users.models import Users


@csrf_exempt
def home(request):
    if not request.user.is_authenticated:
        return redirect('kirish')

    # admin
    if request.user.role == RoleChoice.ADMIN:
        return redirect('admin_home')
    
    # prorektor
    if request.user.role == RoleChoice.PROREKTOR:
        return redirect('prorektor_home')
    
    # bolim boshligi
    if request.user.role == RoleChoice.BOLIM_BOSHLIGI:
        return redirect('rahbar_home')
    
    # hodim
    if request.user.role == RoleChoice.HODIM:
        return redirect('hodim_home')

    context = {}
    return render(request, 'asosiy/home.html', context)



def kirish(request):
    if request.user.is_authenticated:
        return redirect('home')

    context = {}
    return render(request, 'asosiy/kirish.html', context)

# Admin

@csrf_exempt
def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if not request.user.role == RoleChoice.ADMIN:
        return redirect('kirish')
    
    context = {}
    return render(request, 'admin/home.html', context)

# Rektor

@csrf_exempt
def rektor_home(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if not request.user.role == RoleChoice.REKTOR:
        return redirect('kirish')
    
    context = {}
    return render(request, 'rektor/home.html', context)

# Prorektor

@csrf_exempt
def prorektor_home(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')
    
    context = {}
    return render(request, 'prorektor/home.html', context)

@csrf_exempt
def prorektor_bolim_rahbarlar(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')
    
    rahbar_data = Users.objects.filter(role=RoleChoice.BOLIM_BOSHLIGI)
    
    context = {
        "rahbar_data":rahbar_data
    }
    return render(request, 'prorektor/bolim_rahbarlar.html', context)

# Bolim boshligi

@csrf_exempt
def bolim_boshligi_home(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.BOLIM_BOSHLIGI:
        return redirect('kirish')

    context = {}
    return render(request, 'bolim_boshligi/home.html', context)

# Dekan

@csrf_exempt
def dekan_home(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.DEKAN:
        return redirect('kirish')

    context = {}
    return render(request, 'dekan/home.html', context)


# Hodim

@csrf_exempt
def hodim_home(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if not request.user.role == RoleChoice.HODIM:
        return redirect('kirish')
    
    context = {}
    return render(request, 'hodim/home.html', context)