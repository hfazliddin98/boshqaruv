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
    
    # rektor
    if request.user.role == RoleChoice.REKTOR:
        return redirect('rektor_home')

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

@csrf_exempt
def rektor_prorektorlar(request):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if not request.user.role == RoleChoice.REKTOR:
        return redirect('kirish')

    prorektor_data = Users.objects.filter(role=RoleChoice.PROREKTOR)

    context = {
        "prorektor_data":prorektor_data
    }
    return render(request, 'rektor/rektor_prorektorlar.html', context)




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
def prorektor_bolim_boshliqlar(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')
    
    boshliq_data = Users.objects.filter(role=RoleChoice.BOLIM_BOSHLIGI)
    
    context = {
        "boshliq_data":boshliq_data
    }
    return render(request, 'prorektor/prorektor_bolim_boshliqlar.html', context)

@csrf_exempt
def prorektor_dekanlar(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')
    
    boshliq_data = Users.objects.filter(role=RoleChoice.DEKAN)
    
    context = {
        "boshliq_data":boshliq_data
    }
    return render(request, 'prorektor/prorektor_dekanlar.html', context)

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