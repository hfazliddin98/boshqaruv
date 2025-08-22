from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Topshiriq, TopshiriqFile, TopshiriqJavob, TopshiriqJavobFile, TopshiriqReport
from .forms import TopshiriqForm, TopshiriqJavobForm, TopshiriqBaxolashForm
from topshiriq.choices import ALLOWED_TOPSHIRIQ_VIEW_MAP, RoleChoice, ALLOWED_TOPSHIRIQ_MAP, ALLOWED_TOPSHIRIQ_JAVOB_MAP, ALLOWED_TOPSHIRIQ_JAVOB_VIEW_MAP
from users.choices import ALLOWED_USER_MAP

# Try to import xlwt, use alternative if not available
try:
    import xlwt
    EXCEL_EXPORT_AVAILABLE = True
except ImportError:
    EXCEL_EXPORT_AVAILABLE = False


def topshiriq_list(request, target_role):
    if not request.user.is_authenticated:
        return redirect('kirish')

    # ALLOWED_TOPSHIRIQ_VIEW_MAP orqali ruxsat tekshirish
    allowed_view_roles = ALLOWED_TOPSHIRIQ_VIEW_MAP.get(request.user.role, [])
   
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
        messages.warning(request, "Siz bu topshiriqqa allaqachon javob yuborib bo'lgansiz.")
        return redirect('topshiriq_bajaruvchi_list', target_role=target_role)
    
    if request.method == 'POST':
        form = TopshiriqJavobForm(request.POST, request.FILES)
        if form.is_valid():
            javob = form.save(commit=False)
            javob.topshiriq = topshiriq
            javob.bajaruvchi_user = request.user
            javob.save()
            
            # Fayllarni saqlash (agar yuklangan bo'lsa)
            for f in request.FILES.getlist('files'):
                TopshiriqJavobFile.objects.create(javob=javob, file=f)
            
            # Signal avtomatik ravishda topshiriq va hisobot holatini yangilaydi
            messages.success(request, "Javob muvaffaqiyatli yuborildi va hisobot yaratildi!")
            
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
        if form.is_valid():
            # Topshiriq statusini yangilash
            topshiriq.status = form.cleaned_data['status']
            topshiriq.baxo = form.cleaned_data['baxo']
            
            # Qo'shimcha izoh qo'shish
            izoh = request.POST.get('izoh', '')
            if izoh:
                topshiriq.izoh = izoh
            
            topshiriq.save()
            
            messages.success(request, "Baholash muvaffaqiyatli saqlandi!")
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

    # Foydalanuvchiga biriktirilgan topshiriqlar
    topshiriq_data = Topshiriq.objects.filter(bajaruvchi_user=request.user).select_related('yaratuvchi_user').order_by('-created_at')

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
        # ALLOWED_TOPSHIRIQ_JAVOB_VIEW_MAP bo'yicha ruxsat tekshirish
        allowed_view_roles = ALLOWED_TOPSHIRIQ_JAVOB_VIEW_MAP.get(request.user.role, [])


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
    """Javob yuborilgan topshiriqlarni ko'rish va baholash"""
    user = request.user
    
    try:
        # Status filter
        status_filter = request.GET.get('status', None)
        
        # Javob yuborilgan topshiriqlarni olish
        if user.role == 'Rektor':
            # Rektor barcha javob yuborilgan topshiriqlarni ko'ra oladi
            all_topshiriqlar = Topshiriq.objects.select_related(
                'bajaruvchi_user', 'yaratuvchi_user'
            ).filter(javob_yuborildi=True)
        else:
            # Boshqa rollar faqat o'zlari yaratgan yoki tegishli topshiriqlar javoblarini ko'radi
            allowed_roles = ALLOWED_USER_MAP.get(user.role, [])
            target_roles = [role.value for role in allowed_roles]
            
            all_topshiriqlar = Topshiriq.objects.select_related(
                'bajaruvchi_user', 'yaratuvchi_user'
            ).filter(
                javob_yuborildi=True
            ).filter(
                Q(yaratuvchi_user=user) |  # O'zi yaratgan topshiriqlar
                Q(bajaruvchi_user=user) |  # O'zi bajargan topshiriqlar
                Q(bajaruvchi_user__role__in=target_roles)  # O'z qo'l ostidagi rollar
            )
        
        # Status filter - topshiriq status bo'yicha
        if status_filter:
            if status_filter == 'completed':
                all_topshiriqlar = all_topshiriqlar.filter(status='YUBORILDI')
            elif status_filter == 'approved':
                all_topshiriqlar = all_topshiriqlar.filter(status='QABUL_QILINDI')
            elif status_filter == 'rejected':
                all_topshiriqlar = all_topshiriqlar.filter(status='QAYTARILDI')
        
        # Yangi javoblar birinchi
        all_topshiriqlar = all_topshiriqlar.order_by('-bajarilgan_vaqti')
        
        # Statistika
        stats = {
            'total_reports': all_topshiriqlar.count(),
            'pending_reports': all_topshiriqlar.filter(status='YUBORILDI').count(),
            'approved_reports': all_topshiriqlar.filter(status='QABUL_QILINDI').count(),
            'rejected_reports': all_topshiriqlar.filter(status='QAYTARILDI').count(),
        }
        
        # Role display name
        user_role_display = dict(RoleChoice.choices).get(user.role, user.role)
        
        # Har bir topshiriq uchun javob ma'lumotlarini qo'shish
        topshiriq_list = []
        for topshiriq in all_topshiriqlar:
            # Javob ma'lumotlarini olish
            try:
                javob = TopshiriqJavob.objects.filter(topshiriq=topshiriq).first()
                if javob:
                    topshiriq.javob = javob
                    # Report ma'lumotlarini qo'shish
                    try:
                        report = TopshiriqReport.objects.get(topshiriq=topshiriq)
                        topshiriq.report = report
                    except TopshiriqReport.DoesNotExist:
                        # Default report yaratish
                        report = type('obj', (object,), {
                            'status': 'completed' if topshiriq.status == 'YUBORILDI' else 'approved' if topshiriq.status == 'QABUL_QILINDI' else 'rejected',
                            'rating': None,
                            'id': None
                        })
                        topshiriq.report = report
                else:
                    topshiriq.javob = None
                    topshiriq.report = None
            except Exception:
                topshiriq.javob = None
                topshiriq.report = None
            
            topshiriq_list.append(topshiriq)
        
        # Pagination
        paginator = Paginator(topshiriq_list, 15)
        page = request.GET.get('page')
        
        try:
            reports = paginator.page(page)
        except PageNotAnInteger:
            reports = paginator.page(1)
        except EmptyPage:
            reports = paginator.page(paginator.num_pages)
        
    except Exception as e:
        messages.error(request, f"Ma'lumotlar bazasida xatolik: {str(e)}")
        reports = []
        stats = {
            'total_reports': 0,
            'pending_reports': 0,
            'approved_reports': 0,
            'rejected_reports': 0,
        }
        user_role_display = user.role
    
    context = {
        'reports': reports,  # Topshiriq obyektlari javob va report ma'lumotlari bilan
        'stats': stats,
        'user_role_display': user_role_display,
        'RoleChoice': RoleChoice,
        'current_status': status_filter,
        'can_evaluate': True,
    }
    
    return render(request, 'topshiriq/hisobot_list.html', context)


@login_required
def hisobot_detail(request, report_id):
    """Report detail view"""
    report = get_object_or_404(TopshiriqReport, id=report_id)
    
    # Check permissions
    user = request.user
    if user.role != 'Rektor':
        if user != report.yaratuvchi and user != report.bajaruvchi and user != report.topshiriq.yaratuvchi_user:
            messages.error(request, "Sizda ushbu hisobotni ko'rish uchun ruxsat yo'q")
            target_role = report.topshiriq.bajaruvchi_user.role
            return redirect('hisobot_list', target_role=target_role)
    
    context = {'report': report}
    return render(request, 'topshiriq/hisobot_detail.html', context)


@login_required
def approve_report(request, report_id):
    """Javobni tasdiqlash"""
    report = get_object_or_404(TopshiriqReport, id=report_id)
    
    # Faqat topshiriq yaratuvchisi tasdiqlashi mumkin
    if request.user != report.topshiriq.yaratuvchi_user:
        messages.error(request, "Sizda ushbu javobni tasdiqlash uchun ruxsat yo'q")
        return redirect('hisobot_detail', report_id=report_id)
    
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        rating = request.POST.get('rating', None)
        
        report.status = 'approved'
        report.approved_at = timezone.now()
        report.tasdiqlovchi = request.user
        report.comment = comment
        
        if rating and rating.isdigit():
            report.rating = int(rating)
        
        report.save()
        
        # Topshiriq holatini yangilash
        report.topshiriq.status = 'QABUL_QILINDI'
        report.topshiriq.save()
        
        messages.success(request, f"Javob muvaffaqiyatli tasdiqlandi! Baho: {report.rating or 'Berilmagan'}")
    
    return redirect('hisobot_list')


@login_required
def reject_report(request, report_id):
    """Javobni rad etish"""
    report = get_object_or_404(TopshiriqReport, id=report_id)
    
    # Faqat topshiriq yaratuvchisi rad etishi mumkin
    if request.user != report.topshiriq.yaratuvchi_user:
        messages.error(request, "Sizda ushbu javobni rad etish uchun ruxsat yo'q")
        return redirect('hisobot_detail', report_id=report_id)
    
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        if not comment.strip():
            messages.error(request, "Rad etish sababi majburiy!")
            return redirect('hisobot_list')
            
        report.status = 'rejected'
        report.rejected_at = timezone.now()
        report.tasdiqlovchi = request.user
        report.comment = comment
        report.save()
        
        # Topshiriq holatini yangilash
        report.topshiriq.status = 'QAYTARILDI'
        report.topshiriq.javob_yuborildi = False  # Javobni qayta yuborish imkoni
        report.topshiriq.save()
        
        messages.success(request, "Javob rad etildi va qayta ishlash uchun yuborildi")
        
    return redirect('hisobot_list')


@login_required
def download_report(request, report_id):
    """Download report as Excel"""
    report = get_object_or_404(TopshiriqReport, id=report_id)
    
    # Check permissions
    user = request.user
    if user.role != 'Rektor' and user != report.yaratuvchi and user != report.bajaruvchi and user != report.topshiriq.yaratuvchi_user:
        messages.error(request, "Sizda ushbu hisobotni yuklash uchun ruxsat yo'q")
        target_role = report.topshiriq.bajaruvchi_user.role
        return redirect('hisobot_list', target_role=target_role)
    
    if not EXCEL_EXPORT_AVAILABLE:
        messages.warning(request, "Excel export funksiyasi mavjud emas. 'pip install xlwt' buyrug'ini ishga tushiring.")
        return redirect('hisobot_detail', report_id=report_id)
    
    # Create Excel workbook
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Hisobot')
    
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Topshiriq', 'Yaratuvchi', 'Bajaruvchi', 'Yaratilgan sana', 'Bajarilgan sana', 'Status']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    
    row = [
        report.topshiriq.title,
        report.yaratuvchi.get_full_name(),
        report.bajaruvchi.get_full_name(),
        report.topshiriq.created_at.strftime('%Y-%m-%d'),
        report.completed_at.strftime('%Y-%m-%d'),
        report.get_status_display()
    ]
    
    row_num += 1
    for col_num in range(len(row)):
        ws.write(row_num, col_num, row[col_num], font_style)
    
    row_num += 2
    ws.write(row_num, 0, "Topshiriq matni:", font_style)
    row_num += 1
    ws.write(row_num, 0, report.topshiriq.body)
    
    row_num += 2
    ws.write(row_num, 0, "Javob matni:", font_style)
    row_num += 1
    ws.write(row_num, 0, report.javob)
    
    if report.comment:
        row_num += 2
        ws.write(row_num, 0, "Izoh:", font_style)
        row_num += 1
        ws.write(row_num, 0, report.comment)
    
    # Create response
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="hisobot_{report.id}.xls"'
    wb.save(response)
    
    return response


@login_required
def export_all_reports(request):
    """Export all user's accessible reports to Excel"""
    user = request.user
    
    try:
        # User roliga qarab ruxsat etilgan hisobotlarni olish
        if user.role == 'Rektor':
            reports = TopshiriqReport.objects.all()
        else:
            allowed_roles = ALLOWED_USER_MAP.get(user.role, [])
            target_roles = [role.value for role in allowed_roles]
            
            reports = TopshiriqReport.objects.filter(
                Q(topshiriq__yaratuvchi_user=user) |
                Q(bajaruvchi=user) |
                Q(topshiriq__bajaruvchi_user__role__in=target_roles)
            )
        
        if not EXCEL_EXPORT_AVAILABLE:
            messages.warning(request, "Excel export funksiyasi mavjud emas.")
            return redirect('hisobot_list')
        
        # Check if there are any reports to export
        if not reports.exists():
            messages.info(request, "Export qilish uchun hisobotlar mavjud emas.")
            return redirect('hisobot_list')
        
        # Apply ordering
        sort_by = request.GET.get('sort', 'completed_at')
        if sort_by == 'completed_at':
            reports = reports.order_by('completed_at')
        else:
            reports = reports.order_by('-completed_at')
        
        # User role display name
        user_role_display = dict(RoleChoice.choices).get(user.role, user.role)
        
        # Create Excel workbook
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(f'{user_role_display} hisobotlari')
        
        # Sheet header
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        
        columns = ['ID', 'Topshiriq', 'Yaratuvchi', 'Bajaruvchi', 'Yaratilgan sana', 'Bajarilgan sana', 'Status']
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        
        # Sheet body
        font_style = xlwt.XFStyle()
        
        for report in reports:
            row_num += 1
            row = [
                report.id,
                report.topshiriq.title,
                report.yaratuvchi.get_full_name(),
                report.bajaruvchi.get_full_name(),
                report.topshiriq.created_at.strftime('%Y-%m-%d'),
                report.completed_at.strftime('%Y-%m-%d') if report.completed_at else 'N/A',
                report.get_status_display()
            ]
            
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        
        # Create response
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{user_role_display}_hisobotlar.xls"'
        wb.save(response)
        
        return response
        
    except Exception as e:
        # Agar jadval mavjud bo'lmasa yoki boshqa xatolik bo'lsa
        messages.error(request, f"Export qilishda xatolik yuz berdi: {str(e)}. Iltimos, admin bilan bog'laning.")
        return redirect('hisobot_list')


@login_required
def get_javob_report_id(request, javob_id):
    """Javob ID'dan Report ID'ni qaytarish"""
    try:
        javob = get_object_or_404(TopshiriqJavob, id=javob_id)
        report = TopshiriqReport.objects.get(javob=javob)
        return JsonResponse({'report_id': report.id})
    except TopshiriqReport.DoesNotExist:
        # Report yo'q bo'lsa yaratish
        report = TopshiriqReport.objects.create(
            javob=javob,
            topshiriq=javob.topshiriq,
            yaratuvchi=javob.topshiriq.yaratuvchi_user,
            bajaruvchi=javob.bajaruvchi_user,
            status='completed',
            completed_at=javob.created_at
        )
        return JsonResponse({'report_id': report.id})
            

        
    except Exception as e:
        # Agar jadval mavjud bo'lmasa yoki boshqa xatolik bo'lsa
        messages.error(request, f"Export qilishda xatolik yuz berdi: {str(e)}. Iltimos, admin bilan bog'laning.")
        return redirect('hisobot_list')


@login_required
def get_javob_report_id(request, javob_id):
    """Javob ID'dan Report ID'ni qaytarish"""
    try:
        javob = get_object_or_404(TopshiriqJavob, id=javob_id)
        report = TopshiriqReport.objects.get(javob=javob)
        return JsonResponse({'report_id': report.id})
    except TopshiriqReport.DoesNotExist:
        # Report yo'q bo'lsa yaratish
        report = TopshiriqReport.objects.create(
            javob=javob,
            topshiriq=javob.topshiriq,
            yaratuvchi=javob.topshiriq.yaratuvchi_user,
            bajaruvchi=javob.bajaruvchi_user,
            status='completed',
            completed_at=javob.created_at
        )
        return JsonResponse({'report_id': report.id})
