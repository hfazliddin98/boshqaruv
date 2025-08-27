from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from users.choices import RoleChoice, ALLOWED_USER_MAP
from users.models import Struktura, Users
from users.forms import (
    KirishForm, UserCreateForm, UserUpdateForm, 
    FoydalanuvchiCreateForm, FoydalanuvchiUpdateForm,
    StrukturaCreateForm, StrukturaUpdateForm
)
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
                role=RoleChoice.HODIM.value,
                yaratgan_user=request.user
            ).count(),
            'topshiriq_count': Topshiriq.objects.filter(
                yaratuvchi_user=request.user,
                bajaruvchi_user__role=RoleChoice.HODIM.value,
                javob_yuborildi=False
            ).count(),
        })
    
    # ZAM_DEKAN statistikasi
    elif request.user.role == RoleChoice.ZAM_DEKAN.value:
        context.update({
            'hodim_count': Users.objects.filter(
                role=RoleChoice.HODIM.value,
                yaratgan_user=request.user
            ).count(),
            'topshiriq_count': Topshiriq.objects.filter(
                yaratuvchi_user=request.user,
                bajaruvchi_user__role=RoleChoice.HODIM.value,
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
        form = FoydalanuvchiCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.yaratgan_user = form.cleaned_data['yaratgan_user']
            user.parol = form.cleaned_data['password1']  # Agar ochiq holatda saqlamoqchi bo‘lsangiz
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('user_list', target_role=target_role)
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
                return redirect('user_list', target_role=target_role)
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

    # Barcha foydalanuvchilarni olish (superuser emas)
    from topshiriq.models import Topshiriq
    from topshiriq.choices import StatusChoice
    from django.utils import timezone
    from django.db.models import Count, Q
    
    foydalanuvchilar = Users.objects.filter(is_superuser=False).order_by('role', 'first_name', 'last_name')
    
    # Har bir foydalanuvchi uchun statistika qo'shish
    foydalanuvchilar_statistika_bilan = []
    joriy_vaqt = timezone.now()
    
    for foydalanuvchi in foydalanuvchilar:
        # Foydalanuvchiga berilgan barcha topshiriqlar
        foydalanuvchi_topshiriqlar = Topshiriq.objects.filter(bajaruvchi_user=foydalanuvchi)
        
        # Statistikalar
        jami_topshiriqlar = foydalanuvchi_topshiriqlar.count()
        bajarilgan_topshiriqlar = foydalanuvchi_topshiriqlar.filter(status=StatusChoice.BAJARILDI).count()
        kechikkan_topshiriqlar = foydalanuvchi_topshiriqlar.filter(
            Q(status=StatusChoice.KECHIKDI)
        ).count()
        bajarilmagan_topshiriqlar = foydalanuvchi_topshiriqlar.filter(
            status__in=[StatusChoice.YUBORILDI]
        ).count()
        muvaffaqiyatsiz_topshiriqlar = foydalanuvchi_topshiriqlar.filter(status=StatusChoice.BAJARILMADI).count()
        
        # Foizlarni hisoblash
        bajarilish_foizi = round((bajarilgan_topshiriqlar / jami_topshiriqlar * 100), 1) if jami_topshiriqlar > 0 else 0
        kechikish_foizi = round((kechikkan_topshiriqlar / jami_topshiriqlar * 100), 1) if jami_topshiriqlar > 0 else 0
        bajarilmaganlik_foizi = round((bajarilmagan_topshiriqlar / jami_topshiriqlar * 100), 1) if jami_topshiriqlar > 0 else 0
        
        foydalanuvchi_statistika_bilan = {
            'user': foydalanuvchi,
            'stats': {
                'total': jami_topshiriqlar,
                'completed': bajarilgan_topshiriqlar,
                'delayed': kechikkan_topshiriqlar,
                'unfinished': bajarilmagan_topshiriqlar,
                'failed': muvaffaqiyatsiz_topshiriqlar,
                'completion_rate': bajarilish_foizi,
                'delay_rate': kechikish_foizi,
                'unfinished_rate': bajarilmaganlik_foizi,
            }
        }
        foydalanuvchilar_statistika_bilan.append(foydalanuvchi_statistika_bilan)

    # Umumiy statistikalar
    jami_barcha_topshiriqlar = sum(foydalanuvchi_data['stats']['total'] for foydalanuvchi_data in foydalanuvchilar_statistika_bilan)
    jami_bajarilgan_topshiriqlar = sum(foydalanuvchi_data['stats']['completed'] for foydalanuvchi_data in foydalanuvchilar_statistika_bilan)
    jami_kechikkan_topshiriqlar = sum(foydalanuvchi_data['stats']['delayed'] for foydalanuvchi_data in foydalanuvchilar_statistika_bilan)
    jami_bajarilmagan_topshiriqlar = sum(foydalanuvchi_data['stats']['unfinished'] for foydalanuvchi_data in foydalanuvchilar_statistika_bilan)
    
    # Umumiy foizlarni hisoblash
    umumiy_bajarilish_foizi = round((jami_bajarilgan_topshiriqlar / jami_barcha_topshiriqlar * 100), 1) if jami_barcha_topshiriqlar > 0 else 0
    umumiy_kechikish_foizi = round((jami_kechikkan_topshiriqlar / jami_barcha_topshiriqlar * 100), 1) if jami_barcha_topshiriqlar > 0 else 0
    umumiy_bajarilmaganlik_foizi = round((jami_bajarilmagan_topshiriqlar / jami_barcha_topshiriqlar * 100), 1) if jami_barcha_topshiriqlar > 0 else 0
    
    # Samaradorlik bo'yicha statistika
    ajoyib_foydalanuvchilar = sum(1 for foydalanuvchi_data in foydalanuvchilar_statistika_bilan if foydalanuvchi_data['stats']['total'] > 0 and foydalanuvchi_data['stats']['completion_rate'] >= 80)
    yaxshi_foydalanuvchilar = sum(1 for foydalanuvchi_data in foydalanuvchilar_statistika_bilan if foydalanuvchi_data['stats']['total'] > 0 and 60 <= foydalanuvchi_data['stats']['completion_rate'] < 80)
    ortacha_foydalanuvchilar = sum(1 for foydalanuvchi_data in foydalanuvchilar_statistika_bilan if foydalanuvchi_data['stats']['total'] > 0 and 40 <= foydalanuvchi_data['stats']['completion_rate'] < 60)
    yomon_foydalanuvchilar = sum(1 for foydalanuvchi_data in foydalanuvchilar_statistika_bilan if foydalanuvchi_data['stats']['total'] > 0 and foydalanuvchi_data['stats']['completion_rate'] < 40)
    
    # Rollarga bo'yicha statistika
    rol_statistikasi = {}
    for rol_tanlovi in RoleChoice:
        rol_statistikasi[rol_tanlovi.value] = sum(1 for foydalanuvchi_data in foydalanuvchilar_statistika_bilan if foydalanuvchi_data['user'].role == rol_tanlovi.value)

    context = {
        'foydalanuvchilar_malumotlari': foydalanuvchilar_statistika_bilan,
        'target_role': target_role,
        'RoleChoice': RoleChoice,
        'total_users': len(foydalanuvchilar_statistika_bilan),
        'total_all_tasks': jami_barcha_topshiriqlar,
        'total_completed_tasks': jami_bajarilgan_topshiriqlar,
        'total_delayed_tasks': jami_kechikkan_topshiriqlar,
        'total_unfinished_tasks': jami_bajarilmagan_topshiriqlar,
        'overall_completion_rate': umumiy_bajarilish_foizi,
        'overall_delay_rate': umumiy_kechikish_foizi,
        'overall_unfinished_rate': umumiy_bajarilmaganlik_foizi,
        'excellent_users': ajoyib_foydalanuvchilar,
        'good_users': yaxshi_foydalanuvchilar,
        'average_users': ortacha_foydalanuvchilar,
        'poor_users': yomon_foydalanuvchilar,
        'role_stats': rol_statistikasi,
    }
    return render(request, 'users/komissiya_foydalanuvchi_list.html', context)
