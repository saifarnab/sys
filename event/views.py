from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import EventType, EventBranchVenue
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def event_list(request):
    return render(request, 'org-admin/event.html', {})


def event_type(request):
    context = EventType.objects.all().values('id', 'name', 'created_at', 'updated_at', 'status')
    return render(request, 'org-admin/event-type.html', {'context': context})


def create_event_type(request):
    if request.method == 'POST':
        if request.POST.get('type') == '':
            return render(request, 'org-admin/create-event-type.html', {'type_error_message': 'Empty field not allowed!'})
        if list(EventType.objects.filter(name=request.POST.get('type'))):
            return render(request, 'org-admin/create-event-type.html', {'type_error_message': 'Type already exists!'})

        try:
            EventType.objects.create(name=request.POST.get('type'), status=request.POST.get('status'))
        except Exception as e:
            return render(request, 'org-admin/create-event-type.html', {'type_error_message': e})

        return redirect('event-type')

    return render(request, 'org-admin/create-event-type.html', {})


def update_event_type(request, pk):

    if request.method == 'POST':
        event = EventType.objects.get(id=pk)

        if request.POST.get('type') == '':
            return render(request, 'org-admin/update-event-type.html', {'context': event, 'type_error_message': 'Empty field not allowed!'})

        try:
            EventType.objects.filter(id=pk).update(name=request.POST.get('type'), status=request.POST.get('status'))
        except Exception as e:
            return render(request, 'org-admin/update-event-type.html', {'context': event, 'type_error_message': e})

        return redirect('event-type')

    event = EventType.objects.get(id=pk)
    return render(request, 'org-admin/update-event-type.html', {'context': event})


def delete_event_type(request, pk):
    EventType.objects.get(id=pk).delete()
    return redirect('event-type')


def event_branch_venue(request):
    context = EventBranchVenue.objects.all().values('id', 'name', 'created_at', 'updated_at')
    return render(request, 'org-admin/event-type.html', {'context': context})


def create_event_branch_venue(request):
    if request.method == 'POST':
        if request.POST.get('type') == '':
            return render(request, 'org-admin/create-event-type.html', {'type_error_message': 'Empty field not allowed!'})
        if list(EventType.objects.filter(user=request.user, name=request.POST.get('type'))):
            return render(request, 'org-admin/create-event-type.html', {'type_error_message': 'Type already exists!'})

        try:
            EventType.objects.create(name=request.POST.get('type'))
        except Exception as e:
            return render(request, 'org-admin/create-event-type.html', {'type_error_message': e})

        return redirect('')
    return render(request, 'org-admin/create-event-type.html', {})
