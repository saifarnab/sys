from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Banner
from userProfile.models import User, OrgProfile
from django.contrib.auth.decorators import login_required
from django.conf import settings

""" Event Banner """


@login_required(login_url='login')
def banner(request):

    if request.user.role == 'Admin':
        context = Banner.objects.all().values('id', 'name', 'img', 'created_at', 'updated_at', 'status', 'user__name')

    elif request.user.role == 'Org':
        org_profile = OrgProfile.objects.get(user=User.objects.get(username=str(request.user)))
        context = Banner.objects.filter(user=org_profile).values('id', 'name', 'img', 'created_at', 'updated_at', 'status')
    return render(request, 'org-admin/banner.html', {'context': context, 'BASE_URL': settings.BASE_URL})


@login_required(login_url='login')
def create_banner(request):
    if request.method == 'POST':
        error_message = dict()
        org_profile = OrgProfile.objects.get(user=User.objects.get(username=str(request.user)))

        if request.POST.get('name').strip() == '':
            error_message['name_error'] = 'Empty field not allowed'

        elif list(Banner.objects.filter(user=org_profile, name=request.POST.get('name').strip())):
            error_message['name_error'] = 'Already available'

        if not request.FILES['file']:
            error_message['img_error'] = 'Select an image'

        if error_message:
            return render(request, 'org-admin/create-banner.html', {'error_message': error_message})

        try:
            if request.user.role == 'Org':
                Banner.objects.create(
                    user=org_profile,
                    name=request.POST.get('name').strip(),
                    img=request.FILES['file'],
                    status=request.POST.get('status')
                )
        except Exception as e:
            return render(request, 'org-admin/create-banner.html', {'error_message': error_message})

        return redirect('banner')
    return render(request, 'org-admin/create-banner.html', {})


@login_required(login_url='login')
def update_banner(request, pk):
    if request.user.role != 'Org':
        return redirect('login')

    context = Banner.objects.get(id=pk)

    if request.method == 'POST':
        error_message = dict()
        org_profile = OrgProfile.objects.get(user=User.objects.get(username=str(request.user)))

        if request.POST.get('name').strip() == '':
            error_message['name_error'] = 'Empty field not allowed'

        if error_message:
            return render(request, 'org-admin/update-banner.html', {'context': context, 'error_message': error_message})

        try:
            check = request.FILES['file']
            Banner.objects.filter(id=pk).update(
                        user=org_profile,
                        name=request.POST.get('name').strip(),
                        status=request.POST.get('status')
                    )

            b = Banner.objects.get(id=pk)
            b.img = request.FILES['file']
            b.save()

        except Exception as e:
            Banner.objects.filter(id=pk).update(
                user=org_profile,
                name=request.POST.get('name').strip(),
                status=request.POST.get('status')
            )

        if error_message:
            return render(request, 'org-admin/update-banner.html', {'context': context, 'error_message': error_message})

        return redirect('banner')

    return render(request, 'org-admin/update-banner.html', {'context': context, 'BASE_URL': settings.BASE_URL})


@login_required(login_url='login')
def delete_banner(request, pk):
    if request.user.role == 'Org':
        Banner.objects.get(id=pk, user=OrgProfile.objects.get(user=User.objects.get(username=str(request.user)))).delete()
        return redirect('banner')
