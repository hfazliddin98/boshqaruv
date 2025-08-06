from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from urllib3 import request
from users.choices import RoleChoice
from users.models import Users
from topshiriq.models import RektorTopshiriq, RektorTopshiriqFile, RektorTopshiriqJavob, ProrektorBolimTopshiriq, ProrektorBolimTopshiriqFile, ProrektorDekanTopshiriq, ProrektorDekanTopshiriqFile
from topshiriq.forms import RektorTopshiriqCreateForm, RektorTopshiriqUpdateForm, ProrektorBolimTopshiriqForm, ProrektorDekanTopshiriqForm
from topshiriq.choices import StatusChoice


# rektor

@csrf_exempt
def rektor_topshiriq(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if not request.user.role == RoleChoice.REKTOR:
        return redirect('kirish')

    current_xolat = request.GET.get('xolat', '')

    rektor_topshiriq_data = RektorTopshiriq.objects.all()
    if current_xolat:
        rektor_topshiriq_data = rektor_topshiriq_data.filter(xolat=current_xolat)

    context = {
        'rektor_topshiriq_data': rektor_topshiriq_data,
        'status_choices': StatusChoice.choices,
        'current_xolat': current_xolat,
    }
    return render(request, 'rektor/rektor_topshiriqlar.html', context)



@csrf_exempt
def rektor_topshiriq_create(request):
    if not request.user.is_authenticated or request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    if request.method == 'POST':
        form = RektorTopshiriqCreateForm(request.POST)
        if form.is_valid():
            topshiriq = form.save(commit=False)
            topshiriq.yaratuvchi_user = request.user
            topshiriq.status = StatusChoice.YUBORILDI
            topshiriq.save()

            # Fayllarni bog‘laymiz
            for f in request.FILES.getlist('files'):
                RektorTopshiriqFile.objects.create(rektor_topshiriq=topshiriq, file=f)

            return redirect('rektor_topshiriq')
    else:
        form = RektorTopshiriqCreateForm()

    return render(request, 'rektor/rektor_topshiriq_create.html', {'form': form})


@csrf_protect
def rektor_topshiriq_update(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    rektor_topshiriq = get_object_or_404(RektorTopshiriq, pk=pk)
    attached_files = rektor_topshiriq.rektor_topshiriq_files.all()

    if request.method == 'POST':
        form = RektorTopshiriqUpdateForm(request.POST, request.FILES, instance=rektor_topshiriq)
        if form.is_valid():
            form.save()
            new_files = request.FILES.getlist('files')
            for file in new_files:
                RektorTopshiriqFile.objects.create(rektor_topshiriq=rektor_topshiriq, file=file)
            return redirect('rektor_topshiriq')
    else:
        form = RektorTopshiriqUpdateForm(request.POST, request.FILES, instance=rektor_topshiriq)

    context = {
        'form': form,
        'rektor_topshiriq': rektor_topshiriq,
        'attached_files': attached_files
    }
    return render(request, 'rektor/rektor_topshiriq_update.html', context)

@csrf_exempt
def rektor_topshiriq_file_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    rektor_topshiriq_file = get_object_or_404(RektorTopshiriqFile, pk=pk)

    # Faylni media papkadan ham o‘chirish
    if rektor_topshiriq_file.file:
        rektor_topshiriq_file.file.delete(save=False)

    # Bazadan yozuvni o‘chirish
    rektor_pk = rektor_topshiriq_file.rektor_topshiriq.pk
    rektor_topshiriq_file.delete()

    return redirect('rektor_topshiriq_update', pk=rektor_pk)

@csrf_exempt
def rektor_topshiriq_delete_message(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    rektor_topshiriq = get_object_or_404(RektorTopshiriq, pk=pk)

    return render(request, 'rektor/rektor_topshiriq_delete_message.html', {'rektor_topshiriq': rektor_topshiriq})

@csrf_exempt
def rektor_topshiriq_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    rektor_topshiriq = get_object_or_404(RektorTopshiriq, pk=pk)

    # Fayllarni o‘chirish
    for file in rektor_topshiriq.rektor_topshiriq_files.all():
        file.file.delete(save=False)
        file.delete()

    # Topshiriqni o‘chirish
    rektor_topshiriq.delete()

    return redirect('rektor_topshiriq')


# prorektor


@csrf_exempt
def prorektor_rektor_topshiriq_list(request):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.PROREKTOR:
        return redirect('kirish')

    topshiriq_data = RektorTopshiriq.objects.filter(bajaruvchi_user=request.user)

    context = {
        'topshiriq_data': topshiriq_data
    }
    return render(request, 'prorektor/rektor/topshiriq_list.html', context)

    


@csrf_exempt
def prorektor_rektor_topshiriq_javob_create(request, pk):
    """
    Prorektor rektor topshirig'iga javob yozadi va fayl biriktiradi.
    """
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.PROREKTOR:
        return redirect('kirish')

    rektor_topshiriq = get_object_or_404(RektorTopshiriq, pk=pk)

    from topshiriq.forms import RektorTopshiriqJavobForm
    from topshiriq.models import RektorTopshiriqJavobFile

    # Mavjud javob fayllari (agar kerak bo'lsa)
    attached_files = RektorTopshiriqJavobFile.objects.filter(rektor_topshiriq_javob__rektor_topshiriq=rektor_topshiriq, rektor_topshiriq_javob__bajaruvchi_user=request.user)

    if request.method == 'POST':
        form = RektorTopshiriqJavobForm(request.POST, request.FILES)
        if form.is_valid():
            javob = form.save(commit=False)
            javob.rektor_topshiriq = rektor_topshiriq
            javob.bajaruvchi_user = request.user
            javob.save()
            # Fayllarni biriktirish
            for f in request.FILES.getlist('files'):
                RektorTopshiriqJavobFile.objects.create(rektor_topshiriq_javob=javob, file=f)
            return redirect('prorektor_rektor_topshiriq_list')
    else:
        form = RektorTopshiriqJavobForm()

    context = {
        'form': form,
        'rektor_topshiriq': rektor_topshiriq,
        'attached_files': attached_files
    }
    return render(request, 'prorektor/rektor/topshiriq_javob_create.html', context)




@csrf_exempt
def prorektor_rektor_topshiriq_javob_update(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.PROREKTOR:
        return redirect('kirish')

    prorektor_topshiriq = get_object_or_404(RektorTopshiriq, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title', '')
        body = request.POST.get('body', '')
        izoh = request.POST.get('izoh', '')

        RektorTopshiriqJavob.objects.create(
            rektor_topshiriq=prorektor_topshiriq,
            bajaruvchi_user=request.user,
            title=title,
            body=body,
            izoh=izoh
        )
        return redirect('prorektor_topishiriq_detail', pk=prorektor_topshiriq.pk)

    context = {
        'prorektor_topshiriq': prorektor_topshiriq
    }
    return render(request, 'prorektor/prorektor_topshiriq_javob_create.html', context)




@csrf_exempt
def prorektor_topshiriq(request):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')
    
    topshiriq_data = RektorTopshiriq.objects.filter(rektor_user=request.user)

    context = {
        'topshiriq_data': topshiriq_data
    }
    return render(request, 'prorektor/prorektor_topshiriq.html', context)

@csrf_exempt
def prorektor_topshiriq_create(request):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')
    
    if request.method == 'POST':
        form = RektorTopshiriqCreateForm(request.POST, request.FILES)
        if form.is_valid():
            prorektor_topishiriq = form.save(commit=False)
            prorektor_topishiriq.prorektor_user = request.user
            prorektor_topishiriq.save()

            for f in request.FILES.getlist('files'):
                RektorTopshiriqFile.objects.create(rektor_topshiriq=prorektor_topishiriq, file=f)

            return redirect('prorektor_topishiriq_detail', pk=prorektor_topishiriq.pk)

    else:
        form = RektorTopshiriqCreateForm()

    context = {
        'form': form
    }
    return render(request, 'prorektor/prorektor_topishiriq_create.html', context)

@csrf_exempt
def prorektor_topshiriq_update(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    prorektor_topishiriq = RektorTopshiriq.objects.get(pk=pk)

    if request.method == 'POST':
        form = RektorTopshiriqCreateForm(request.POST, request.FILES, instance=prorektor_topishiriq)
        if form.is_valid():
            form.save()

            return redirect('prorektor_topishiriq_detail', pk=prorektor_topishiriq.pk)
    else:
        form = RektorTopshiriqCreateForm(instance=prorektor_topishiriq)

    context = {
        'form': form,
        'prorektor_topishiriq': prorektor_topishiriq
    }
    return render(request, 'prorektor/topishiriq_update.html', context)


@csrf_exempt
def prorektor_bolim_topshiriq_list(request):
    """
    Prorektor uchun bo‘lim boshliqlariga yuborilgan topshiriqlar ro‘yxati.
    """
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.PROREKTOR:
        return redirect('kirish')

    topshiriq_data = ProrektorBolimTopshiriq.objects.all().order_by('-created_at')

    context = {
        'topshiriq_data': topshiriq_data
    }
    return render(request, 'prorektor/prorektor_bolim_topshiriq_list.html', context)


@csrf_exempt
def prorektor_bolim_topshiriq_create(request):
    """
    Prorektor tomonidan bo‘lim boshlig‘iga yangi topshiriq yaratish.
    """
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.PROREKTOR:
        return redirect('kirish')

    if request.method == 'POST':
        form = ProrektorBolimTopshiriqForm(request.POST, request.FILES)
        if form.is_valid():
            topshiriq = form.save(commit=False)
            topshiriq.yaratuvchi_user = request.user
            topshiriq.save()
            # Fayllarni saqlash
            for f in request.FILES.getlist('files'):
                ProrektorBolimTopshiriqFile.objects.create(prorektor_bolim_topshiriq=topshiriq, file=f)
            return redirect('prorektor_bolim_topshiriq_list')
    else:
        form = ProrektorBolimTopshiriqForm()

    return render(request, 'prorektor/prorektor_bolim_topshiriq_create.html', {'form': form})


@csrf_exempt
def prorektor_bolim_topshiriq_update(request, pk):
    """
    Prorektor tomonidan bo‘lim boshlig‘iga yuborilgan topshiriqni tahrirlash.
    """
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.PROREKTOR:
        return redirect('kirish')

    topshiriq = get_object_or_404(ProrektorBolimTopshiriq, pk=pk)
    attached_files = topshiriq.prorektor_bolim_topshiriq_files.all()

    if request.method == 'POST':
        form = ProrektorBolimTopshiriqForm(request.POST, request.FILES, instance=topshiriq)
        if form.is_valid():
            form.save()
            # Yangi fayllarni qo'shish
            for f in request.FILES.getlist('files'):
                ProrektorBolimTopshiriqFile.objects.create(prorektor_bolim_topshiriq=topshiriq, file=f)
            return redirect('prorektor_bolim_topshiriq_list')
    else:
        form = ProrektorBolimTopshiriqForm(instance=topshiriq)

    context = {
        'form': form,
        'topshiriq': topshiriq,
        'attached_files': attached_files
    }
    return render(request, 'prorektor/prorektor_bolim_topshiriq_update.html', context)


@csrf_exempt
def prorektor_dekan_topshiriq_list(request):
    """
    Prorektor uchun dekanlarga yuborilgan topshiriqlar ro‘yxati.
    """
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.PROREKTOR:
        return redirect('kirish')

    topshiriq_data = ProrektorDekanTopshiriq.objects.all().order_by('-created_at')

    context = {
        'topshiriq_data': topshiriq_data
    }
    return render(request, 'prorektor/prorektor_dekan_topshiriq_list.html', context)


@csrf_exempt
def prorektor_dekan_topshiriq_create(request):
    """
    Prorektor tomonidan dekanlarga yangi topshiriq yaratish.
    """
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.PROREKTOR:
        return redirect('kirish')

    if request.method == 'POST':
        form = ProrektorDekanTopshiriqForm(request.POST, request.FILES)
        if form.is_valid():
            topshiriq = form.save(commit=False)
            topshiriq.yaratuvchi_user = request.user
            topshiriq.save()
            # Fayllarni saqlash
            for f in request.FILES.getlist('files'):
                ProrektorDekanTopshiriqFile.objects.create(prorektor_dekan_topshiriq=topshiriq, file=f)
            return redirect('prorektor_dekan_topshiriq_list')
    else:
        form = ProrektorDekanTopshiriqForm()

    return render(request, 'prorektor/prorektor_dekan_topshiriq_create.html', {'form': form})


@csrf_exempt
def prorektor_dekan_topshiriq_update(request, pk):
    """
    Prorektor tomonidan dekanlarga yuborilgan topshiriqni tahrirlash.
    """
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.PROREKTOR:
        return redirect('kirish')

    topshiriq = get_object_or_404(ProrektorDekanTopshiriq, pk=pk)
    attached_files = topshiriq.prorektor_dekan_topshiriq_files.all()

    if request.method == 'POST':
        form = ProrektorDekanTopshiriqForm(request.POST, request.FILES, instance=topshiriq)
        if form.is_valid():
            form.save()
            # Yangi fayllarni qo'shish
            for f in request.FILES.getlist('files'):
                ProrektorDekanTopshiriqFile.objects.create(prorektor_dekan_topshiriq=topshiriq, file=f)
            return redirect('prorektor_dekan_topshiriq_list')
    else:
        form = ProrektorDekanTopshiriqForm(instance=topshiriq)

    context = {
        'form': form,
        'topshiriq': topshiriq,
        'attached_files': attached_files
    }
    return render(request, 'prorektor/prorektor_dekan_topshiriq_update.html', context)
