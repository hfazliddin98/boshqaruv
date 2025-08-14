from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from users.choices import RoleChoice, ALLOWED_USER_MAP
from users.models import Users
from users.forms import KirishForm, UserCreateForm, UserUpdateForm

@login_required
@csrf_exempt
def home(request):
    context = {
        'RoleChoice': RoleChoice,
    }
    return render(request, 'users/home.html', context)

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
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri.")

    context = {
        "form": form
    }
    return render(request, 'asosiy/kirish.html', context)


@login_required
def user_list(request, target_role):
    allowed_roles = ALLOWED_USER_MAP.get(request.user.role, [])
    if target_role not in allowed_roles:
        return HttpResponseForbidden("Siz ushbu roldagi foydalanuvchilarni ko‘ra olmaysiz.")
    users = Users.objects.filter(role=target_role)

    context = {
        'users': users,
        'target_role': target_role,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'users/user_list.html', context)

@login_required
def user_create(request, target_role):
    allowed_roles = ALLOWED_USER_MAP.get(request.user.role, [])
    if target_role not in allowed_roles:
        return HttpResponseForbidden("Siz ushbu roldagi foydalanuvchi yaratolmaysiz.")

    if request.method == 'POST':
        form = UserCreateForm(request.POST or None, target_role=target_role)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = target_role
            user.yaratgan_user = request.user
            user.parol = form.cleaned_data['password1']  # Agar ochiq holatda saqlamoqchi bo‘lsangiz
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('user_list', target_role=target_role)
    else:
        form = UserCreateForm(target_role=target_role)

    context = {
        'form': form,
        'target_role': target_role,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'users/user_create.html', context)

@login_required
def user_update(request, target_role, pk):
    allowed_roles = ALLOWED_USER_MAP.get(request.user.role, [])
    if target_role not in allowed_roles:
        return HttpResponseForbidden("Siz ushbu roldagi foydalanuvchini tahrirlashga ruxsatingiz yo‘q.")

    user = get_object_or_404(Users, pk=pk, role=target_role)
    if user.yaratgan_user != request.user:
        return HttpResponseForbidden("Siz faqat o'zingiz yaratgan foydalanuvchini tahrirlashingiz mumkin.")

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user, target_role=target_role)
        if form.is_valid():
            user = form.save(commit=False)
            user.parol = form.cleaned_data['password1']  # Agar ochiq holatda saqlamoqchi bo‘lsangiz
            user.set_password(form.cleaned_data['password1'])
            form.save()
            return redirect('user_list', target_role=target_role)
    else:
        form = UserUpdateForm(instance=user, target_role=target_role)

    context = {
        'form': form,
        'target_role': target_role,
        'user': user,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'users/user_update.html', context)