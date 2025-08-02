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
from topshiriq.models import RektorTopshiriq, RektorTopshiriqFile
from topshiriq.forms import RektorTopshiriqCreateForm, RektorTopshiriqUpdateForm
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

    if not request.user.role == RoleChoice.REKTOR:
        return redirect('kirish')

    rektor_topshiriq_file = get_object_or_404(RektorTopshiriqFile, pk=pk)
    rektor_topshiriq_file.delete()
    return redirect('rektor_topshiriq_update', pk=rektor_topshiriq_file.rektor_topshiriq.pk)


# prorektor

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
                RektorTopshiriqFile.objects.create(rektor_topishiriq=prorektor_topishiriq, file=f)

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
