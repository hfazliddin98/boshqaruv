from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from users.models import Users
from users.choices import ALLOWED_USER_MAP
from topshiriq.models import Topshiriq, TopshiriqFile, TopshiriqJavob, TopshiriqJavobFile, Notification
from topshiriq.forms import TopshiriqForm, TopshiriqJavobForm, TopshiriqBaxolashForm
from topshiriq.services import NotificationService
from topshiriq.choices import RoleChoice, ALLOWED_TOPSHIRIQ_MAP, ALLOWED_TOPSHIRIQ_JAVOB_MAP
from topshiriq.choices import StatusChoice


# Try to import xlwt, use alternative if not available
try:
    import xlwt
    EXCEL_EXPORT_AVAILABLE = True
except ImportError:
    EXCEL_EXPORT_AVAILABLE = False


def topshiriq_list(request, target_role):
    if not request.user.is_authenticated:
        return redirect('kirish')

    # ALLOWED_TOPSHIRIQ_MAP orqali ruxsat tekshirish
    allowed_view_roles = ALLOWED_TOPSHIRIQ_MAP.get(request.user.role, [])
   
    # Agar foydalanuvchi o'z topshiriqlarini ko'rmoqchi bo'lsa (bajaruvchi sifatida)
    if request.user.role == target_role:
        # Bajaruvchi o'ziga berilgan topshiriqlarni ko'ra oladi
        topshiriq_data = Topshiriq.objects.select_related('bajaruvchi_user').filter(
            bajaruvchi_user=request.user,
            javob_yuborildi=False
        ).order_by('-created_at')
    elif target_role in [role.value for role in allowed_view_roles]:
        # Ruxsat bor bo'lsa, target_role roldagi bajaruvchilarga berilgan topshiriqlarni ko'rsatish
        topshiriq_data = Topshiriq.objects.select_related('bajaruvchi_user').filter(
            bajaruvchi_user__role=target_role,
            javob_yuborildi=False
        ).order_by('-created_at')
        
        # Agar foydalanuvchi Admin yoki Rektor bo'lmasa, faqat o'zi yaratgan topshiriqlarni ko'radi
        if request.user.role not in ['Admin', 'Rektor']:
            topshiriq_data = topshiriq_data.filter(yaratuvchi_user=request.user)
    else:
        return HttpResponseForbidden(f"Siz {target_role} rolidagi foydalanuvchilar topshiriqlarini ko'ra olmaysiz.")

    context = {
        'topshiriq_data': topshiriq_data,
        'RoleChoice': RoleChoice,
        'target_role': target_role,
    }
    return render(request, 'topshiriq/topshiriq_list.html', context)


@csrf_exempt
def topshiriq_create(request, target_role):
    if not request.user.is_authenticated:
        return redirect('kirish')

    # Ruxsat tekshirish — kim kimga topshiriq bera oladi
    if request.user.role not in ALLOWED_TOPSHIRIQ_MAP.keys():
        return HttpResponseForbidden("Siz topshiriq bera olmaysiz.")

    if target_role not in ALLOWED_TOPSHIRIQ_MAP[request.user.role]:
        return HttpResponseForbidden("Siz ushbu roldagi foydalanuvchiga topshiriq bera olmaysiz.")

    # POST so'rovni tekshirish
    if request.method == 'POST':
        form = TopshiriqForm(request.POST, request.FILES, target_role=target_role, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.yaratuvchi_user = request.user
            task.save()

            # Fayllarni saqlash
            for f in request.FILES.getlist('files'):
                TopshiriqFile.objects.create(topshiriq=task, file=f)

            # Bajaruvchiga notification yuborish
            try:
                NotificationService.notify_new_topshiriq(task)
                # Muvaffaqiyatli xabarni xabar sahifasida ko'rsatish
                return render(request, 'asosiy/xabar.html', {
                    'xatolik_turi': 'Muvaffaqiyat',
                    'xabar_matni': f"'{task.title}' topshirig'i muvaffaqiyatli yaratildi va bajaruvchiga xabar yuborildi!",
                })
            except Exception as e:
                # Xabar yuborishda xato bo'lsa ham topshiriq yaratildi
                return render(request, 'asosiy/xabar.html', {
                    'xatolik_turi': 'Ogohlantirish',  
                    'xabar_matni': f"'{task.title}' topshirig'i yaratildi, lekin bajaruvchiga xabar yuborishda xato: {str(e)}",
                })

            return redirect('topshiriq_list', target_role=target_role)
    else:
        form = TopshiriqForm(target_role=target_role, user=request.user)

    context = {
        'form': form,
        'target_role': target_role,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'topshiriq/topshiriq_create.html', context)


@csrf_exempt
def topshiriq_update(request, target_role, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    # target_role ni enumga aylantirish
    if isinstance(target_role, str):
        try:
            target_role_enum = RoleChoice[target_role]
        except KeyError:
            target_role_enum = RoleChoice(target_role)
    else:
        target_role_enum = target_role

    topshiriq = get_object_or_404(Topshiriq, pk=pk)
    attached_files = topshiriq.files.all()

    # Ruxsat tekshirish (faqat yaratuvchi tahrirlashi mumkin)
    if request.user != topshiriq.yaratuvchi_user:
        return HttpResponseForbidden("Siz ushbu topshiriqni tahrirlashga ruxsatingiz yo'q.")

    if request.method == 'POST':
        form = TopshiriqForm(request.POST, request.FILES, instance=topshiriq, user=request.user, target_role=target_role_enum)
        if form.is_valid():
            topshiriq = form.save()
            # Fayllarni saqlash
            for f in request.FILES.getlist('files'):
                TopshiriqFile.objects.create(topshiriq=topshiriq, file=f)
            return redirect('topshiriq_list', target_role=target_role)
    else:
        form = TopshiriqForm(instance=topshiriq, user=request.user, target_role=target_role_enum)

    context = {
        'form': form,
        'topshiriq': topshiriq,
        'attached_files': attached_files,
        'target_role': target_role,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'topshiriq/topshiriq_update.html', context)


@csrf_exempt
def topshiriq_file_delete(request, target_role, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    topshiriq_file = get_object_or_404(TopshiriqFile, pk=pk)

    if topshiriq_file.file:
        topshiriq_file.file.delete(save=False)

    parent_pk = topshiriq_file.topshiriq.pk
    topshiriq_file.delete()
    return redirect('topshiriq_update', target_role=target_role, pk=parent_pk)


@csrf_exempt
def topshiriq_delete_message(request, target_role, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    topshiriq = get_object_or_404(Topshiriq, pk=pk)
    context = {
        'topshiriq': topshiriq,
        'RoleChoice': RoleChoice,
        'target_role': target_role,
    }
    return render(request, 'topshiriq/topshiriq_delete_message.html', context)


@csrf_exempt
def topshiriq_delete(request, target_role, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    topshiriq = get_object_or_404(Topshiriq, pk=pk)

    for f in topshiriq.files.all():
        f.file.delete(save=False)
        f.delete()

    topshiriq.delete()
    return redirect('topshiriq_list', target_role=target_role)


@csrf_exempt
def topshiriq_javob_create(request, target_role, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    topshiriq = get_object_or_404(Topshiriq, pk=pk)
    
    # ALLOWED_TOPSHIRIQ_JAVOB_MAP bo'yicha ruxsat tekshirish
    allowed_receivers = ALLOWED_TOPSHIRIQ_JAVOB_MAP.get(request.user.role, [])
    
    # Foydalanuvchi topshiriq yaratuvchisiga javob bera oladimi tekshirish
    if topshiriq.yaratuvchi_user.role not in allowed_receivers:
        return HttpResponseForbidden(f"Siz {topshiriq.yaratuvchi_user.role} rolidagi foydalanuvchi topshiriqlariga javob bera olmaysiz.")
    
    # Topshiriq bajaruvchisi ekanligini tekshirish
    if request.user != topshiriq.bajaruvchi_user:
        return HttpResponseForbidden("Siz ushbu topshiriqqa javob bera olmaysiz.")
    
    # Javob allaqachon yuborilgan bo'lsa
    existing_javob = TopshiriqJavob.objects.filter(topshiriq=topshiriq, bajaruvchi_user=request.user).first()
    if existing_javob:
        return redirect('topshiriq_bajaruvchi_list', target_role=target_role)
    
    if request.method == 'POST':
        form = TopshiriqJavobForm(request.POST, request.FILES)
        if form.is_valid():
            javob = form.save(commit=False)
            javob.topshiriq = topshiriq
            javob.bajaruvchi_user = request.user
            javob.urinishlar_soni = topshiriq.urinishlar_soni
            javob.save()
            
            # Fayllarni saqlash (agar yuklangan bo'lsa)
            for f in request.FILES.getlist('files'):
                TopshiriqJavobFile.objects.create(javob=javob, file=f)
            
            # Topshiriq javob yuborildi holatini yangilash
            topshiriq.javob_yuborildi = True
            topshiriq.bajarilgan_vaqti = timezone.now()
            topshiriq.save()
            
            # Yaratuvchiga javob keldi bildirishnomasi yuborish
            try:
                # Javob objektini yaratish
                javob = TopshiriqJavob.objects.filter(topshiriq=topshiriq, bajaruvchi_user=request.user).last()
                if javob:
                    NotificationService.notify_topshiriq_javob(javob)
                
                # Bajaruvchidan shu topshiriq bilan bog'liq barcha bildirishnomalarni o'chirish
                Notification.objects.filter(
                    users=request.user,
                    topshiriq=topshiriq
                ).delete()
                
            except Exception as e:
                print(f"Javob notification yuborishda xato: {str(e)}")
            
            return redirect('topshiriq_bajaruvchi_list', target_role=target_role)
    else:
        form = TopshiriqJavobForm()

    context = {
        'form': form,
        'topshiriq': topshiriq,
        'target_role': target_role,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'topshiriq/topshiriq_javob_create.html', context)


def topshiriq_baxolash(request, target_role, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    topshiriq = get_object_or_404(Topshiriq, pk=pk)

    # Faqat yaratuvchi baholay oladi
    if request.user != topshiriq.yaratuvchi_user:
        return HttpResponseForbidden("Faqat topshiriq yaratuvchisi baholay oladi.")

    # Topshiriq javob yuborilganligini tekshirish
    if not topshiriq.javob_yuborildi:
        return HttpResponseForbidden("Topshiriqqa hali javob yuborilmagan.")

    # Javob ma'lumotlarini olish
    javob = None
    javob_files = []
    try:
        javob = TopshiriqJavob.objects.filter(topshiriq=topshiriq).first()
        if javob:
            javob_files = javob.files.all()
    except TopshiriqJavob.DoesNotExist:
        javob = None

    if request.method == 'POST':
        form = TopshiriqBaxolashForm(request.POST, instance=topshiriq)
        
        # Form valid bo'lmasa ham ma'lumotlarni saqlash
        status = request.POST.get('status')
        baxo = request.POST.get('baxo')
        
        # Manual saqlash
        if status:
            topshiriq.status = status
        if baxo:
            try:
                topshiriq.baxo = int(baxo)
            except (ValueError, TypeError):
                topshiriq.baxo = 0
        
        topshiriq.save()
        
        # Bajaruvchiga baholash bildirishnomasi yuborish
        try:
            NotificationService.notify_topshiriq_baholandi(topshiriq)
            
            # Yaratuvchidan shu topshiriq bilan bog'liq javob bildirishnomalarini o'chirish
            Notification.objects.filter(
                recipient=request.user,
                topshiriq=topshiriq,
                notification_type='topshiriq_javob'
            ).delete()
            
        except Exception as e:
            print(f"Baholash notification yuborishda xato: {str(e)}")
        
        return redirect('hisobot_list')
    else:
        form = TopshiriqBaxolashForm(instance=topshiriq)

    context = {
        'form': form,
        'topshiriq': topshiriq,
        'javob': javob,
        'javob_files': javob_files,
        'target_role': target_role,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'topshiriq/topshiriq_baxolash.html', context)


def topshiriq_bajaruvchi_list(request, target_role):
    if not request.user.is_authenticated:
        return redirect('kirish')

    # Filter parametrini olish
    filter_type = request.GET.get('filter', 'kutilayotgan')  # default: kutilayotgan topshiriqlar
    
    # Foydalanuvchiga biriktirilgan topshiriqlar - base queryset
    base_queryset = Topshiriq.objects.filter(bajaruvchi_user=request.user).select_related('yaratuvchi_user').order_by('-created_at')
    
    # Filter bo'yicha filterlash
    if filter_type == 'bajarilgan':
        # Bajarilgan topshiriqlar - javob yuborilgan
        topshiriq_data = base_queryset.filter(javob_yuborildi=True)
    elif filter_type == 'kutilayotgan':
        # Kutilayotgan topshiriqlar - javob yuborilmagan
        topshiriq_data = base_queryset.filter(javob_yuborildi=False)
    else:
        # Barcha topshiriqlar
        topshiriq_data = base_queryset

    # Pagination
    paginator = Paginator(topshiriq_data, 10)  # Her sahifada 10 ta
    page = request.GET.get('page')
    
    try:
        topshiriq_data = paginator.page(page)
    except PageNotAnInteger:
        topshiriq_data = paginator.page(1)
    except EmptyPage:
        topshiriq_data = paginator.page(paginator.num_pages)

    context = {
        'topshiriq_data': topshiriq_data,
        'target_role': target_role,
        'filter_type': filter_type,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'topshiriq/topshiriq_bajaruvchi_list.html', context)


def topshiriq_javob_list(request, target_role):
    if not request.user.is_authenticated:
        return redirect('kirish')

    # Agar foydalanuvchi o'z javoblarini ko'rmoqchi bo'lsa (bajaruvchi sifatida)
    if request.user.role == target_role:
        # Bajaruvchi o'ziga berilgan va javob yuborgan topshiriqlarni ko'ra oladi
        topshiriq_data = Topshiriq.objects.select_related('bajaruvchi_user', 'yaratuvchi_user').filter(
            bajaruvchi_user=request.user,
            javob_yuborildi=False
        )
        
        javoblar = topshiriq_data
        
    else:
        # ALLOWED_TOPSHIRIQ_JAVOB_MAP bo'yicha ruxsat tekshirish
        allowed_view_roles = ALLOWED_TOPSHIRIQ_JAVOB_MAP.get(request.user.role, [])


        # Agar target_role ko'rish ruxsati bo'lmasa
        if target_role not in [role.value for role in allowed_view_roles]:
            print(f"Ruxsat yo'q: {target_role} not in {[role.value for role in allowed_view_roles]}")
            return HttpResponseForbidden(f"Siz {target_role} rolidagi foydalanuvchilar javoblarini ko'ra olmaysiz.")
        
        
        # Target_role roldagi foydalanuvchilarning javob yuborgan topshiriqlarini olish
        topshiriq_data = Topshiriq.objects.select_related('bajaruvchi_user', 'yaratuvchi_user').filter(
            bajaruvchi_user__role=target_role,
            javob_yuborildi=False
        )
        
        # Javoblar ham topshiriqlarning o'zidan olinadi
        javoblar = topshiriq_data
        
        
        # Agar foydalanuvchi Admin yoki Rektor bo'lmasa, faqat o'zi yaratgan topshiriqlar javoblarini ko'radi
        if request.user.role not in ['Admin', 'Rektor']:
            javoblar = javoblar.filter(yaratuvchi_user=request.user)
            topshiriq_data = topshiriq_data.filter(yaratuvchi_user=request.user)
    
    context = {
        'topshiriq_data': topshiriq_data,
        'javoblar': javoblar,
        'target_role': target_role,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'topshiriq/topshiriq_javob_list.html', context)


def topshiriq_javob_yuborish_list(request):
    if not request.user.is_authenticated:
        return redirect('kirish')

    # Foydalanuvchiga biriktirilgan va hali javob yuborilmagan topshiriqlar
    topshiriq_data = Topshiriq.objects.filter(bajaruvchi_user=request.user, javob_yuborildi=False).select_related('yaratuvchi_user')

    context = {
        'topshiriq_data': topshiriq_data,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'topshiriq/topshiriq_javob_yuborish_list.html', context)


def topshiriq_detail(request, target_role, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    topshiriq = get_object_or_404(Topshiriq, pk=pk)
    
    # Javob ma'lumotlarini olish
    javob = None
    javob_files = []
    if topshiriq.javob_yuborildi:
        try:
            javob = TopshiriqJavob.objects.filter(topshiriq=topshiriq).first()
            if javob:
                javob_files = javob.files.all()
        except TopshiriqJavob.DoesNotExist:
            javob = None
    
    context = {
        'topshiriq': topshiriq,
        'javob': javob,
        'javob_files': javob_files,
        'target_role': target_role,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'topshiriq/topshiriq_detail.html', context)


@login_required
def hisobot_list(request):
    """Javob yuborilgan topshiriqlarni ko'rish va baholash (javob_yuborildi=True)"""
    user = request.user
    
    # Status filter
    status_filter = request.GET.get('status', None)
    
    # Faqat javob yuborilgan va yaratuvchi user bo'lgan topshiriqlarni olish
    base_filter = Q(javob_yuborildi=True) & Q(yaratuvchi_user=user)

    topshiriqlar = Topshiriq.objects.select_related(
        'bajaruvchi_user', 'yaratuvchi_user'
    ).filter(base_filter)
    
    # Statistics hisobi (filter qo'llanishidan oldin)
    stats = {
        'total_reports': topshiriqlar.count(),
        'approved_reports': topshiriqlar.filter(status=StatusChoice.BAJARILDI.value).count(),  # Bajarildi
        'delayed_reports': topshiriqlar.filter(status=StatusChoice.KECHIKDI.value).count(),  # Kechikdi
        'failed_reports': topshiriqlar.filter(status=StatusChoice.BAJARILMADI.value).count(),  # Bajarilmadi
    }
 
    # Status filter qo'llash (statistika hisobidan keyin)
    if status_filter:
        if status_filter == 'completed':
            topshiriqlar = topshiriqlar.filter(status=StatusChoice.BAJARILDI.value)
        elif status_filter == 'delayed':
            topshiriqlar = topshiriqlar.filter(status=StatusChoice.KECHIKDI.value)
        elif status_filter == 'failed':
            topshiriqlar = topshiriqlar.filter(status=StatusChoice.BAJARILMADI.value)

    # Yangi javoblar birinchi
    topshiriqlar = topshiriqlar.order_by('-bajarilgan_vaqti')
    
    # Pagination
    paginator = Paginator(topshiriqlar, 15)
    page = request.GET.get('page')
    
    try:
        topshiriqlar_page = paginator.page(page)
    except PageNotAnInteger:
        topshiriqlar_page = paginator.page(1)
    except EmptyPage:
        topshiriqlar_page = paginator.page(paginator.num_pages)
    
    # Har bir topshiriq uchun javob ma'lumotlarini qo'shish (faqat sahifadagi elementlar uchun)
    topshiriq_ids = [t.id for t in topshiriqlar_page]
    javoblar_dict = {}
    
    # Javoblarni bir marta olib, dictionary ga joylash
    javoblar = TopshiriqJavob.objects.filter(
        topshiriq__id__in=topshiriq_ids
    ).select_related('bajaruvchi_user')
    
    for javob in javoblar:
        javoblar_dict[javob.topshiriq_id] = javob
    
    # Har bir topshiriqga javobni biriktirish
    for topshiriq in topshiriqlar_page:
        topshiriq.javob = javoblar_dict.get(topshiriq.id)
    
    context = {
        'reports': topshiriqlar_page,  # Template da 'reports' ishlatiladi
        'topshiriqlar': topshiriqlar_page,  # Backward compatibility uchun
        'stats': stats,  # Statistika ma'lumotlari
        'StatusChoice': StatusChoice,
        'RoleChoice': RoleChoice,
        'current_status': status_filter,
    }
    
    return render(request, 'topshiriq/hisobot_list.html', context)


def komissiya_statistika_list(request, target_role):
    """Komissiya statistikasi sahifasi - HTML template'ga mos o'zgaruvchilar + date filters"""
    if not request.user.is_authenticated:
        return redirect('kirish')

    from datetime import datetime, timedelta
    from django.db.models import Count, Q

    # Date filter parametrlarini olish
    filter_year = request.GET.get('year')
    filter_month = request.GET.get('month')
    filter_day = request.GET.get('day')

    # Bugungi sana (kechikkanlarni aniqlash uchun)
    bugun = timezone.now().date()

    # Foydalanuvchi bilan bog'liq barcha topshiriqlar
    user_topshiriqlar = Topshiriq.objects.all()

    # Date filter qo'llash
    if filter_year or filter_month or filter_day:
        # Sana filtrlari bor bo'lsa, yaratilish vaqti bo'yicha filtrlash
        filter_q = Q()
        
        if filter_year:
            filter_q &= Q(created_at__year=filter_year)
        if filter_month:
            filter_q &= Q(created_at__month=filter_month)
        if filter_day:
            filter_q &= Q(created_at__day=filter_day)
            
        user_topshiriqlar = user_topshiriqlar.filter(filter_q)

    # HTML'da ishlatiladigan stats o'zgaruvchilari
    stats = {
        # === ASOSIY 4 TA CARD ===
        'total_tasks': user_topshiriqlar.count(),  # Jami topshiriqlar
        
        'completed_reports': user_topshiriqlar.filter(  # Bajarilgan
            javob_yuborildi=True,
            status__in=[StatusChoice.BAJARILDI]
        ).count(),
        
        'overdue_tasks': user_topshiriqlar.filter(  # Kechikkan  
            javob_yuborildi=True,
            status__in=[StatusChoice.KECHIKDI]
        ).count(),
        
        'incomplete_reports': user_topshiriqlar.filter(  # Bajarilmagan
            javob_yuborildi=False,
            status__in=[StatusChoice.YUBORILDI]
        ).count(),

        # === CHART UCHUN QO'SHIMCHA STATISTIKALAR ===
        'approved_reports': user_topshiriqlar.filter(status='QABUL_QILINDI').count(),  # Tasdiqlangan  
        'rejected_reports': user_topshiriqlar.filter(status='QAYTARILDI').count(),  # Rad etilgan
    }

    # Current filter values for template
    current_filters = {
        'year': filter_year,
        'month': filter_month,
        'day': filter_day,
    }

    # Template konteksti
    context = {
        'stats': stats,              # HTML'dagi {{ stats.* }} uchun
        'current_filters': current_filters,  # HTML'dagi filter values uchun
        'RoleChoice': RoleChoice,    # HTML'dagi {{ RoleChoice }} uchun
        'target_role': target_role,  # HTML'dagi {{ target_role }} uchun  
        'user': request.user,        # HTML'dagi {{ user }} uchun
        'current_date': timezone.now(),  # HTML'dagi vaqt uchun
    }
    
    return render(request, 'topshiriq/komissiya_statistika_list.html', context)




@login_required
def notifications_list(request):
    """Bildirishnomalar ro'yxati"""
    notifications = Notification.objects.filter(users=request.user).order_by('-created_at')
    
    # Sahifa ma'lumotlari
    paginator = Paginator(notifications, 20)
    page = request.GET.get('page')
    
    try:
        notifications_page = paginator.page(page)
    except PageNotAnInteger:
        notifications_page = paginator.page(1)
    except EmptyPage:
        notifications_page = paginator.page(paginator.num_pages)
    
    return render(request, 'notifications/list.html', {
        'notifications': notifications_page,
        'unread_count': request.user.bildirishnomalar.filter(is_read=False).count(),
    })

@login_required
def notification_detail(request, pk):
    """Bildirishnoma detallari va o'qilgan deb belgilash"""
    notification = get_object_or_404(Notification, pk=pk, users=request.user)
    
    # Bildirishnomani o'qilgan deb belgilash
    notification.mark_as_read()
    
    # Topshiriqqa yo'naltirish
    if notification.topshiriq:
        topshiriq = notification.topshiriq
        
        # User rolini aniqlash
        from users.choices import RoleChoice
        user_role_mapping = {
            'REKTOR': 'rektor',
            'PROREKTOR': 'prorektor', 
            'DEKAN': 'dekan',
            'PRODDEKAN': 'proddekan',
            'KAFEDRA_MUDIRI': 'kafedra_mudiri',
            'USTOZ': 'ustoz'
        }
        target_role = user_role_mapping.get(request.user.role, 'ustoz')
        
        # Agar bajaruvchi bo'lsa bajaruvchi sahifasiga, yaratuvchi bo'lsa baholash sahifasiga
        if request.user == topshiriq.bajaruvchi_user:
            return redirect('topshiriq_bajaruvchi_list', target_role=target_role)
        elif request.user == topshiriq.yaratuvchi_user:
            return redirect('topshiriq_baxolash', target_role=target_role, pk=topshiriq.pk)
    
    # Agar topshiriq bog'lanmagan bo'lsa, bildirishnomalar sahifasiga qaytish
    return redirect('notifications_list')

@login_required
def mark_all_notifications_read(request):
    """Barcha bildirishnomalarni o'qilgan deb belgilash"""
    if request.method == 'POST':
        count = NotificationService.mark_all_as_read(request.user)
        # Xabar sahifasiga yo'naltirish
        return render(request, 'asosiy/xabar.html', {
            'xatolik_turi': 'Muvaffaqiyat',
            'xabar_matni': f"{count} ta bildirishnoma o'qilgan deb belgilandi.",
        })
    
    return redirect('notifications_list')

@login_required
def notification_count_ajax(request):
    """AJAX orqali bildirishnomalar sonini olish"""
    count = NotificationService.get_unread_count(request.user)
    recent = NotificationService.get_recent_notifications(request.user, 5)
    
    notifications_data = []
    for notification in recent:
        notifications_data.append({
            'id': notification.id,
            'title': notification.topshiriq.title,
            'message': notification.topshiriq.body[:100] if notification.topshiriq.body else '',
            'created_at': notification.created_at.strftime('%d.%m.%Y %H:%M'),
            'is_read': notification.is_read,
        })
    
    return JsonResponse({
        'count': count,
        'notifications': notifications_data
    })
