from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Topshiriq, TopshiriqFile, TopshiriqReport, TopshiriqJavob
from .forms import TopshiriqForm, TopshiriqJavobForm
from topshiriq.choices import RoleChoice, ALLOWED_TOPSHIRIQ_MAP, ALLOWED_TOPSHIRIQ_JAVOB_MAP
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

    allowed_roles = ALLOWED_TOPSHIRIQ_MAP.get(request.user.role, [])
    if target_role not in allowed_roles:
        return HttpResponseForbidden("Siz ushbu roldagi foydalanuvchiga topshiriqlarini ko'ra olmaysiz.")

    # Faqat target_role roldagi bajaruvchilarga berilgan topshiriqlarni ko'rsatish
    topshiriq_data = Topshiriq.objects.select_related('bajaruvchi_user').filter(bajaruvchi_user__role=target_role)

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
    
    # Ruxsat tekshirish - faqat bajaruvchi javob bera oladi
    if request.user != topshiriq.bajaruvchi_user:
        return HttpResponseForbidden("Siz ushbu topshiriqqa javob bera olmaysiz.")
    
    if request.method == 'POST':
        form = TopshiriqJavobForm(request.POST, request.FILES)
        if form.is_valid():
            javob = form.save(commit=False)
            javob.topshiriq = topshiriq
            javob.bajaruvchi_user = request.user
            javob.save()
            
            # Topshiriq holatini yangilash
            topshiriq.javob_yuborildi = True
            topshiriq.status = 'YUBORILDI'
            topshiriq.save()
            
            # Avtomatik hisobot yaratish (agar TopshiriqReport jadval mavjud bo'lsa)
            try:
                TopshiriqReport.objects.create(
                    topshiriq=topshiriq,
                    yaratuvchi=topshiriq.yaratuvchi_user,
                    bajaruvchi=request.user,
                    javob=javob.javob_matni,
                    status='completed',
                    completed_at=timezone.now()
                )
            except Exception as e:
                messages.warning(request, "Hisobot yaratishda xatolik yuz berdi, lekin javob muvaffaqiyatli yuborildi.")
            
            messages.success(request, "Javob muvaffaqiyatli yuborildi!")
            return redirect('topshiriq_list', target_role=target_role)
    else:
        form = TopshiriqJavobForm()

    context = {
        'form': form,
        'topshiriq': topshiriq,
        'target_role': target_role,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'topshiriq/topshiriq_javob_create.html', context)


def topshiriq_javob_list(request, target_role):
    if not request.user.is_authenticated:
        return redirect('kirish')

    # Foydalanuvchiga biriktirilgan va hali javob yuborilmagan topshiriqlar
    topshiriq_data = Topshiriq.objects.filter(bajaruvchi_user=request.user, javob_yuborildi=False).select_related('yaratuvchi_user')
    
    # Har bir topshiriq uchun javoblarni olish
    javoblar = TopshiriqJavob.objects.filter(topshiriq__in=topshiriq_data, bajaruvchi_user=request.user).select_related('bajaruvchi_user', 'topshiriq').order_by('-created_at')
    
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
    context = {
        'topshiriq': topshiriq,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'topshiriq/topshiriq_detail.html', context)


@login_required
def hisobot_list(request):
    """Foydalanuvchi roliga qarab hisobotlar ro'yxati"""
    user = request.user
    
    try:
        # Get sort and filter parameters
        status_filter = request.GET.get('status', None)
        
        # User roliga qarab ruxsat etilgan hisobotlarni olish
        if user.role == 'Rektor':
            # Rektor barcha hisobotlarni ko'ra oladi
            all_reports = TopshiriqReport.objects.select_related(
                'topshiriq', 'bajaruvchi', 'yaratuvchi', 'topshiriq__bajaruvchi_user', 'topshiriq__yaratuvchi_user'
            ).all()
        else:
            # Boshqa rollar faqat o'zlari yaratgan yoki o'zlariga tegishli hisobotlarni ko'radi
            allowed_roles = ALLOWED_USER_MAP.get(user.role, [])
            target_roles = [role.value for role in allowed_roles]
            
            all_reports = TopshiriqReport.objects.select_related(
                'topshiriq', 'bajaruvchi', 'yaratuvchi', 'topshiriq__bajaruvchi_user', 'topshiriq__yaratuvchi_user'
            ).filter(
                Q(topshiriq__yaratuvchi_user=user) |  # O'zi yaratgan topshiriqlarning hisobotlari
                Q(bajaruvchi=user) |  # O'zi bajargan topshiriqlarning hisobotlari
                Q(topshiriq__bajaruvchi_user__role__in=target_roles)  # O'z qo'l ostidagi rollarning hisobotlari
            )
        
        # Apply status filter
        if status_filter:
            all_reports = all_reports.filter(status=status_filter)
        
        # Sort by date
        all_reports = all_reports.order_by('-completed_at')
        
        # Calculate stats
        stats = {
            'total_tasks': all_reports.count(),
            'pending_tasks': all_reports.filter(status='completed').count(),
            'completed_tasks': all_reports.filter(status='approved').count(),
            'overdue_tasks': all_reports.filter(status='rejected').count(),
        }
        
        # Role display name
        user_role_display = dict(RoleChoice.choices).get(user.role, user.role)
        
    except Exception as e:
        # Agar jadval mavjud bo'lmasa, bo'sh ma'lumotlar bilan sahifa ko'rsatish
        messages.error(request, f"Ma'lumotlar bazasida xatolik: {str(e)}. Iltimos, migratsiyalarni ishga tushiring.")
        all_reports = []
        stats = {
            'total_tasks': 0,
            'pending_tasks': 0,
            'completed_tasks': 0,
            'overdue_tasks': 0,
        }
        user_role_display = user.role
    
    context = {
        'reports': all_reports,
        'stats': stats,
        'user_role_display': user_role_display,
        'RoleChoice': RoleChoice,
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
    """Approve a submitted report"""
    report = get_object_or_404(TopshiriqReport, id=report_id)
    
    # Only the task creator can approve
    if request.user != report.topshiriq.yaratuvchi_user:
        messages.error(request, "Sizda ushbu hisobotni tasdiqlash uchun ruxsat yo'q")
        return redirect('hisobot_detail', report_id=report_id)
    
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        report.status = 'approved'
        report.approved_at = timezone.now()
        report.comment = comment
        report.save()
        
        # Update task status
        report.topshiriq.status = 'QABUL_QILINDI'
        report.topshiriq.save()
        
        messages.success(request, "Hisobot muvaffaqiyatli tasdiqlandi!")
    
    target_role = report.topshiriq.bajaruvchi_user.role
    return redirect('hisobot_list', target_role=target_role)


@login_required
def reject_report(request, report_id):
    """Reject a submitted report"""
    report = get_object_or_404(TopshiriqReport, id=report_id)
    
    # Only the task creator can reject
    if request.user != report.topshiriq.yaratuvchi_user:
        messages.error(request, "Sizda ushbu hisobotni rad etish uchun ruxsat yo'q")
        return redirect('hisobot_detail', report_id=report_id)
    
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        if not comment.strip():
            messages.error(request, "Rad etish sababi majburiy!")
            return redirect('hisobot_list', target_role=report.bajaruvchi.role)
            
        report.status = 'rejected'
        report.rejected_at = timezone.now()
        report.comment = comment
        report.save()
        
        # Update task status
        report.topshiriq.status = 'QAYTARILDI'
        report.topshiriq.save()
        
        messages.success(request, "Hisobot rad etildi")
        
    return redirect('hisobot_list', target_role=report.bajaruvchi.role)


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
                report.completed_at.strftime('%Y-%m-%d'),
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
        messages.error(request, "Export qilishda xatolik yuz berdi. Iltimos, admin bilan bog'laning.")
        return redirect('hisobot_list')


