from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from event.models import EventCategory, EventSubCategory, Event, EventBranchVenue
from slider.models import Slider
from userProfile.models import OrgProfile, MemberProfile, User, TrainerProfile
from banner.models import Banner
from invoice.models import Cart
from django.conf import settings
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum


def home(request):
    context = dict()
    context['BASE_URL'] = settings.BASE_URL
    context['category'] = EventCategory.objects.filter(status='Active').values('id', 'name')
    context['slider'] = Slider.objects.filter(status='Active').values('id', 'img')
    context['sub_category'] = EventSubCategory.objects.filter(status='Active').values('id', 'name', 'category__name')
    if not request.user.is_anonymous:
        context['current_cart_data_amount'] = len(list(Cart.objects.filter(user=request.user)))
        if request.user.role == 'Org':
            context['org_account'] = OrgProfile.objects.get(user=request.user)
    context['event'] = Event.objects.filter(status='Active').values('id', 'org__id', 'org__name', 'trainer__name',
                                                                    'title', 'trainer__id',
                                                                    'amount', 'discount', 'category__name', 'thumbnail',
                                                                    'featured', 'most_popular', 'top_rated',
                                                                    'best_sell')

    return render(request, 'home/index.html', {'context': context})


def org_home(request, pk):
    context = dict()
    context['org'] = OrgProfile.objects.get(id=pk)
    context['branch'] = EventBranchVenue.objects.filter(user=context['org'])
    context['BASE_URL'] = settings.BASE_URL
    context['category'] = EventCategory.objects.filter(status='Active').values('id', 'name')
    context['slider'] = Banner.objects.filter(status='Active', user=context['org']).values('id', 'img')
    if not request.user.is_anonymous:
        context['current_cart_data_amount'] = len(list(Cart.objects.filter(user=request.user)))
        if request.user.role == 'Org':
            context['org_account'] = OrgProfile.objects.get(user=request.user)
    context['sub_category'] = EventSubCategory.objects.filter(status='Active').values('id', 'name', 'category__name')
    context['event'] = Event.objects.filter(status='Active', org__id=pk).values('id', 'org__name',
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
    if not request.user.is_anonymous:
        context['current_cart_data_amount'] = len(list(Cart.objects.filter(user=request.user)))
        if request.user.role == 'Org':
            context['org_account'] = OrgProfile.objects.get(user=request.user)
    context['similar_event'] = Event.objects.filter(category__name=context['event_details'].category.name).values('id', 'org__id', 'org__name', 'trainer__name',
                                                                                  'title', 'amount', 'discount', 'category__name', 'thumbnail', 'featured')
    return render(request, 'home/event_details.html', {'context': context})


def sub_category_search(request, pk):
    context = dict()

    context['BASE_URL'] = settings.BASE_URL
    context['category'] = EventCategory.objects.filter(status='Active').values('id', 'name')
    context['slider'] = Slider.objects.filter(status='Active').values('id', 'img')
    context['sub_cat_name'] = EventSubCategory.objects.get(id=pk)
    if not request.user.is_anonymous:
        context['current_cart_data_amount'] = len(list(Cart.objects.filter(user=request.user)))
        if request.user.role == 'Org':
            context['org_account'] = OrgProfile.objects.get(user=request.user)
    context['sub_category'] = EventSubCategory.objects.filter(status='Active').values('id', 'name', 'category__name')
    context['event'] = Event.objects.filter(status='Active', featured=True).values('id', 'org__id', 'org__name', 'trainer__name',
                                                                    'title',
                                                                    'amount', 'discount', 'category__name', 'thumbnail',
                                                                    'featured', 'most_popular', 'top_rated',
                                                                    'best_sell')
    context['sub_cat_event'] = Event.objects.filter(status='Active', sub_category__id=pk).values('id', 'org__id', 'org__name',
                                                                                         'trainer__name',
                                                                                         'title',
                                                                                         'amount', 'discount',
                                                                                         'category__name', 'thumbnail')

    page = request.GET.get('page', 1)
    paginator = Paginator(context['sub_cat_event'], 12)

    try:
        context['sub_cat_event'] = paginator.page(page)
    except PageNotAnInteger:
        context['sub_cat_event'] = paginator.page(1)
    except EmptyPage:
        context['sub_cat_event'] = paginator.page(paginator.num_pages)

    return render(request, 'home/sub_category_search.html', {'context': context})


def org_sub_category_search(request, org_id, pk):
    context = dict()
    context['org'] = OrgProfile.objects.get(id=org_id)
    context['branch'] = EventBranchVenue.objects.filter(user=context['org'])
    context['BASE_URL'] = settings.BASE_URL
    context['category'] = EventCategory.objects.filter(status='Active').values('id', 'name')
    context['sub_cat_name'] = EventSubCategory.objects.get(id=pk)
    if not request.user.is_anonymous:
        context['current_cart_data_amount'] = len(list(Cart.objects.filter(user=request.user)))
        if request.user.role == 'Org':
            context['org_account'] = OrgProfile.objects.get(user=request.user)
    context['slider'] = Banner.objects.filter(status='Active', user=context['org']).values('id', 'img')
    context['sub_category'] = EventSubCategory.objects.filter(status='Active').values('id', 'name', 'category__name')
    context['sub_cat_event'] = Event.objects.filter(status='Active', sub_category__id=pk, org=context['org']).values('id', 'org__id',
                                                                                                 'org__name',
                                                                                                 'trainer__name',
                                                                                                 'title',
                                                                                                 'amount', 'discount',
                                                                                                 'category__name',
                                                                                                 'thumbnail')

    page = request.GET.get('page', 1)
    paginator = Paginator(context['sub_cat_event'], 12)

    try:
        context['sub_cat_event'] = paginator.page(page)
    except PageNotAnInteger:
        context['sub_cat_event'] = paginator.page(1)
    except EmptyPage:
        context['sub_cat_event'] = paginator.page(paginator.num_pages)

    return render(request, 'home/org_sub_category_search.html', {'context': context})


def register(request):
    context = dict()
    error = dict()
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password').strip()
        agree_term = request.POST.get('agree_term')

        if name == '':
            error['name'] = 'Enter your name'
        if email == '':
            error['email'] = 'Enter your email'
        if password == '':
            error['password'] = 'Enter your password'
        if confirm_password == '':
            error['confirm_password'] = 'Confirm your password'
        if password != confirm_password:
            error['confirm_password'] = "Password does not match"
        if agree_term is None:
            error['agree_term'] = 'Please check terms and conditions'

        context['error'] = error

        if error:
            context['name'] = name
            context['email'] = email
            context['password'] = password
            context['confirm_password'] = confirm_password

        else:
            user = User.objects.create_user(username=email,
                                            email=email,
                                            password=password,
                                            role="Member")

            if user:
                MemberProfile.objects.create(email=email, user=user, name=name)
                user_login(request, user)
                return redirect('home')

    return render(request, 'reg_login/register.html', {'context': context})


def register_as_org(request):
    context = dict()
    error = dict()
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password').strip()
        agree_term = request.POST.get('agree_term')

        if name == '':
            error['name'] = 'Enter your organization name'
        if email == '':
            error['email'] = 'Enter your organization email'
        if password == '':
            error['password'] = 'Enter your password'
        if confirm_password == '':
            error['confirm_password'] = 'Confirm your password'
        if password != confirm_password:
            error['confirm_password'] = "Password does not match"
        if agree_term is None:
            error['agree_term'] = 'Please check terms and conditions'

        context['error'] = error

        if error:
            context['name'] = name
            context['email'] = email
            context['password'] = password
            context['confirm_password'] = confirm_password

        else:
            user = User.objects.create_user(username=email,
                                            email=email,
                                            password=password,
                                            role="Org")

            if user:
                OrgProfile.objects.create(email=email, user=user, name=name)
                user_login(request, user)
                return redirect('admin-login')

    return render(request, 'reg_login/register_as_org.html', {'context': context})


@login_required(login_url='login')
def save_to_cart(request):
    event = Event.objects.get(id=request.POST.get('event_id'))
    try:
        Cart.objects.get(user=request.user, event=event)
    except:
        Cart.objects.create(user=request.user, event=event)
    current_cart_data_amount = len(list(Cart.objects.filter(user=request.user)))
    return HttpResponse(current_cart_data_amount)


@login_required(login_url='login')
def user_cart(request):
    context = dict()
    if request.user.is_anonymous:
        return redirect('login')
    if request.user.role == 'Org':
        return redirect('login')
    context['current_cart_data_amount'] = len(list(Cart.objects.filter(user=request.user)))
    context['cart'] = Cart.objects.filter(user=request.user)
    context['total_amount'] = Cart.objects.aggregate(Sum('event__amount'))
    context['total_discount'] = Cart.objects.aggregate(Sum('event__discount'))
    return render(request, 'home/cart.html', {'context': context})


@login_required(login_url='login')
def delete_event_from_cart(request, pk):
    try:
        Cart.objects.filter(id=pk, user=request.user).delete()
        return redirect('cart')
    except:
        return redirect('login')


def login(request):
    context = dict()

    if request.method == 'POST':
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        try:
            user = authenticate(username=email, password=password)
            user_login(request, user)
            return redirect('home')
        except Exception as e:
            context['error'] = 'Email and password does not match'

    return render(request, 'reg_login/login.html', {'context': context})


@login_required(login_url='login')
def logout(request):
    user_logout(request)
    return redirect('home')


@login_required(login_url='login')
def user_profile(request):
    context = dict()
    if request.method == "POST":
        name = request.POST.get('name').strip()
        phone = request.POST.get('phone').strip()
        address = request.POST.get('address').strip()
        facebook = request.POST.get('facebook').strip()
        twitter = request.POST.get('twitter').strip()
        linkedin = request.POST.get('linkedin').strip()
        education = request.POST.get('education')

        MemberProfile.objects.filter(user=request.user).update(
            name=name,
            contact_number=phone,
            address=address,
            facebook_link=facebook,
            twitter_link=twitter,
            linkedin_link=linkedin,
            education=education
        )
        try:
            b = MemberProfile.objects.get(user=request.user)
            b.img = request.FILES['img']
            b.save()
        except:
            print('hit exception')

    context['BASE_URL'] = settings.BASE_URL
    context['event'] = Event.objects.filter(featured=True).values('id', 'org__id', 'trainer__id', 'org__name', 'trainer__name', 'title',
                                                                  'amount', 'discount',
                                                                  'category__name',
                                                                  'thumbnail', 'featured')
    context['current_cart_data_amount'] = len(list(Cart.objects.filter(user=request.user)))
    context['profile'] = MemberProfile.objects.get(user=request.user)
    return render(request, 'home/user.html', {'context': context})


@login_required(login_url='login')
def trainer_profile(request, pk):
    context = dict()
    context['BASE_URL'] = settings.BASE_URL
    context['event'] = Event.objects.filter(featured=True).values('id', 'org__id', 'trainer__id', 'org__name', 'trainer__name', 'title',
                                                                  'amount', 'discount',
                                                                  'category__name',
                                                                  'thumbnail', 'featured')
    context['current_cart_data_amount'] = len(list(Cart.objects.filter(user=request.user)))
    context['profile'] = TrainerProfile.objects.get(id=pk)
    return render(request, 'home/trainer.html', {'context': context})


def home_search(request):
    context = dict()
    search = request.POST.get('search').strip()
    context['BASE_URL'] = settings.BASE_URL
    context['search'] = search
    context['category'] = EventCategory.objects.filter(status='Active').values('id', 'name')
    context['slider'] = Slider.objects.filter(status='Active').values('id', 'img')
    context['sub_category'] = EventSubCategory.objects.filter(status='Active').values('id', 'name', 'category__name')
    if not request.user.is_anonymous:
        context['current_cart_data_amount'] = len(list(Cart.objects.filter(user=request.user)))
        if request.user.role == 'Org':
            context['org_account'] = OrgProfile.objects.get(user=request.user)
    context['event'] = Event.objects.filter(status='Active', featured=True).values('id', 'org__id', 'org__name', 'trainer__name',
                                                                            'title', 'amount', 'discount', 'category__name', 'thumbnail',
                                                                            'featured', 'most_popular', 'top_rated', 'best_sell')
    context['search_event'] = Event.objects.filter(status='Active', title__icontains=search).values('id', 'org__id',
                                                                                             'org__name',
                                                                                             'trainer__name',
                                                                                             'title', 'amount',
                                                                                             'discount',
                                                                                             'category__name',
                                                                                             'thumbnail')

    page = request.GET.get('page', 1)
    paginator = Paginator(context['search_event'], 12)

    try:
        context['search_event'] = paginator.page(page)
    except PageNotAnInteger:
        context['search_event'] = paginator.page(1)
    except EmptyPage:
        context['search_event'] = paginator.page(paginator.num_pages)

    return render(request, 'home/home_search.html', {'context': context})





