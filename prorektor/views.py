from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import Http404  # ADD: for 404s

from users.choices import RoleChoice
from users.forms import UserCreateForm, UserUpdateForm
from users.models import Users

from topshiriq.models import Topshiriq, TopshiriqFile, TopshiriqJavob, TopshiriqJavobFile
from topshiriq.forms import TopshiriqForm
from topshiriq.choices import StatusChoice, XolatChoice, TopshiriqType





def prorektor_home(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if request.user.role != RoleChoice.PROREKTOR:
        return redirect('kirish')

    bolim_boshliqlar_soni = Users.objects.filter(role=RoleChoice.BOLIM_BOSHLIGI).count()
    dekanlar_soni = Users.objects.filter(role=RoleChoice.DEKAN).count()

    # Unified Topshiriq-based counts
    rektor_topshiriqlar_soni = Topshiriq.objects.filter(
        topshiriq_type=TopshiriqType.REKTOR,
        bajaruvchi_user__role=RoleChoice.PROREKTOR
    ).count()
    bolim_topshiriqlar_soni = Topshiriq.objects.filter(
        topshiriq_type=TopshiriqType.PROREKTOR,
        bajaruvchi_user__role=RoleChoice.BOLIM_BOSHLIGI
    ).count()
    dekan_topshiriqlar_soni = Topshiriq.objects.filter(
        topshiriq_type=TopshiriqType.PROREKTOR,
        bajaruvchi_user__role=RoleChoice.DEKAN
    ).count()

    hisobotlar_soni = 12  # vaqtincha

    context = {
        "bolim_boshliqlar_soni": bolim_boshliqlar_soni,
        "dekanlar_soni": dekanlar_soni,
        "rektor_topshiriqlar_soni": rektor_topshiriqlar_soni,
        "bolim_topshiriqlar_soni": bolim_topshiriqlar_soni,
        "dekan_topshiriqlar_soni": dekan_topshiriqlar_soni,
        "hisobotlar_soni": hisobotlar_soni,
        'RoleChoice': RoleChoice,
    }
    return render(request, 'prorektor/home.html', context)

def bolim_rahbar_list(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')
    
    boshliq_data = Users.objects.filter(role=RoleChoice.BOLIM_RAHBARI)
    
    context = {
        "boshliq_data":boshliq_data
    }
    return render(request, 'prorektor/admin/bolim_rahbar_list.html', context)

def bolim_rahbar_create(request):    
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bolim_rahbar_list')
        else:
            # Form xatoliklarini terminalga chiqarish va foydalanuvchiga ko‘rsatish
            print(form.errors)
            from django.contrib import messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = UserCreateForm()

    return render(request, 'prorektor/admin/bolim_rahbar_create.html', {"form": form})

def bolim_rahbar_update(request, pk):    
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    try:
        bolim_boshliq = Users.objects.get(pk=pk, role=RoleChoice.BOLIM_BOSHLIGI)
    except Users.DoesNotExist:
        raise Http404("Bolim boshligi topilmadi")

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=bolim_boshliq)
        if form.is_valid():
            form.save()
            return redirect('bolim_rahbar_list')
    else:
        form = UserUpdateForm(instance=bolim_boshliq)

    context = {
        "form": form,
        "bolim_boshliq": bolim_boshliq 
    }
    return render(request, 'prorektor/admin/bolim_rahbar_update.html', context)


def dekan_list(request):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    dekan_data = Users.objects.filter(role=RoleChoice.DEKAN)

    context = {
        "dekan_data":dekan_data
    }
    return render(request, 'prorektor/admin/dekan_list.html', context)


def dekan_create(request):   
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dekan_list')
    else:
        form = UserCreateForm()

    return render(request, 'prorektor/admin/dekan_create.html', {"form": form})

def dekan_update(request, pk):    
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    try:
        dekan = Users.objects.get(pk=pk, role=RoleChoice.DEKAN)
    except Users.DoesNotExist:
        raise Http404("Dekan topilmadi")

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=dekan)
        if form.is_valid():
            form.save()
            return redirect('dekan_list')
    else:
        form = UserUpdateForm(instance=dekan)

    context = {
        "form": form,
        "dekan": dekan 
    }
    return render(request, 'prorektor/admin/dekan_update.html', context)



@csrf_exempt
def rektor_topshiriq_list(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    current_xolat = request.GET.get('xolat', '')
    qs = (Topshiriq.objects
          .filter(bajaruvchi_user=request.user, topshiriq_type=TopshiriqType.REKTOR)
          .select_related('yaratuvchi_user', 'bajaruvchi_user')
          .prefetch_related('files')
          .order_by('-created_at'))
    if current_xolat:
        qs = qs.filter(xolat=current_xolat)

    context = {
        'topshiriq_data': qs,
        'status_choices': XolatChoice.choices,
        'current_xolat': current_xolat,
    }
    return render(request, 'prorektor/rektor/topshiriq_list.html', context)


@csrf_protect  # switched to protect instead of exempt
def rektor_topshiriq_javob_create(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    topshiriq = get_object_or_404(
        Topshiriq, pk=pk,
        topshiriq_type=TopshiriqType.REKTOR,
        bajaruvchi_user=request.user
    )

    attached_files = TopshiriqJavobFile.objects.filter(
        javob__topshiriq=topshiriq,
        javob__bajaruvchi_user=request.user
    )

    if request.method == 'POST':
        title = request.POST.get('title', '')
        body = request.POST.get('body', '')
        izoh = request.POST.get('izoh', '')

        javob = TopshiriqJavob.objects.create(
            topshiriq=topshiriq,
            bajaruvchi_user=request.user,
            title=title,
            body=body,
            izoh=izoh
        )
        for f in request.FILES.getlist('files'):
            TopshiriqJavobFile.objects.create(javob=javob, file=f)

        # Mark parent as answered
        if hasattr(topshiriq, 'javob_yuborildi'):
            topshiriq.javob_yuborildi = True
            topshiriq.save(update_fields=['javob_yuborildi'])

        return redirect('prorektor_rektor_topshiriq_list')

    context = {'rektor_topshiriq': topshiriq, 'attached_files': attached_files}
    return render(request, 'prorektor/rektor/topshiriq_javob_create.html', context)


# 2) Prorektor → Bo‘lim boshlig‘i
@csrf_exempt
def bolim_rahbar_topshiriq_list(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    current_xolat = request.GET.get('xolat', '')
    qs = (Topshiriq.objects
          .filter(yaratuvchi_user=request.user,
                  topshiriq_type=TopshiriqType.PROREKTOR,
                  bajaruvchi_user__role=RoleChoice.BOLIM_BOSHLIGI)
          .select_related('yaratuvchi_user', 'bajaruvchi_user')
          .prefetch_related('files')
          .order_by('-created_at'))
    if current_xolat:
        qs = qs.filter(xolat=current_xolat)

    context = {
        'topshiriq_data': qs,
        'status_choices': XolatChoice.choices,
        'current_xolat': current_xolat,
    }
    return render(request, 'prorektor/prorektor_bolim_topshiriq_list.html', context)


@csrf_exempt
def bolim_rahbar_topshiriq_create(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    form = TopshiriqForm(request.POST or None)
    # Restrict bajaruvchi to only Bo‘lim boshlig‘i users
    form.fields['bajaruvchi_user'].queryset = Users.objects.filter(role=RoleChoice.BOLIM_BOSHLIGI)

    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.yaratuvchi_user = request.user
        obj.status = StatusChoice.YUBORILDI
        obj.topshiriq_type = TopshiriqType.PROREKTOR
        obj.save()
        for f in request.FILES.getlist('files'):
            TopshiriqFile.objects.create(topshiriq=obj, file=f)
        return redirect('prorektor_bolim_topshiriq_list')

    return render(request, 'prorektor/prorektor_bolim_topshiriq_create.html', {'form': form})


@csrf_protect
def bolim_rahbar_topshiriq_update(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    topshiriq = get_object_or_404(
        Topshiriq, pk=pk,
        yaratuvchi_user=request.user,
        topshiriq_type=TopshiriqType.PROREKTOR,
        bajaruvchi_user__role=RoleChoice.BOLIM_BOSHLIGI
    )
    attached_files = topshiriq.files.all()

    form = TopshiriqUpdateForm(request.POST or None, request.FILES or None, instance=topshiriq)
    form.fields['bajaruvchi_user'].queryset = Users.objects.filter(role=RoleChoice.BOLIM_BOSHLIGI)

    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        # Keep type consistent for prorektor-created task
        obj.topshiriq_type = TopshiriqType.PROREKTOR
        obj.save()
        for f in request.FILES.getlist('files'):
            TopshiriqFile.objects.create(topshiriq=obj, file=f)
        return redirect('prorektor_bolim_topshiriq_list')

    context = {'form': form, 'topshiriq': topshiriq, 'attached_files': attached_files}
    return render(request, 'prorektor/prorektor_bolim_topshiriq_update.html', context)


# 3) Prorektor → Dekan
@csrf_exempt
def dekan_topshiriq_list(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    current_xolat = request.GET.get('xolat', '')
    qs = (Topshiriq.objects
          .filter(yaratuvchi_user=request.user,
                  topshiriq_type=TopshiriqType.PROREKTOR,
                  bajaruvchi_user__role=RoleChoice.DEKAN)
          .select_related('yaratuvchi_user', 'bajaruvchi_user')
          .prefetch_related('files')
          .order_by('-created_at'))
    if current_xolat:
        qs = qs.filter(xolat=current_xolat)

    context = {
        'topshiriq_data': qs,
        'status_choices': XolatChoice.choices,
        'current_xolat': current_xolat,
    }
    return render(request, 'prorektor/prorektor_dekan_topshiriq_list.html', context)


@csrf_exempt
def dekan_topshiriq_create(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    form = TopshiriqCreateForm(request.POST or None)
    # Restrict bajaruvchi to only Dekan users
    form.fields['bajaruvchi_user'].queryset = Users.objects.filter(role=RoleChoice.DEKAN)

    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.yaratuvchi_user = request.user
        obj.status = StatusChoice.YUBORILDI
        obj.topshiriq_type = TopshiriqType.PROREKTOR
        obj.save()
        for f in request.FILES.getlist('files'):
            TopshiriqFile.objects.create(topshiriq=obj, file=f)
        return redirect('prorektor_dekan_topshiriq_list')

    return render(request, 'prorektor/prorektor_dekan_topshiriq_create.html', {'form': form})


@csrf_protect
def dekan_topshiriq_update(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    topshiriq = get_object_or_404(
        Topshiriq, pk=pk,
        yaratuvchi_user=request.user,
        topshiriq_type=TopshiriqType.PROREKTOR,
        bajaruvchi_user__role=RoleChoice.DEKAN
    )
    attached_files = topshiriq.files.all()

    form = TopshiriqUpdateForm(request.POST or None, request.FILES or None, instance=topshiriq)
    form.fields['bajaruvchi_user'].queryset = Users.objects.filter(role=RoleChoice.DEKAN)

    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.topshiriq_type = TopshiriqType.PROREKTOR
        obj.save()
        for f in request.FILES.getlist('files'):
            TopshiriqFile.objects.create(topshiriq=obj, file=f)
        return redirect('prorektor_dekan_topshiriq_list')

    context = {'form': form, 'topshiriq': topshiriq, 'attached_files': attached_files}
    return render(request, 'prorektor/prorektor_dekan_topshiriq_update.html', context)
