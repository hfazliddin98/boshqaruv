from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from users.choices import RoleChoice, ALLOWED_USER_MAP
from users.models import Struktura, Users
from users.forms import (
    KirishForm, UserCreateForm, UserUpdateForm, 
    FoydalanuvchiCreateForm, FoydalanuvchiUpdateForm,
    StrukturaCreateForm, StrukturaUpdateForm
)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from topshiriq.models import Topshiriq, TopshiriqJavob


def xabar(request, xabar_matni):
    if not request.user.is_authenticated:
        return redirect('kirish')

    context = {
        'xabar_matni': xabar_matni
    }
    return render(request, 'asosiy/xabar.html', context)


@csrf_exempt
def home(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    # Role-based statistics
    context = {
        'RoleChoice': RoleChoice,
    }
    
    # REKTOR statistikasi
    if request.user.role == RoleChoice.REKTOR.value:
        context.update({
            'prorektor_count': Users.objects.filter(
                role=RoleChoice.PROREKTOR.value,
                yaratgan_user=request.user
            ).count(),
            'topshiriq_count': Topshiriq.objects.filter(
                yaratuvchi_user=request.user,
                bajaruvchi_user__role=RoleChoice.PROREKTOR.value,
                javob_yuborildi=False
            ).count(),
            'hisobot_count': Topshiriq.objects.filter(
                yaratuvchi_user=request.user,
                bajaruvchi_user__role=RoleChoice.PROREKTOR.value,
                javob_yuborildi=True
            ).count(),
        })
    
    # PROREKTOR statistikasi
    elif request.user.role == RoleChoice.PROREKTOR.value:
        context.update({
            'bolim_rahbar_count': Users.objects.filter(
                role=RoleChoice.BOLIM_RAHBARI.value,
                yaratgan_user=request.user
            ).count(),
            'dekan_count': Users.objects.filter(
                role=RoleChoice.DEKAN.value,
                yaratgan_user=request.user
            ).count(),
            'bolim_topshiriq_count': Topshiriq.objects.filter(
                yaratuvchi_user=request.user,
                bajaruvchi_user__role=RoleChoice.BOLIM_RAHBARI.value,
                javob_yuborildi=False
            ).count(),
            'hisobot_count': Topshiriq.objects.filter(
                yaratuvchi_user=request.user,
                javob_yuborildi=True
            ).count(),
        })
    
    # BOLIM_RAHBARI statistikasi
    elif request.user.role == RoleChoice.BOLIM_RAHBARI.value:
        context.update({
            'bolim_boshlik_count': Users.objects.filter(
                role=RoleChoice.BOLIM_BOSHLIGI.value,
                yaratgan_user=request.user
            ).count(),
            'bolim_topshiriq_count': Topshiriq.objects.filter(
                yaratuvchi_user=request.user,
                bajaruvchi_user__role=RoleChoice.BOLIM_BOSHLIGI.value,
                javob_yuborildi=False
            ).count(),
        })
    
    # DEKAN statistikasi
    elif request.user.role == RoleChoice.DEKAN.value:
        context.update({
            'kafedra_mudiri_count': Users.objects.filter(
                role=RoleChoice.KAFEDRA_MUDIRI.value,
                yaratgan_user=request.user
            ).count(),
            'zam_dekan_count': Users.objects.filter(
                role=RoleChoice.ZAM_DEKAN.value,
                yaratgan_user=request.user
            ).count(),
            'kafedra_topshiriq_count': Topshiriq.objects.filter(
                yaratuvchi_user=request.user,
                bajaruvchi_user__role=RoleChoice.KAFEDRA_MUDIRI.value,
                javob_yuborildi=False
            ).count(),
        })
    
    # BOLIM_BOSHLIGI va KAFEDRA_MUDIRI statistikasi
    elif request.user.role in [RoleChoice.BOLIM_BOSHLIGI.value, RoleChoice.KAFEDRA_MUDIRI.value]:
        context.update({
            'hodim_count': Users.objects.filter(
                role=RoleChoice.KAFEDRA_HODIM.value,
                yaratgan_user=request.user
            ).count(),
            'topshiriq_count': Topshiriq.objects.filter(
                yaratuvchi_user=request.user,
                bajaruvchi_user__role=RoleChoice.KAFEDRA_HODIM.value,
                javob_yuborildi=False
            ).count(),
        })
    
    # ZAM_DEKAN statistikasi
    elif request.user.role == RoleChoice.ZAM_DEKAN.value:
        context.update({
            'hodim_count': Users.objects.filter(
                role=RoleChoice.TYUTOR.value,
                yaratgan_user=request.user
            ).count(),
            'topshiriq_count': Topshiriq.objects.filter(
                yaratuvchi_user=request.user,
                bajaruvchi_user__role=RoleChoice.TYUTOR.value,
                javob_yuborildi=False
            ).count(),
        })
    
    # KOMISSIYA statistikasi
    elif request.user.role == RoleChoice.KOMISSIYA.value:
        context.update({
            'user_count': Users.objects.filter(
                is_active=True
            ).exclude(
                role__in=[RoleChoice.ADMIN.value, RoleChoice.KOMISSIYA.value]
            ).count(),
            'topshiriq_count': Topshiriq.objects.count(),
            'statistika_count': Users.objects.filter(is_active=True).count() + Topshiriq.objects.count(),
        })
    
    # ADMIN statistikasi
    elif request.user.role == RoleChoice.ADMIN.value:
        context.update({
            'user_count': Users.objects.filter(
                is_active=True
            ).exclude(
                role__in=[RoleChoice.ADMIN.value, RoleChoice.KOMISSIYA.value]
            ).count(),
            'struktura_count': Struktura.objects.filter(is_active=True).count(),
            'admin_topshiriq_count': Topshiriq.objects.count(),
            'admin_hisobot_count': Topshiriq.objects.filter(javob_yuborildi=True).count(),
        })
    
    # HODIM va TYUTOR uchun o'ziga berilgan topshiriqlar
    else:
        context.update({
            'topshiriq_count': Topshiriq.objects.filter(
                bajaruvchi_user=request.user,
                javob_yuborildi=False
            ).count(),
            'bajarilgan_count': Topshiriq.objects.filter(
                bajaruvchi_user=request.user,
                javob_yuborildi=True
            ).count(),
        })
    
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
    users = Users.objects.filter(role=target_role).filter(yaratgan_user=request.user)

    # Target role uchun display nomi
    target_role_display = dict(RoleChoice.choices).get(target_role, target_role)

    context = {
        'users': users,
        'target_role': target_role,
        'target_role_display': target_role_display,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'users/user_list.html', context)

@login_required
def user_create(request, target_role):
    allowed_roles = ALLOWED_USER_MAP.get(request.user.role, [])
    if target_role not in allowed_roles:
        return HttpResponseForbidden("Siz ushbu roldagi foydalanuvchi yaratolmaysiz.")

    # Mapdan filterlash - faqat joriy userga ruxsat etilgan strukturalarni ko'rsatish
    allowed_struktura_roles = ALLOWED_USER_MAP.get(request.user.role, [])
    struktura_filter = Struktura.objects.filter(
        is_active=True,
        role__in=allowed_struktura_roles
    ) if allowed_struktura_roles else Struktura.objects.filter(is_active=True)

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

    # Target role uchun display nomi
    target_role_display = dict(RoleChoice.choices).get(target_role, target_role)

    context = {
        'form': form,
        'target_role': target_role,
        'target_role_display': target_role_display,
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

    # Target role uchun display nomi
    target_role_display = dict(RoleChoice.choices).get(target_role, target_role)

    context = {
        'form': form,
        'target_role': target_role,
        'target_role_display': target_role_display,
        'user': user,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'users/user_update.html', context)


def admin_foydalanuvchi_list(request, target_role):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != 'Admin':
        return HttpResponseForbidden("Siz ushbu sahifani ko'rishga ruxsat bermaysiz.")

    # Superuser bo'lmagan barcha foydalanuvchilarni olish
    foydalanuvchilar = Users.objects.filter(is_superuser=False)
    

    
    context = {
        'users': foydalanuvchilar,
        'target_role': target_role
    }
    return render(request, 'users/admin_foydalanuvchi_list.html', context)


def admin_foydalanuvchi_create(request, target_role):

    if request.method == 'POST':
        form = FoydalanuvchiCreateForm(request.POST, target_role=target_role)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.yaratgan_user = form.cleaned_data['yaratgan_user']
            user.parol = form.cleaned_data['password1']  # Agar ochiq holatda saqlamoqchi bo‘lsangiz
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('admin_foydalanuvchi_list', target_role=target_role)
    else:
        form = FoydalanuvchiCreateForm(target_role=target_role)

    context = {
        'form': form,
        'target_role': target_role,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'users/admin_foydalanuvchi_create.html', context)

def admin_foydalanuvchi_update(request, target_role, pk):
    if target_role == RoleChoice.ADMIN.value:
        
        user = get_object_or_404(Users, pk=pk)
        

        if request.method == 'POST':
            form = FoydalanuvchiUpdateForm(request.POST, instance=user, target_role=target_role)
            if form.is_valid():
                user = form.save(commit=False)
                user.parol = form.cleaned_data['password1']  # Agar ochiq holatda saqlamoqchi bo‘lsangiz
                user.set_password(form.cleaned_data['password1'])
                form.save()
                return redirect('admin_foydalanuvchi_list', target_role=target_role)
        else:
            form = FoydalanuvchiUpdateForm(instance=user, target_role=target_role)
    else:
        xabar_matni = "Siz ushbu roldagi foydalanuvchini tahrirlashga ruxsatingiz yo‘q."
        return xabar(request, xabar_matni)

    context = {
        'form': form,
        'target_role': target_role,
        'user': user,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'users/admin_foydalanuvchi_update.html', context)


def admin_struktura_list(request, target_role):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != 'Admin':
        xabar_matni = "Siz ushbu sahifani ko'rishga ruxsat bermaysiz."
        return xabar(request, xabar_matni)

    # Barcha strukturalarni olish
    strukturalar = Struktura.objects.all()

    context = {
        'strukturalar': strukturalar,
        'target_role': target_role
    }
    return render(request, 'users/admin_struktura_list.html', context)

def admin_struktura_create(request, target_role):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != 'Admin':
        xabar_matni = "Siz ushbu sahifani ko'rishga ruxsat bermaysiz."
        return xabar(request, xabar_matni)

    if request.method == 'POST':
        form = StrukturaCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_struktura_list', target_role)
    else:
        form = StrukturaCreateForm()

    context = {
        'form': form,
        'target_role': target_role
    }
    return render(request, 'users/admin_struktura_create.html', context)

def admin_struktura_update(request, target_role, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != 'Admin':
        xabar_matni = "Siz ushbu sahifani ko'rishga ruxsat bermaysiz."
        return xabar(request, xabar_matni)

    struktura = get_object_or_404(Struktura, pk=pk)

    if request.method == 'POST':
        form = StrukturaUpdateForm(request.POST, instance=struktura)
        if form.is_valid():
            form.save()
            return redirect('admin_struktura_list', target_role)
    else:
        form = StrukturaUpdateForm(instance=struktura)

    context = {
        'form': form,
        'struktura': struktura,
        'target_role': target_role
    }
    return render(request, 'users/admin_struktura_update.html', context)


def komissiya_foydalanuvchi_list(request, target_role):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.KOMISSIYA.value:
        xabar_matni = "Siz ushbu sahifani ko'rishga ruxsat bermaysiz."
        return xabar(request, xabar_matni)

    
    # Filter parametrlari
    role_filter = request.GET.get('role', '').strip()
    
    # Pagination parametrlari
    page = request.GET.get('page', 1)
    per_page = 20  # Har sahifada 20 ta foydalanuvchi
    
    try:
        # Barcha foydalanuvchilarni olish
        foydalanuvchilar = Users.objects.filter(is_superuser=False).order_by('role', 'first_name', 'last_name')
        
        # Role filter qo'llash
        if role_filter:
            foydalanuvchilar = foydalanuvchilar.filter(role=role_filter)
        
        # Pagination qo'llash
        paginator = Paginator(foydalanuvchilar, per_page)
        
        try:
            foydalanuvchilar_page = paginator.page(page)
        except PageNotAnInteger:
            foydalanuvchilar_page = paginator.page(1)
        except EmptyPage:
            foydalanuvchilar_page = paginator.page(paginator.num_pages)
        
    except Exception as e:
        print(f"DEBUG: Xatolik yuz berdi: {e}")
        import traceback
        traceback.print_exc()

    context = {
        'foydalanuvchilar_page': foydalanuvchilar_page,
        'target_role': target_role,
        'RoleChoice': RoleChoice,
        'role_filter': role_filter,  # Current role filter
    }
    return render(request, 'users/komissiya_foydalanuvchi_list.html', context)


# AJAX Views
def get_struktura_by_role(request, role):
    """Tanlangan rolga mos strukturalarni qaytarish (AJAX uchun)"""
    if request.method == 'GET':
        try:
            # Debug uchun barcha strukturalarni ko'ramiz
            all_strukturalar = Struktura.objects.all()
            print(f"Barcha strukturalar: {all_strukturalar.count()}")
            
            # Role bo'yicha filter (is_active filterni hozircha olib tashlaymiz)
            strukturalar = Struktura.objects.filter(role=role)
            print(f"Role '{role}' uchun strukturalar: {strukturalar.count()}")
            
            for s in strukturalar:
                print(f"  - {s.name} (is_active: {s.is_active})")
            
            data = {
                'strukturalar': [
                    {
                        'id': str(struktura.id),
                        'name': struktura.name
                    }
                    for struktura in strukturalar
                ]
            }
            return JsonResponse(data)
        except Exception as e:
            print(f"AJAX xatosi: {e}")
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Faqat GET so\'rovlar qabul qilinadi'}, status=405)


def get_form_data_example(request):
    """Form ma'lumotlarini olish misoli"""
    if request.method == 'POST':
        # 1. Django form orqali
        form = UserCreateForm(request.POST)
        if form.is_valid():
            # Cleaned data dan olish (validatsiyadan o'tgan)
            selected_role = form.cleaned_data.get('role')
            selected_struktura = form.cleaned_data.get('struktura')
            username = form.cleaned_data.get('username')
            is_active = form.cleaned_data.get('is_active', False)
            
            # 2. To'g'ridan-to'g'ri request.POST dan olish
            raw_role = request.POST.get('role')
            raw_struktura_id = request.POST.get('struktura')
            raw_username = request.POST.get('username')
            raw_is_active = request.POST.get('is_active') == 'on'  # Checkbox uchun
            
            # 3. Multiple select uchun
            # selected_items = request.POST.getlist('multiple_field_name')
            
            # Ma'lumotlarni qayta ishlash
            print(f"Tanlangan rol: {selected_role}")
            print(f"Tanlangan struktura: {selected_struktura}")
            print(f"Foydalanuvchi aktiv: {is_active}")
            
            # Ajax response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Ma\'lumotlar muvaffaqiyatli saqlandi',
                    'data': {
                        'role': selected_role,
                        'struktura': selected_struktura.name if selected_struktura else None,
                        'username': username,
                        'is_active': is_active
                    }
                })
            
            # Oddiy redirect
            return redirect('success_page')
        
        else:
            # Form xatoliklari
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
    
    return JsonResponse({'error': 'Noto\'g\'ri so\'rov'}, status=400)


@login_required
def user_tasks(request, user_id):
    """Foydalanuvchining barcha topshiriqlari va baholari"""
    from datetime import datetime
    from django.utils import timezone
    
    foydalanuvchi = get_object_or_404(Users, id=user_id)
    
    # Foydalanuvchining barcha topshiriqlarini olish
    topshiriqlar = Topshiriq.objects.filter(
        bajaruvchi_user=foydalanuvchi
    ).order_by('-yaratilgan_vaqt')
    
    # Bugungi sana
    today = timezone.now()
    
    # Statistika hisoblash
    completed_count = topshiriqlar.filter(javob_yuborildi=True).count()
    pending_count = topshiriqlar.filter(javob_yuborildi=False, muddat__gte=today).count()
    overdue_count = topshiriqlar.filter(javob_yuborildi=False, muddat__lt=today).count()
    
    # Har bir topshiriq uchun javob va baho olish
    topshiriqlar_data = []
    for topshiriq in topshiriqlar:
        try:
            javob = TopshiriqJavob.objects.get(topshiriq=topshiriq)
            topshiriq.javob_fayl = javob.javob_fayl
            topshiriq.baho = javob.baho
            topshiriq.status = 'completed' if topshiriq.javob_yuborildi else 'pending'
        except TopshiriqJavob.DoesNotExist:
            topshiriq.javob_fayl = None
            topshiriq.baho = None
            topshiriq.status = 'pending'
        
        topshiriqlar_data.append(topshiriq)
    
    context = {
        'foydalanuvchi': foydalanuvchi,
        'topshiriqlar': topshiriqlar_data,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'overdue_count': overdue_count,
        'today': today,
    }
    
    return render(request, 'users/user_tasks.html', context)
