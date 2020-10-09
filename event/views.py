import datetime
import json
import dateutil.parser
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import EventType, EventBranchVenue, EventCategory, EventSubCategory, Event
from userProfile.models import User, OrgProfile, TrainerProfile
from django.contrib.auth.decorators import login_required


def convert24(str1):
    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]
    elif str1[-2:] == "AM":
        return str1[:-2]
    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]
    else:
        return str(int(str1[:2]) + 12) + str1[2:8]


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
    return HttpResponse(json.dumps(context), content_type="application/json")


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
    if request.user.role == 'Admin':
        context = Event.objects.all().values('id', 'title', 'starting_date', 'trainer__name', 'status', 'type__name',
                                             'amount', 'discount', 'org__name')
        print(context)

    if request.user.role == 'Org':
        context = Event.objects.filter(org=OrgProfile.objects.get(user=User.objects.get(username=str(request.user)))).values('id', 'title', 'starting_date', 'trainer__name', 'status', 'type__name',
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

        if request.POST.get('title').strip() == '':
            error_message['title_error'] = 'Empty field not allowed'

        if request.POST.get('branch_venue') == '0':
            error_message['branch_venue_error'] = 'Select branch or venue'

        if request.POST.get('category') == '0':
            error_message['category_error'] = 'Select category'

        if request.POST.get('status') == '0':
            error_message['status_error'] = 'Select status'

        if request.POST.get('trainer') == '0':
            error_message['trainer_error'] = 'Select trainer'

        if request.POST.get('type') == '0':
            error_message['type_error'] = 'Select type'

        if request.POST.get('starting_date').strip() == '':
            error_message['starting_date_error'] = 'Select date'

        if request.POST.get('last_registration_date').strip() == '':
            error_message['last_registration_date_error'] = 'Select date'

        if request.POST.get('last_registration_date').strip() == '':
            error_message['last_registration_date_error'] = 'Select date'

        if request.POST.get('duration').strip() == '':
            error_message['duration_error'] = 'Provide duration in hours'

        if request.POST.get('session_per_week').strip() == '':
            error_message['session_per_week_error'] = 'Provide Session per week'

        if request.POST.get('session_start_time').strip() == '':
            error_message['session_start_time_error'] = 'Provide event start time'

        if request.POST.get('session_end_time').strip() == '':
            error_message['session_end_time_error'] = 'Provide event end time'

        if request.POST.get('amount').strip() == '':
            error_message['amount_error'] = 'Provide event amount'

        if request.POST.get('discount').strip() == '':
            error_message['discount_error'] = 'Provide event discount'

        if request.POST.get('event_details') == '':
            error_message['event_details_error'] = 'Provide event details'

        try:
            thumbnail = request.FILES['file']
        except Exception as e:
            error_message['img_error'] = 'Select an image'

        if error_message:
            print('hit error')
            context = dict()
            context['title'] = request.POST.get('title').strip()
            context['branch_venue'] = request.POST.get('branch_venue')
            context['type'] = request.POST.get('type')
            context['status'] = request.POST.get('status')
            context['category'] = request.POST.get('category')
            try:
                context['sub_category'] = EventSubCategory.objects.get(id=request.POST.get('sub_category'))
            except Exception as e:
                context['sub_category'] = {'id': 0}

            context['trainer'] = request.POST.get('trainer')
            context['starting_date'] = request.POST.get('starting_date')
            context['last_registration_date'] = request.POST.get('last_registration_date')
            context['duration'] = request.POST.get('duration').strip()
            context['session_per_week'] = request.POST.get('session_per_week').strip()
            context['session_start_time'] = request.POST.get('session_start_time').strip()
            context['session_end_time'] = request.POST.get('session_end_time').strip()
            context['amount'] = request.POST.get('amount').strip()
            context['discount'] = request.POST.get('discount').strip()

            return render(request, 'org-admin/create-event.html', {
                'context': context,
                'category_context': category_context,
                'type_context': type_context,
                'branch_venue_context': branch_venue_context,
                'trainer_context': trainer_context,
                'error_message': error_message
            })
        else:
            try:
                print('hit try')
                org = OrgProfile.objects.get(user=User.objects.get(username=str(request.user)))
                trainer = TrainerProfile.objects.get(id=request.POST.get('trainer'))
                branch_venue = EventBranchVenue.objects.get(id=request.POST.get('branch_venue'))
                type = EventType.objects.get(id=request.POST.get('type'))
                category = EventCategory.objects.get(id=request.POST.get('category'))
                sub_category = EventSubCategory.objects.get(id=request.POST.get('sub_category'))

                Event.objects.create(
                    org=org,
                    title=request.POST.get('title').strip(),
                    trainer=trainer,
                    category=category,
                    sub_category=sub_category,
                    starting_date=request.POST.get('starting_date'),
                    last_registration_date=request.POST.get('last_registration_date'),
                    duration=request.POST.get('duration').strip(),
                    session_per_week=request.POST.get('session_per_week').strip(),
                    session_start_time=request.POST.get('session_start_time'),
                    session_end_time=request.POST.get('session_end_time'),
                    thumbnail=request.FILES['file'],
                    type=type,
                    branch_venue=branch_venue,
                    amount=request.POST.get('amount').strip(),
                    discount=request.POST.get('discount').strip(),
                    content=request.POST.get('event_details'),
                    status=request.POST.get('status')
                )
                return redirect('event')
            except Exception as e:
                print(e)

    return render(request, 'org-admin/create-event.html', {
        'category_context': category_context,
        'type_context': type_context,
        'branch_venue_context': branch_venue_context,
        'trainer_context': trainer_context
    })


@login_required(login_url='login')
def update_event(request, pk):

    context = Event.objects.get(id=pk)
    category_context = list(EventCategory.objects.filter(status='Active').values('id', 'name'))
    type_context = list(EventType.objects.filter(status='Active').values('id', 'name'))
    branch_venue_context = list(EventBranchVenue.objects.filter(status='Active').values('id', 'name'))
    trainer_context = list(TrainerProfile.objects.all().values('id', 'name'))

    if request.method == 'POST':
        error_message = dict()
        thumbnail = None

        if request.POST.get('title').strip() == '':
            error_message['title_error'] = 'Empty field not allowed'

        if request.POST.get('branch_venue') == '0':
            error_message['branch_venue_error'] = 'Select branch or venue'

        if request.POST.get('category') == '0':
            error_message['category_error'] = 'Select category'

        if request.POST.get('status') == '0':
            error_message['status_error'] = 'Select status'

        if request.POST.get('trainer') == '0':
            error_message['trainer_error'] = 'Select trainer'

        if request.POST.get('type') == '0':
            error_message['type_error'] = 'Select type'

        if request.POST.get('starting_date').strip() == '':
            error_message['starting_date_error'] = 'Select date'

        if request.POST.get('last_registration_date').strip() == '':
            error_message['last_registration_date_error'] = 'Select date'

        if request.POST.get('last_registration_date').strip() == '':
            error_message['last_registration_date_error'] = 'Select date'

        if request.POST.get('duration').strip() == '':
            error_message['duration_error'] = 'Provide duration in hours'

        if request.POST.get('session_per_week').strip() == '':
            error_message['session_per_week_error'] = 'Provide Session per week'

        if request.POST.get('session_start_time').strip() == '':
            error_message['session_start_time_error'] = 'Provide event start time'

        if request.POST.get('session_end_time').strip() == '':
            error_message['session_end_time_error'] = 'Provide event end time'

        if request.POST.get('amount').strip() == '':
            error_message['amount_error'] = 'Provide event amount'

        if request.POST.get('discount').strip() == '':
            error_message['discount_error'] = 'Provide event discount'

        if request.POST.get('event_details') == '':
            error_message['event_details_error'] = 'Provide event details'

        if request.user.role == 'Admin':
            if request.POST.get('featured') is None:
                Event.objects.filter(id=pk).update(featured=False)
            else:
                Event.objects.filter(id=pk).update(featured=True)

            if request.POST.get('top_rated') is None:
                Event.objects.filter(id=pk).update(top_rated=False)
            else:
                Event.objects.filter(id=pk).update(top_rated=True)

            if request.POST.get('most_popular') is None:
                Event.objects.filter(id=pk).update(most_popular=False)
            else:
                Event.objects.filter(id=pk).update(most_popular=True)

            if request.POST.get('best_sell') is None:
                Event.objects.filter(id=pk).update(best_sell=False)
            else:
                Event.objects.filter(id=pk).update(best_sell=True)

        try:
            e = Event.objects.get(id=pk)
            e.thumbnail = request.FILES['file']
            e.save()
        except Exception as e:
            pass

        if error_message:
            context = dict()
            context['id'] = pk
            context['title'] = request.POST.get('title').strip()
            context['branch_venue'] = EventBranchVenue.objects.get(id=request.POST.get('branch_venue'))
            context['type'] = EventType.objects.get(id=request.POST.get('type'))
            context['status'] = request.POST.get('status')
            context['category'] = EventCategory.objects.get(id=request.POST.get('category'))
            context['sub_category'] = EventSubCategory.objects.get(id=request.POST.get('sub_category'))
            context['trainer'] = TrainerProfile.objects.get(id=request.POST.get('trainer'))
            context['starting_date'] = dateutil.parser.parse(request.POST.get('starting_date'))
            context['last_registration_date'] = dateutil.parser.parse(request.POST.get('last_registration_date'))
            context['duration'] = request.POST.get('duration').strip()
            context['session_per_week'] = request.POST.get('session_per_week').strip()
            context['session_start_time'] = request.POST.get('session_start_time').strip()
            context['session_end_time'] = request.POST.get('session_end_time').strip()
            context['amount'] = request.POST.get('amount').strip()
            context['discount'] = request.POST.get('discount').strip()
            context['event_details'] = request.POST.get('event_details')

            return render(request, 'org-admin/update-event.html', {
                'context': context,
                'category_context': category_context,
                'type_context': type_context,
                'branch_venue_context': branch_venue_context,
                'trainer_context': trainer_context,
                'error_message': error_message
            })
        else:
            try:
                trainer = TrainerProfile.objects.get(id=request.POST.get('trainer'))
                branch_venue = EventBranchVenue.objects.get(id=request.POST.get('branch_venue'))
                event_type = EventType.objects.get(id=request.POST.get('type'))
                category = EventCategory.objects.get(id=request.POST.get('category'))
                sub_category = EventSubCategory.objects.get(id=request.POST.get('sub_category'))

                if thumbnail:
                    event = Event.objects.filter(id=pk).update(
                        title=request.POST.get('title').strip(),
                        trainer=trainer,
                        category=category,
                        sub_category=sub_category,
                        starting_date=request.POST.get('starting_date'),
                        last_registration_date=request.POST.get('last_registration_date'),
                        duration=request.POST.get('duration').strip(),
                        session_per_week=request.POST.get('session_per_week').strip(),
                        session_start_time=request.POST.get('session_start_time'),
                        session_end_time=request.POST.get('session_end_time'),
                        type=event_type,
                        branch_venue=branch_venue,
                        amount=request.POST.get('amount').strip(),
                        discount=request.POST.get('discount').strip(),
                        content=request.POST.get('event_details'),
                        status=request.POST.get('status')
                    )
                    event.thumbnail = request.FILES['file']
                    event.save()
                else:
                    Event.objects.filter(id=pk).update(
                        title=request.POST.get('title').strip(),
                        trainer=trainer,
                        category=category,
                        sub_category=sub_category,
                        starting_date=request.POST.get('starting_date'),
                        last_registration_date=request.POST.get('last_registration_date'),
                        duration=request.POST.get('duration').strip(),
                        session_per_week=request.POST.get('session_per_week').strip(),
                        session_start_time=request.POST.get('session_start_time'),
                        session_end_time=request.POST.get('session_end_time'),
                        type=event_type,
                        branch_venue=branch_venue,
                        amount=request.POST.get('amount').strip(),
                        discount=request.POST.get('discount').strip(),
                        content=request.POST.get('event_details'),
                        status=request.POST.get('status')
                    )
                return redirect('event')
            except Exception as e:
                print(e)
    context.session_start_time = str(context.session_start_time)
    context.session_end_time = str(context.session_end_time)

    return render(request, 'org-admin/update-event.html', {
        'BASE_URL': settings.BASE_URL,
        'context': context,
        'category_context': category_context,
        'type_context': type_context,
        'branch_venue_context': branch_venue_context,
        'trainer_context': trainer_context
    })


@login_required(login_url='login')
def delete_event(request, pk):
    if request.user.role == 'Admin':
        Event.objects.get(id=pk).delete()
        return redirect('event')
    else:
        org = OrgProfile.objects.get(user=User.objects.get(username=str(request.user)))
        Event.objects.get(id=pk, org=org).delete()
        return redirect('event')