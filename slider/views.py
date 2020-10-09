from django.shortcuts import render
from .models import Slider
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


def slider(request):
    if request.user.role != 'Admin':
        redirect('login')
    context = Slider.objects.all().values('id', 'name', 'img', 'created_at', 'updated_at', 'status')
    return render(request, 'org-admin/slider.html', {'context': context, 'BASE_URL': settings.BASE_URL})


@login_required(login_url='login')
def create_slider(request):
    if request.user.role != 'Admin':
        redirect('login')

    if request.method == 'POST':
        error_message = dict()

        if request.POST.get('name').strip() == '':
            error_message['name_error'] = 'Empty field not allowed'

        if not request.FILES['file']:
            error_message['img_error'] = 'Select an image'

        if error_message:
            return render(request, 'org-admin/create-slider.html', {'error_message': error_message})

        try:
            Slider.objects.create(
                name=request.POST.get('name').strip(),
                img=request.FILES['file'],
                status=request.POST.get('status')
            )

        except Exception as e:
            return render(request, 'org-admin/create-slider.html', {'error_message': error_message})

        return redirect('slider')
    return render(request, 'org-admin/create-slider.html', {})


@login_required(login_url='login')
def update_slider(request, pk):
    if request.user.role != 'Admin':
        return redirect('login')

    context = Slider.objects.get(id=pk)

    if request.method == 'POST':
        error_message = dict()

        if request.POST.get('name').strip() == '':
            error_message['name_error'] = 'Empty field not allowed'

        if error_message:
            return render(request, 'org-admin/update-slider.html', {'context': context, 'error_message': error_message})

        try:
            check = request.FILES['file']
            Slider.objects.filter(id=pk).update(
                        name=request.POST.get('name').strip(),
                        status=request.POST.get('status')
                    )

            b = Slider.objects.get(id=pk)
            b.img = request.FILES['file']
            b.save()

        except Exception as e:
            Slider.objects.filter(id=pk).update(
                name=request.POST.get('name').strip(),
                status=request.POST.get('status')
            )

        if error_message:
            return render(request, 'org-admin/update-slider.html', {'context': context, 'error_message': error_message})

        return redirect('slider')

    return render(request, 'org-admin/update-slider.html', {'context': context, 'BASE_URL': settings.BASE_URL})


@login_required(login_url='login')
def delete_slider(request, pk):
    if request.user.role != 'Admin':
        return redirect('login')
    Slider.objects.get(id=pk).delete()
    return redirect('slider')
