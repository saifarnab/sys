from django.shortcuts import render


def event_list(request):
    return render(request, 'org-admin/event.html', {})


def event_type(request):
    return render(request, 'org-admin/form-advanced.html', {})