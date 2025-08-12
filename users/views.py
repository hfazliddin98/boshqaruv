from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from users.choices import RoleChoice
from users.models import Users
from users.forms import UserUpdateForm, UserCreateForm, KirishForm
# from users.forms import BolimBoshliqCreateForm, BolimBoshliqUpdateForm, DekanCreateForm, DekanUpdateForm
# from topshiriq.models import RektorTopshiriq  # va boshqa kerakli modellaringizni import qiling


@csrf_exempt
def home(request):
    if request.user.is_authenticated:
        return redirect('topshiriq_home')

    # # admin
    # if request.user.role == RoleChoice.ADMIN:
    #     return redirect('admin_home')
    
    # # rektor
    # if request.user.role == RoleChoice.REKTOR:
    #     return redirect('rektor_home')

    # # prorektor
    # if request.user.role == RoleChoice.PROREKTOR:
    #     return redirect('prorektor_home')
    
    # # bolim boshligi
    # if request.user.role == RoleChoice.BOLIM_BOSHLIGI:
    #     return redirect('rahbar_home')
    
    # # hodim
    # if request.user.role == RoleChoice.HODIM:
    #     return redirect('hodim_home')


    context = {}
    return render(request, 'asosiy/home.html', context)


def chiqish(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('kirish')


def kirish(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = KirishForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = Users.objects.filter(username=username).first()
            if user and user.check_password(password):
                # Foydalanuvchini tizimga kiritish
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri.")

    context = {
        "form": form
    }
    return render(request, 'asosiy/kirish.html', context)

# # Admin

# def admin_home(request):
#     if not request.user.is_authenticated:
#         return redirect('kirish')
    
#     if not request.user.role == RoleChoice.ADMIN:
#         return redirect('kirish')
    
#     context = {}
#     return render(request, 'admin/home.html', context)

# # Rektor

# def rektor_home(request):
#     if not request.user.is_authenticated:
#         return redirect('kirish')
    
#     if not request.user.role == RoleChoice.REKTOR:
#         return redirect('kirish')
    
#     context = {}
#     return render(request, 'rektor/home.html', context)

# def rektor_prorektorlar(request):
#     if not request.user.is_authenticated:
#         return redirect('kirish')

#     if not request.user.role == RoleChoice.REKTOR:
#         return redirect('kirish')

#     prorektor_data = Users.objects.filter(role=RoleChoice.PROREKTOR)

#     context = {
#         "prorektor_data":prorektor_data
#     }
#     return render(request, 'rektor/rektor_prorektorlar.html', context)


# def rektor_prorektor_create(request):
#     if not request.user.is_authenticated:
#         return redirect('kirish')
#     if not request.user.role == RoleChoice.REKTOR:
#         return redirect('kirish')

#     if request.method == "POST":
#         form = UserCreateForm(request.POST)
#         if form.is_valid():
#             form.save(role=RoleChoice.PROREKTOR)
#             return redirect('rektor_prorektorlar')
#     else:
#         form = UserCreateForm()

#     return render(request, 'rektor/rektor_prorektor_create.html', {"form": form})


# def rektor_prorektor_update(request, pk):
#     if not request.user.is_authenticated:
#         return redirect('kirish')

#     if not request.user.role == RoleChoice.REKTOR:
#         return redirect('kirish')

#     try:
#         prorektor = Users.objects.get(pk=pk, role=RoleChoice.PROREKTOR)
#     except Users.DoesNotExist:
#         raise Http404("Prorektor topilmadi")

#     if request.method == "POST":
#         form = UserUpdateForm(request.POST, instance=prorektor)
#         if form.is_valid():
#             form.save()
#             return redirect('rektor_prorektorlar')
#     else:
#         form = UserUpdateForm(instance=prorektor)

#     context = {
#         "form": form,
#         "prorektor": prorektor 
#     }
#     return render(request, 'rektor/rektor_prorektor_update.html', context)

# # Bolim boshligi

# def bolim_boshligi_home(request):
#     if not request.user.is_authenticated:
#         return redirect('kirish')
#     if not request.user.role == RoleChoice.BOLIM_BOSHLIGI:
#         return redirect('kirish')

#     context = {}
#     return render(request, 'bolim_boshligi/home.html', context)

# # Dekan

# def dekan_home(request):
#     if not request.user.is_authenticated:
#         return redirect('kirish')
#     if not request.user.role == RoleChoice.DEKAN:
#         return redirect('kirish')

#     context = {}
#     return render(request, 'dekan/home.html', context)


# # Hodim

# def hodim_home(request):
#     if not request.user.is_authenticated:
#         return redirect('kirish')
    
#     if not request.user.role == RoleChoice.HODIM:
#         return redirect('kirish')
    
#     context = {}
#     return render(request, 'hodim/home.html', context)