from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import Topshiriq, TopshiriqFile
from .forms import TopshiriqForm
from users.choices import RoleChoice

# Kim kimga topshiriq bera oladi mapping
allowed_map = {
    RoleChoice.REKTOR: [RoleChoice.PROREKTOR],
    RoleChoice.PROREKTOR: [RoleChoice.BOLIM_RAHBARI, RoleChoice.DEKAN],
    RoleChoice.BOLIM_RAHBARI: [RoleChoice.BOLIM_BOSHLIGI],
    RoleChoice.BOLIM_BOSHLIGI: [RoleChoice.HODIM],
    RoleChoice.DEKAN: [RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN],
    RoleChoice.KAFEDRA_MUDIRI: [RoleChoice.HODIM],
    RoleChoice.ZAM_DEKAN: [RoleChoice.TYUTOR],
    # Yana kerakli rollarni qo‘shing
}

def topshiriq_home(request):
    if not request.user.is_authenticated:
        return redirect('kirish')

    context = {
        'RoleChoice': RoleChoice,
    }
    return render(request, 'topshiriq/home.html', context)


def topshiriq_list(request, target_role):
    if not request.user.is_authenticated:
        return redirect('kirish')

    allowed_roles = allowed_map.get(request.user.role, [])
    if target_role not in allowed_roles:
        return HttpResponseForbidden("Siz ushbu roldagi foydalanuvchiga topshiriqlarini ko‘ra olmaysiz.")

    topshiriq_data = Topshiriq.objects.filter(yaratuvchi_user=request.user)

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
    if request.user.role not in allowed_map.keys():
        return HttpResponseForbidden("Siz topshiriq bera olmaysiz.")

    if target_role not in allowed_map[request.user.role]:
        return HttpResponseForbidden("Siz ushbu roldagi foydalanuvchiga topshiriq bera olmaysiz.")

    # POST so‘rovni tekshirish
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
        'target_role':target_role,
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

    # Ruxsat tekshirish (masalan, faqat yaratuvchi yoki admin/prorektor tahrirlashi mumkin)
    if not request.user == topshiriq.yaratuvchi_user:
        return HttpResponseForbidden("Siz ushbu topshiriqni tahrirlashga ruxsatingiz yo‘q.")

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
        'RoleChoice': RoleChoice,
        'target_role': target_role,
        'attached_files': attached_files,
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

    rektor_topshiriq = get_object_or_404(Topshiriq, pk=pk)
    context = {
        'rektor_topshiriq': rektor_topshiriq,
        'RoleChoice': RoleChoice,
        'target_role': target_role,
    }
    return render(request, 'rektor/topshiriq/topshiriq_delete_message.html', context)


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
