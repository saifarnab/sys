from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from userProfile.models import User, OrgProfile
from django.contrib.auth.decorators import login_required
from django.conf import settings

""" Event Video """


@login_required(login_url='login')
def video(request):

    if request.user.role == 'Admin':
        context = Video.objects.all().values('id', 'name', 'video', 'created_at', 'updated_at', 'status', 'user__name')

    elif request.user.role == 'Org':
        org_profile = OrgProfile.objects.get(user=User.objects.get(username=str(request.user)))
        context = Video.objects.filter(user=org_profile).values('id', 'name', 'video', 'created_at', 'updated_at', 'status')
    return render(request, 'org-admin/video.html', {'context': context, 'BASE_URL': settings.BASE_URL})


@login_required(login_url='login')
def create_video(request):
    if request.method == 'POST':
        error_message = dict()
        org_profile = OrgProfile.objects.get(user=User.objects.get(username=str(request.user)))

        if request.POST.get('name').strip() == '':
            error_message['name_error'] = 'Empty field not allowed'

        elif list(Video.objects.filter(user=org_profile, name=request.POST.get('name').strip())):
            error_message['name_error'] = 'Already available'

        try:
            request.FILES['file']

        except Exception as e:
            error_message['video_error'] = 'Select a video'

        if error_message:
            return render(request, 'org-admin/create-video.html', {'error_message': error_message})

        try:
            if request.user.role == 'Org':
                Video.objects.create(
                    user=org_profile,
                    name=request.POST.get('name').strip(),
                    video=request.FILES['file'],
                    status=request.POST.get('status')
                )
        except Exception as e:
            return render(request, 'org-admin/create-video.html', {'error_message': error_message})

        return redirect('video')
    return render(request, 'org-admin/create-video.html', {})


@login_required(login_url='login')
def update_video(request, pk):

    context = Video.objects.get(id=pk)
    if request.method == 'POST':

        error_message = dict()
        org_profile = OrgProfile.objects.get(user=User.objects.get(username=str(request.user)))

        if request.POST.get('name').strip() == '':
            error_message['name_error'] = 'Empty field not allowed'

        if error_message:
            return render(request, 'org-admin/update-video.html', {'context': context, 'error_message': error_message})

        try:
            check = request.FILES['file']
            v = Video.objects.filter(id=pk).update(
                user=org_profile,
                name=request.POST.get('name').strip(),
                status=request.POST.get('status')
            )
            v = Video.objects.get(id=pk)
            v.video = request.FILES['file']
            v.save()
        except Exception as e:
            Video.objects.filter(id=pk).update(
                user=org_profile,
                name=request.POST.get('name').strip(),
                status=request.POST.get('status')
            )

        return redirect('video')
    return render(request, 'org-admin/update-video.html', {'context': context})


@login_required(login_url='login')
def delete_video(request, pk):
    if request.user.role == 'Org':
        Video.objects.get(id=pk, user=OrgProfile.objects.get(user=User.objects.get(username=str(request.user)))).delete()
        return redirect('video')
