from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from users.choices import RoleChoice
from users.models import Users
from topshiriq.models import RektorTopishiriq, RektorTopishiriqFile
from topshiriq.forms import RektorTopishiriqForm


# rektor

@csrf_exempt
def rektor_topishiriq(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if not request.user.role == RoleChoice.REKTOR:
        return redirect('kirish')
    
    rektor_topishiriqlar = RektorTopishiriq.objects.filter(rektor_user=request.user)

    return render(request, 'rektor/rektor_topishiriq.html', {'rektor_topishiriqlar': rektor_topishiriqlar})

@csrf_exempt
def rektor_topishiriq_create(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if not request.user.role == RoleChoice.REKTOR:
        return redirect('kirish')
    
    if request.method == 'POST':
        form = RektorTopishiriqForm(request.POST, request.FILES)
        if form.is_valid():
            rektor_topishiriq = form.save(commit=False)
            rektor_topishiriq.rektor_user = request.user
            rektor_topishiriq.save()

            for f in request.FILES.getlist('files'):
                RektorTopishiriqFile.objects.create(rektor_topishiriq=rektor_topishiriq, file=f)

            return redirect('rektor_topishiriq_detail', pk=rektor_topishiriq.pk)

    else:
        form = RektorTopishiriqForm()

    return render(request, 'rektor/rektor_topishiriq_create.html', {'form': form})

@csrf_exempt
def rektor_topishiriq_update(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')
    
    if not request.user.role == RoleChoice.REKTOR:
        return redirect('kirish')

    rektor_topishiriq = RektorTopishiriq.objects.get(pk=pk)

    if request.method == 'POST':
        form = RektorTopishiriqForm(request.POST, request.FILES, instance=rektor_topishiriq)
        if form.is_valid():
            form.save()
            return redirect('rektor_topishiriq_detail', pk=rektor_topishiriq.pk)
    else:
        form = RektorTopishiriqForm(instance=rektor_topishiriq)

    return render(request, 'rektor/topishiriq_update.html', {'form': form, 'rektor_topishiriq': rektor_topishiriq})
    
 

# prorektor

@csrf_exempt
def prorektor_topishiriq(request):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')
    
    topshiriq_data = RektorTopishiriq.objects.filter(rektor_user=request.user)

    return render(request, 'prorektor/prorektor_topishiriq.html', {'topshiriq_data': topshiriq_data})

@csrf_exempt
def prorektor_topishiriq_create(request):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')
    
    if request.method == 'POST':
        form = RektorTopishiriqForm(request.POST, request.FILES)
        if form.is_valid():
            prorektor_topishiriq = form.save(commit=False)
            prorektor_topishiriq.prorektor_user = request.user
            prorektor_topishiriq.save()

            for f in request.FILES.getlist('files'):
                RektorTopishiriqFile.objects.create(rektor_topishiriq=prorektor_topishiriq, file=f)

            return redirect('prorektor_topishiriq_detail', pk=prorektor_topishiriq.pk)

    else:
        form = RektorTopishiriqForm()

    return render(request, 'prorektor/prorektor_topishiriq_create.html', {'form': form})

@csrf_exempt
def prorektor_topishiriq_update(request, pk):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if not request.user.role == RoleChoice.PROREKTOR:
        return redirect('kirish')

    prorektor_topishiriq = RektorTopishiriq.objects.get(pk=pk)

    if request.method == 'POST':
        form = RektorTopishiriqForm(request.POST, request.FILES, instance=prorektor_topishiriq)
        if form.is_valid():
            form.save()
            return redirect('prorektor_topishiriq_detail', pk=prorektor_topishiriq.pk)
    else:
        form = RektorTopishiriqForm(instance=prorektor_topishiriq)

    return render(request, 'prorektor/topishiriq_update.html', {'form': form, 'prorektor_topishiriq': prorektor_topishiriq})
