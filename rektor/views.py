from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from django.http import Http404

# User models
from users.models import Users
from users.choices import RoleChoice

# Use unified models and choices
from topshiriq.models import Topshiriq, TopshiriqFile
from topshiriq.choices import StatusChoice, XolatChoice, TopshiriqType, ROLE_TO_TOPSHIRIQ_TYPE

# Use unified forms (see forms below)
from users.forms import UserCreateForm, UserUpdateForm
from topshiriq.forms import TopshiriqCreateForm, TopshiriqUpdateForm




def rektor_home(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')
    
    prorektor_count = Users.objects.filter(role=RoleChoice.PROREKTOR).count()
    topshiriq_count = Topshiriq.objects.filter(yaratuvchi_user=request.user).count()
    
    context = {
        'user': request.user,
        'prorektor_count': prorektor_count,
        'topshiriq_count': topshiriq_count
    }
    return render(request, 'rektor/home.html', context)


def prorektor_list(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    prorektor_data = Users.objects.filter(role=RoleChoice.PROREKTOR)
    return render(request, 'rektor/admin/prorektor_list.html', {"prorektor_data": prorektor_data})


def prorektor_create(request):
    if not request.user.is_authenticated or request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save(role=RoleChoice.PROREKTOR)
            return redirect('prorektor_list')
    else:
        form = UserCreateForm()

    return render(request, 'rektor/admin/prorektor_create.html', {"form": form})


def prorektor_update(request, pk):
    if not request.user.is_authenticated or request.user.role != RoleChoice.REKTOR:
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

    return render(request, 'rektor/admin/prorektor_update.html', {"form": form, "prorektor": prorektor})


@csrf_exempt
def topshiriq_list(request):
    if not request.user.is_authenticated or request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    current_xolat = request.GET.get('xolat', '')
    topshiriq_data = Topshiriq.objects.all()
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
        form = TopshiriqCreateForm(request.POST)
        # Show only Prorektors in the dropdown
        form.fields['bajaruvchi_user'].queryset = Users.objects.filter(role=RoleChoice.PROREKTOR)
        if form.is_valid():
            topshiriq = form.save(commit=False)
            topshiriq.yaratuvchi_user = request.user
            topshiriq.status = StatusChoice.YUBORILDI
            topshiriq.topshiriq_type = ROLE_TO_TOPSHIRIQ_TYPE.get(
                request.user.role, TopshiriqType.XODIM
            )
            topshiriq.save()
            for f in request.FILES.getlist('files'):
                TopshiriqFile.objects.create(topshiriq=topshiriq, file=f)
            messages.success(request, "Topshiriq yaratildi.")
            return redirect('topshiriq_list')
    else:
        form = TopshiriqCreateForm()
        # Show only Prorektors in the dropdown
        form.fields['bajaruvchi_user'].queryset = Users.objects.filter(role=RoleChoice.PROREKTOR)

    return render(request, 'rektor/topshiriq/topshiriq_create.html', {'form': form})


@csrf_protect
def topshiriq_update(request, pk):
    if not request.user.is_authenticated or request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    topshiriq = get_object_or_404(Topshiriq, pk=pk)
    attached_files = topshiriq.files.all()

    if request.method == 'POST':
        form = TopshiriqUpdateForm(request.POST, request.FILES, instance=topshiriq)
        # Show only Prorektors in the dropdown
        form.fields['bajaruvchi_user'].queryset = Users.objects.filter(role=RoleChoice.PROREKTOR)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.topshiriq_type = ROLE_TO_TOPSHIRIQ_TYPE.get(
                request.user.role, obj.topshiriq_type or TopshiriqType.XODIM
            )
            obj.save()
            for file in request.FILES.getlist('files'):
                TopshiriqFile.objects.create(topshiriq=obj, file=file)
            messages.success(request, "Topshiriq yangilandi.")
            return redirect('topshiriq_list')
    else:
        form = TopshiriqUpdateForm(instance=topshiriq)
        # Show only Prorektors in the dropdown
        form.fields['bajaruvchi_user'].queryset = Users.objects.filter(role=RoleChoice.PROREKTOR)

    context = {
        'form': form,
        'topshiriq': topshiriq,
        'rektor_topshiriq': topshiriq,
        'attached_files': attached_files
    }
    return render(request, 'rektor/topshiriq/topshiriq_update.html', context)


@csrf_exempt
def topshiriq_file_delete(request, pk):
    if not request.user.is_authenticated or request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    topshiriq_file = get_object_or_404(TopshiriqFile, pk=pk)

    if topshiriq_file.file:
        topshiriq_file.file.delete(save=False)

    parent_pk = topshiriq_file.topshiriq.pk
    topshiriq_file.delete()

    return redirect('topshiriq_update', pk=parent_pk)


@csrf_exempt
def topshiriq_delete_message(request, pk):
    if not request.user.is_authenticated or request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    rektor_topshiriq = get_object_or_404(Topshiriq, pk=pk)
    return render(request, 'rektor/topshiriq/topshiriq_delete_message.html', {'rektor_topshiriq': rektor_topshiriq})


@csrf_exempt
def topshiriq_delete(request, pk):
    if not request.user.is_authenticated or request.user.role != RoleChoice.REKTOR:
        return redirect('kirish')

    topshiriq = get_object_or_404(Topshiriq, pk=pk)

    for f in topshiriq.files.all():
        f.file.delete(save=False)
        f.delete()

    topshiriq.delete()
    return redirect('topshiriq_list')


