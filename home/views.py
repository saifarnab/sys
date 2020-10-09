from django.shortcuts import render
from event.models import EventCategory, EventSubCategory, Event
from django.conf import settings


def home(request):
    context = dict()
    context['BASE_URL'] = settings.BASE_URL
    context['category'] = EventCategory.objects.filter(status='Active').values('id', 'name')
    context['sub_category'] = EventSubCategory.objects.filter(status='Active').values('id', 'name', 'category__name')
    context['event'] = Event.objects.filter(status='Active').values('id', 'org__name', 'trainer__name', 'title',
                                                                    'amount', 'discount', 'category__name', 'thumbnail',
                                                                    'featured', 'most_popular', 'top_rated', 'best_sell')
    print(context['BASE_URL'])
    return render(request, 'home/index.html', {'context': context})
