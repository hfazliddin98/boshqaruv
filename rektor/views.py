from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from django.http import Http404

# User models
from users.models import Users
from users.forms import UserCreateForm, UserUpdateForm
from users.choices import RoleChoice

# Topshiriq models
from rektor.models import RektorTopshiriq, RektorTopshiriqFile
from rektor.choices import StatusChoice, XolatChoice

# Forms
from rektor.forms import RektorTopshiriqCreateForm, RektorTopshiriqUpdateForm


def rektor_home(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if not request.user.role == RoleChoice.REKTOR:
        return redirect('kirish')
    
    context = {}
    return render(request, 'rektor/home.html', context)


# Prorektorlar ro'yxati

def prorektor_list(request):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if not request.user.role == RoleChoice.REKTOR:
        return redirect('kirish')

    prorektor_data = Users.objects.filter(role=RoleChoice.PROREKTOR)

    context = {
        "prorektor_data":prorektor_data
    }
    return render(request, 'rektor/admin/prorektor_list.html', context)



def prorektor_create(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.REKTOR:
        return redirect('kirish')

    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save(role=RoleChoice.PROREKTOR)
            return redirect('prorektor_list')
    else:
        form = UserCreateForm()

    context = {
        "form": form
    }
    return render(request, 'rektor/admin/prorektor_create.html', context)


def prorektor_update(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if not request.user.role == RoleChoice.REKTOR:
        return redirect('kirish')

    try:
        prorektor = Users.objects.get(pk=pk, role=RoleChoice.PROREKTOR)
    except Users.DoesNotExist:
        raise Http404("Prorektor topilmadi")

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=prorektor)
        if form.is_valid():
            form.save()
            return redirect('prorektor_list')
    else:
        form = UserUpdateForm(instance=prorektor)

    context = {
        "form": form,
        "prorektor": prorektor 
    }
    return render(request, 'rektor/admin/prorektor_update.html', context)


# Topshiriqlar ro'yxati

@csrf_exempt
def topshiriq_list(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if not request.user.role == RoleChoice.REKTOR:
        return redirect('kirish')

    current_xolat = request.GET.get('xolat', '')

    topshiriq_data = RektorTopshiriq.objects.all()
    if current_xolat:
        topshiriq_data = topshiriq_data.filter(xolat=current_xolat)

    context = {
        'topshiriq_data': topshiriq_data,
        'status_choices': StatusChoice.choices,
        'current_xolat': current_xolat,
    }
    return render(request, 'rektor/topshiriq/topshiriq_list.html', context)



@csrf_exempt
def topshiriq_create(request):
    if not request.user.is_authenticated or request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    if request.method == 'POST':
        form = RektorTopshiriqCreateForm(request.POST)
        if form.is_valid():
            topshiriq = form.save(commit=False)
            topshiriq.yaratuvchi_user = request.user
            topshiriq.status = StatusChoice.YUBORILDI
            topshiriq.save()

            # Fayllarni bog'laymiz - to'g'ri maydon nomi bilan
            for f in request.FILES.getlist('files'):
                RektorTopshiriqFile.objects.create(rektor_topshiriq=topshiriq, file=f)

            return redirect('topshiriq_list')
    else:
        form = RektorTopshiriqCreateForm()

    return render(request, 'rektor/topshiriq/topshiriq_create.html', {'form': form})


@csrf_protect
def topshiriq_update(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    topshiriq = get_object_or_404(RektorTopshiriq, pk=pk)
    # To'g'ri related_name dan foydalanish
    attached_files = topshiriq.rektor_topshiriq_files.all()

    if request.method == 'POST':
        form = RektorTopshiriqUpdateForm(request.POST, request.FILES, instance=topshiriq)
        if form.is_valid():
            form.save()
            new_files = request.FILES.getlist('files')
            for file in new_files:
                # To'g'ri maydon nomi bilan
                RektorTopshiriqFile.objects.create(rektor_topshiriq=topshiriq, file=file)
            return redirect('topshiriq_list')
    else:
        form = RektorTopshiriqUpdateForm(instance=topshiriq)

    context = {
        'form': form,
        'topshiriq': topshiriq,
        'attached_files': attached_files
    }
    return render(request, 'rektor/topshiriq/topshiriq_update.html', context)

@csrf_exempt
def topshiriq_file_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    topshiriq_file = get_object_or_404(RektorTopshiriqFile, pk=pk)

    # Faylni media papkadan ham o'chirish
    if topshiriq_file.file:
        topshiriq_file.file.delete(save=False)

    # Bazadan yozuvni o'chirish - to'g'ri maydon nomi bilan
    pk = topshiriq_file.rektor_topshiriq.pk
    topshiriq_file.delete()

    return redirect('topshiriq_update', pk=pk)

@csrf_exempt
def topshiriq_delete_message(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    rektor_topshiriq = get_object_or_404(RektorTopshiriq, pk=pk)

    context = {
        'rektor_topshiriq': rektor_topshiriq
    }
    return render(request, 'rektor/topshiriq/topshiriq_delete_message.html', context)

@csrf_exempt
def topshiriq_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    topshiriq = get_object_or_404(RektorTopshiriq, pk=pk)

    # Fayllarni o'chirish - to'g'ri related_name bilan
    for file in topshiriq.rektor_topshiriq_files.all():
        file.file.delete(save=False)
        file.delete()

    # Topshiriqni o'chirish
    topshiriq.delete()

    return redirect('topshiriq_list')


