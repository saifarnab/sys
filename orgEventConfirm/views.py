from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from invoice.models import Confirm
from event.models import Event
from userProfile.models import MemberProfile


@login_required(login_url='admin-login')
def orgEventConfirm(request):

    if request.user.role == 'Admin':
        context = Confirm.objects.all()

    elif request.user.role == 'Org':
        context = Confirm.objects.filter(event__org__user=request.user)
    return render(request, 'org-admin/orgEventConfirm.html', {'context': context, 'BASE_URL': settings.BASE_URL})


def updateOrgEventConfirm(request, pk):
    if request.method == 'POST':
        Confirm.objects.filter(id=pk).update(status=request.POST.get('status'))
        return redirect('org-event-confirm')
    context = dict()
    context['confirm'] = Confirm.objects.get(id=pk, event__org__user=request.user)
    context['member'] = MemberProfile.objects.get(user=context['confirm'].user)
    return render(request, 'org-admin/update-orgEventConfirm.html', {'context': context, 'BASE_URL': settings.BASE_URL})


def deleteOrgEventConfirm(request, pk):
    Confirm.objects.filter(id=pk).delete()
    return redirect('org-event-confirm')