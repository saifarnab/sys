import json

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import EventType, EventBranchVenue, EventCategory, EventSubCategory, Event
from userProfile.models import User, OrgProfile, TrainerProfile
from django.contrib.auth.decorators import login_required


""" Event Type """


@login_required(login_url='login')
def event_type(request):
    context = EventType.objects.all().values('id', 'name', 'created_at', 'updated_at', 'status')
    return render(request, 'org-admin/event-type.html', {'context': context})


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def delete_event_type(request, pk):
    if request.user.role == 'Admin':
        EventType.objects.get(id=pk).delete()
        return redirect('event-type')


""" Event Branch/Venue """


@login_required(login_url='login')
def event_branch_venue(request):

    if request.user.role == 'Admin':
        context = EventBranchVenue.objects.all().values('id', 'name', 'address', 'contact_no',  'created_at', 'updated_at', 'status', 'user__name')

    elif request.user.role == 'Org':
        org_profile = OrgProfile.objects.get(user=User.objects.get(username=str(request.user)))
        context = EventBranchVenue.objects.filter(user=org_profile).values('id', 'name', 'address', 'contact_no', 'created_at', 'updated_at', 'status')
    return render(request, 'org-admin/event-branch-venue.html', {'context': context})


@login_required(login_url='login')
def create_event_branch_venue(request):
    if request.method == 'POST':
        error_message = dict()
        org_profile = OrgProfile.objects.get(user=User.objects.get(username=str(request.user)))

        if request.POST.get('branch').strip() == '':
            error_message['branch_error'] = 'Empty field not allowed'

        elif list(EventBranchVenue.objects.filter(user=org_profile, name=request.POST.get('branch').strip())):
            error_message['branch_error'] = 'Already available'

        if request.POST.get('address').strip() == '':
            error_message['address_error'] = 'Empty field not allowed'

        if request.POST.get('contact_no').strip() == '':
            error_message['contact_no_error'] = 'Empty field not allowed'

        if error_message:
            return render(request, 'org-admin/create-event-branch-venue.html', {'error_message': error_message})

        try:
            if request.user.role == 'Org':
                EventBranchVenue.objects.create(
                    user=org_profile,
                    name=request.POST.get('branch').strip(),
                    address=request.POST.get('address').strip(),
                    contact_no=request.POST.get('contact_no').strip(),
                    status=request.POST.get('status')
                )
        except Exception as e:
            return render(request, 'org-admin/create-event-branch-venue.html', {'error_message': error_message})

        return redirect('event-branch-venue')
    return render(request, 'org-admin/create-event-branch-venue.html', {})


@login_required(login_url='login')
def update_event_branch_venue(request, pk):
    context = EventBranchVenue.objects.get(id=pk)

    if request.method == 'POST':
        error_message = dict()
        org_profile = OrgProfile.objects.get(user=User.objects.get(username=str(request.user)))

        if request.POST.get('branch').strip() == '':
            error_message['branch_error'] = 'Empty field not allowed'

        elif list(EventBranchVenue.objects.filter(user=org_profile, name=request.POST.get('branch').strip())):
            error_message['branch_error'] = 'Already available'

        if request.POST.get('address').strip() == '':
            error_message['address_error'] = 'Empty field not allowed'

        if request.POST.get('contact_no').strip() == '':
            error_message['contact_no_error'] = 'Empty field not allowed'

        if error_message:
            return render(request, 'org-admin/update-event-branch-venue.html', {'context': context, 'error_message': error_message})

        try:
            if request.user.role == 'Org':
                EventBranchVenue.objects.filter(id=pk).update(
                    user=org_profile,
                    name=request.POST.get('branch').strip(),
                    address=request.POST.get('address').strip(),
                    contact_no=request.POST.get('contact_no').strip(),
                    status=request.POST.get('status')
                )
        except Exception as e:
            error_message['general_error'] = 'Exception arise: Already available'

        if error_message:
            return render(request, 'org-admin/update-event-branch-venue.html', {'context': context, 'error_message': error_message})

        return redirect('event-branch-venue')

    return render(request, 'org-admin/update-event-branch-venue.html', {'context': context})


@login_required(login_url='login')
def delete_event_branch_venue(request, pk):
    if request.user.role == 'Org':
        EventBranchVenue.objects.get(id=pk).delete()
        return redirect('event-branch-venue')


""" Event Category """


@login_required(login_url='login')
def event_category(request):
    context = EventCategory.objects.all().values('id', 'name', 'created_at', 'updated_at', 'status')
    return render(request, 'org-admin/event-category.html', {'context': context})


@login_required(login_url='login')
def create_event_category(request):
    if request.user.role != 'Admin':
        return redirect('login')

    if request.method == 'POST':

        error_message = dict()

        if request.POST.get('category').strip() == '':
            error_message['category_error'] = 'Empty field not allowed'

        if list(EventCategory.objects.filter(name=request.POST.get('category'))):
            error_message['category_error'] = 'Already exists'

        if error_message:
            return render(request, 'org-admin/create-event-category.html', {'error_message': error_message})

        try:
            EventCategory.objects.create(
                name=request.POST.get('category').strip(),
                status=request.POST.get('status')
            )
        except Exception as e:
            return render(request, 'org-admin/create-event-category.html', {'error_message': 'Exception arise'})

        return redirect('event-category')
    return render(request, 'org-admin/create-event-category.html', {})


@login_required(login_url='login')
def update_event_category(request, pk):

    if request.user.role != 'Admin':
        return redirect('login')

    context = EventCategory.objects.get(id=pk)

    if request.method == 'POST':

        error_message = dict()

        if request.POST.get('category').strip() == '':
            error_message['category_error'] = 'Empty field not allowed'

        if error_message:
            print(error_message)
            return render(request, 'org-admin/update-event-category.html', {'context': context, 'error_message': error_message})

        try:
            EventCategory.objects.filter(id=pk).update(
                name=request.POST.get('category').strip(),
                status=request.POST.get('status')
            )
        except Exception as e:
            error_message['category_error'] = 'Already exists'
            return render(request, 'org-admin/update-event-category.html', {'context': context, 'error_message': error_message})

        return redirect('event-category')
    return render(request, 'org-admin/update-event-category.html', {'context': context})


@login_required(login_url='login')
def delete_event_category(request, pk):
    if request.user.role == 'Admin':
        EventCategory.objects.get(id=pk).delete()
        return redirect('event-category')
    else:
        return redirect('login')


""" Event Sub Category """


#  --- for AJAX call --- #

def get_event_sub_category(request, pk):
    print('hit ajax call method')
    context = list(EventSubCategory.objects.filter(category__id=pk).values('id', 'name'))
    return HttpResponse(context)


@login_required(login_url='login')
def event_sub_category(request):
    if request.user.role != 'Admin':
        return redirect('login')
    context = EventSubCategory.objects.all().values('id', 'name', 'category__name', 'created_at', 'updated_at', 'status')
    return render(request, 'org-admin/event-sub-category.html', {'context': context})


@login_required(login_url='login')
def create_event_sub_category(request):
    if request.user.role != 'Admin':
        return redirect('login')

    context = list(EventCategory.objects.filter(status='Active').values('id', 'name'))

    if request.method == 'POST':

        error_message = dict()

        if request.POST.get('sub_category').strip() == '':
            error_message['sub_category_error'] = 'Empty field not allowed'

        if list(EventCategory.objects.filter(name=request.POST.get('category'))):
            error_message['sub_category_error'] = 'Already exists'

        if error_message:
            print(error_message)
            return render(request, 'org-admin/create-event-sub-category.html', {'error_message': error_message, 'context': context})

        try:

            EventSubCategory.objects.create(
                name=request.POST.get('sub_category').strip(),
                category=EventCategory.objects.get(id=request.POST.get('category')),
                status=request.POST.get('status')
            )
        except Exception as e:
            print(e)
            return render(request, 'org-admin/create-event-sub-category.html', {'context': context, 'error_message': 'Exception arise'})

        return redirect('event-sub-category')

    return render(request, 'org-admin/create-event-sub-category.html', {'context': context})


@login_required(login_url='login')
def update_event_sub_category(request, pk):
    if request.user.role != 'Admin':
        return redirect('login')

    category_context = list(EventCategory.objects.filter(status='Active').values('id', 'name'))
    sub_category_context = EventSubCategory.objects.get(id=pk)

    if request.method == 'POST':

        error_message = dict()

        if request.POST.get('category').strip() == '':
            error_message['sub_category_error'] = 'Empty field not allowed'

        if error_message:
            return render(request, 'org-admin/update-event-sub-category.html',
                          {'error_message': error_message, 'category_context': category_context,
                           'sub_category_context': sub_category_context})

        try:
            EventSubCategory.objects.filter(id=pk).update(
                name=request.POST.get('sub_category').strip(),
                category=EventCategory.objects.get(id=request.POST.get('category')),
                status=request.POST.get('status')
            )

        except Exception as e:
            error_message['sub_category_error'] = 'Already exists'
            return render(request, 'org-admin/update-event-sub-category.html',
                          {'sub_category_context': sub_category_context,
                           'category_context': category_context, 'error_message': error_message})

        return redirect('event-sub-category')

    return render(request, 'org-admin/update-event-sub-category.html', {'sub_category_context': sub_category_context, 'category_context': category_context})


@login_required(login_url='login')
def delete_event_sub_category(request, pk):
    if request.user.role == 'Admin':
        EventSubCategory.objects.get(id=pk).delete()
        return redirect('event-sub-category')
    else:
        return redirect('login')


""" Events """


@login_required(login_url='login')
def event(request):
    if request.user.role != 'Admin':
        context = Event.objects.all().values('id', 'title', 'starting_date', 'trainer__name', 'status', 'type__name',
                                             'amount', 'discount')

    if request.user.role != 'Org':
        context = Event.objects.all().values('id', 'title', 'starting_date', 'trainer__name', 'status', 'type__name',
                                             'amount', 'discount')

    return render(request, 'org-admin/event.html', {'context': context})


@login_required(login_url='login')
def create_event(request):
    if request.user.role != 'Org':
        return redirect('login')

    category_context = list(EventCategory.objects.filter(status='Active').values('id', 'name'))
    type_context = list(EventType.objects.filter(status='Active').values('id', 'name'))
    branch_venue_context = list(EventBranchVenue.objects.filter(status='Active').values('id', 'name'))
    trainer_context = list(TrainerProfile.objects.all().values('id', 'name'))

    if request.method == 'POST':

        error_message = dict()

        if request.POST.get('sub_category').strip() == '':
            error_message['sub_category_error'] = 'Empty field not allowed'

        if list(Event.objects.filter(name=request.POST.get('category'))):
            error_message['sub_category_error'] = 'Already exists'

        if error_message:
            return render(request, 'org-admin/create-event.html', {
                'category_context': category_context,
                'type_context': type_context,
                'branch_venue_context': branch_venue_context,
                'trainer_context': trainer_context,
                'error_message': error_message
            })

        try:
            Event.objects.create(
                name=request.POST.get('sub_category').strip(),
                category=EventCategory.objects.get(id=request.POST.get('category')),
                status=request.POST.get('status')
            )
        except Exception as e:
            return render(request, 'org-admin/create-event.html', {
                'category_context': category_context,
                'type_context': type_context,
                'branch_venue_context': branch_venue_context,
                'trainer_context': trainer_context,
                'error_message': error_message
            })

        return redirect('event-sub-category')

    return render(request, 'org-admin/create-event.html', {
        'category_context': category_context,
        'type_context': type_context,
        'branch_venue_context': branch_venue_context,
        'trainer_context': trainer_context
    })


@login_required(login_url='login')
def update_event(request, pk):
    if request.user.role != 'Admin':
        return redirect('login')

    category_context = list(EventCategory.objects.filter(status='Active').values('id', 'name'))
    sub_category_context = EventSubCategory.objects.get(id=pk)

    if request.method == 'POST':

        error_message = dict()

        if request.POST.get('category').strip() == '':
            error_message['sub_category_error'] = 'Empty field not allowed'

        if error_message:
            return render(request, 'org-admin/update-event-sub-category.html',
                          {'error_message': error_message, 'category_context': category_context,
                           'sub_category_context': sub_category_context})

        try:
            EventSubCategory.objects.filter(id=pk).update(
                name=request.POST.get('sub_category').strip(),
                category=EventCategory.objects.get(id=request.POST.get('category')),
                status=request.POST.get('status')
            )

        except Exception as e:
            error_message['sub_category_error'] = 'Already exists'
            return render(request, 'org-admin/update-event-sub-category.html',
                          {'sub_category_context': sub_category_context,
                           'category_context': category_context, 'error_message': error_message})

        return redirect('event-sub-category')

    return render(request, 'org-admin/update-event-sub-category.html', {'sub_category_context': sub_category_context, 'category_context': category_context})


@login_required(login_url='login')
def delete_event(request, pk):
    if request.user.role == 'Admin':
        EventSubCategory.objects.get(id=pk).delete()
        return redirect('event-sub-category')
    else:
        return redirect('login')