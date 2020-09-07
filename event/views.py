from django.shortcuts import render


def event_list(request):
    return render(request, 'org-admin/event.html', {})