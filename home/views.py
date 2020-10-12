from django.shortcuts import render
from event.models import EventCategory, EventSubCategory, Event, EventBranchVenue
from slider.models import Slider
from userProfile.models import OrgProfile
from banner.models import Banner
from django.conf import settings


def home(request):
    context = dict()
    context['BASE_URL'] = settings.BASE_URL
    context['category'] = EventCategory.objects.filter(status='Active').values('id', 'name')
    context['slider'] = Slider.objects.filter(status='Active').values('id', 'img')
    context['sub_category'] = EventSubCategory.objects.filter(status='Active').values('id', 'name', 'category__name')
    context['event'] = Event.objects.filter(status='Active').values('id', 'org__id', 'org__name', 'trainer__name',
                                                                    'title',
                                                                    'amount', 'discount', 'category__name', 'thumbnail',
                                                                    'featured', 'most_popular', 'top_rated',
                                                                    'best_sell')
    return render(request, 'home/index.html', {'context': context})


def org_home(request, pk):
    context = dict()
    context['org'] = OrgProfile.objects.get(id=pk)
    context['branch'] = EventBranchVenue.objects.filter(id=pk)
    context['BASE_URL'] = settings.BASE_URL
    context['category'] = EventCategory.objects.filter(status='Active').values('id', 'name')
    context['slider'] = Banner.objects.filter(status='Active', user__user=request.user).values('id', 'img')
    context['sub_category'] = EventSubCategory.objects.filter(status='Active').values('id', 'name', 'category__name')
    context['event'] = Event.objects.filter(status='Active', org__user=request.user).values('id', 'org__name',
                                                                                            'trainer__name', 'title',
                                                                                            'amount', 'discount',
                                                                                            'category__name',
                                                                                            'thumbnail', )
    return render(request, 'home/organization.html', {'context': context})


def event_details(request, pk):
    context = dict()
    context['BASE_URL'] = settings.BASE_URL
    context['event'] = Event.objects.filter(featured=True).values('id', 'org__name', 'trainer__name', 'title',
                                                                                    'amount', 'discount',
                                                                                    'category__name',
                                                                                    'thumbnail', 'featured')

    context['event_details'] = Event.objects.get(id=pk)

    context['similar_event'] = Event.objects.filter(category__name=context['event_details'].category.name).values('id', 'org__id', 'org__name', 'trainer__name',
                                                                                  'title', 'amount', 'discount', 'category__name', 'thumbnail', 'featured')
    return render(request, 'home/event_details.html', {'context': context})


def register(request):
    context = dict()
    return render(request, 'reg_login/register.html', {'context': context})


def login(request):
    context = dict()
    return render(request, 'reg_login/login.html', {'context': context})




