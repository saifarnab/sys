from django.shortcuts import render
from userProfile.models import OrgProfile, TrainerProfile, MemberProfile
from event.models import Event, EventCategory, EventSubCategory, EventBranchVenue, EventType
from invoice.models import Confirm
from banner.models import Banner
from videos.models import Video


def dashboard(request):
    context = dict()
    if request.user.role == 'Admin':
        context['total_org'] = OrgProfile.objects.count()
        context['total_trainer'] = TrainerProfile.objects.count()
        context['total_member'] = MemberProfile.objects.count()
        context['total_event'] = Event.objects.count()
        context['total_type'] = EventType.objects.count()
        context['total_category'] = EventCategory.objects.count()
        context['total_subcategory'] = EventSubCategory.objects.count()
        context['confirm_event_pending'] = Confirm.objects.filter(status='Pending').count()
        context['confirm_event_approved'] = Confirm.objects.filter(status='Approved').count()

    elif request.user.role == 'Org':
        context['total_trainer'] = TrainerProfile.objects.filter(user=request.user).count()
        context['total_video'] = Video.objects.filter(user__user=request.user).count()
        context['total_event'] = Event.objects.filter(org__user=request.user).count()
        context['total_branch'] = EventBranchVenue.objects.filter(user__user=request.user).count()
        context['total_banner'] = Banner.objects.filter(user__user=request.user).count()
        context['confirm_event_pending'] = Confirm.objects.filter(status='Pending').count()
        context['confirm_event_approved'] = Confirm.objects.filter(status='Approved').count()

    return render(request, 'org-admin/index.html', {'context': context})
