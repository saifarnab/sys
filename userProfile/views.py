from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User, TrainerProfile


def sign_in(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('email').strip(), password=request.POST.get('password'))
        print(request.POST.get('password'))
        if user is not None:
            try:
                print(request, user)
                login(request, user)
            except Exception as e:
                print(e)
            return redirect('event')

    return render(request, 'org-admin/login.html', {})


def sign_out(request):
    logout(request)
    return render(request, 'org-admin/login.html', {})


def org_trainer(request):
    context = dict()
    if request.user.role == 'Org':
        context['trainer'] = TrainerProfile.objects.filter(user=request.user)
    if request.user.role == 'Admin':
        context['trainer'] = TrainerProfile.objects.all()
    return render(request, 'org-admin/trainer.html', {'context': context})


def create_trainer(request):
    context = dict()
    if request.user.role != 'Org':
        return redirect('admin-login')
    if request.method == 'POST':
        error_message = dict()

        name = request.POST.get('name').strip()
        email = request.POST.get('email').strip()
        phone = request.POST.get('phone').strip()
        address = request.POST.get('address').strip()
        facebook = request.POST.get('facebook').strip()
        twitter = request.POST.get('twitter').strip()
        linkedin = request.POST.get('linkedin').strip()
        education = request.POST.get('education')
        experience = request.POST.get('experience')

        if name == '':
            error_message['name_error'] = 'Empty field not allowed'

        if email == '':
            error_message['email_error'] = 'Empty field not allowed'

        context['name'] = name
        context['email'] = email
        context['phone'] = phone
        context['address'] = address
        context['facebook'] = facebook
        context['twitter'] = twitter
        context['linkedin'] = linkedin
        context['education'] = education
        context['experience'] = experience
        if error_message:
            return render(request, 'org-admin/create-trainer.html', {'context': context, 'error_message': error_message})

        try:
            trainer = TrainerProfile.objects.create(
                user=request.user,
                name=name,
                email=email,
                contact_number=phone,
                address=address,
                facebook_link=facebook,
                twitter_link=twitter,
                linkedin_link=linkedin,
                education=education,
                experience=experience,
                status=request.POST.get('status')
            )
            try:
                trainer.img = request.FILES['file']
                trainer.save()
            except Exception as e:
                print('hit exception')
        except Exception as e:
            error_message['email_error'] = 'Email already available'
            return render(request, 'org-admin/create-trainer.html', {'context': context, 'error_message': error_message})

        return redirect('org-trainer')

    return render(request, 'org-admin/create-trainer.html', {})


def update_trainer(request, pk):
    context = dict()
    trainer = TrainerProfile.objects.get(id=pk)
    if request.method == 'POST':
        error_message = dict()
        name = request.POST.get('name').strip()
        phone = request.POST.get('phone').strip()
        address = request.POST.get('address').strip()
        facebook = request.POST.get('facebook').strip()
        twitter = request.POST.get('twitter').strip()
        linkedin = request.POST.get('linkedin').strip()
        education = request.POST.get('education')
        experience = request.POST.get('experience')

        if name == '':
            error_message['name_error'] = 'Empty field not allowed'

        context['name'] = name
        context['phone'] = phone
        context['address'] = address
        context['facebook'] = facebook
        context['twitter'] = twitter
        context['linkedin'] = linkedin
        context['education'] = education
        context['experience'] = experience
        if error_message:
            return render(request, 'org-admin/update-trainer.html', {'context': context, 'error_message': error_message})

        try:
            trainer = TrainerProfile.objects.filter(id=pk).update(
                name=name,
                contact_number=phone,
                address=address,
                facebook_link=facebook,
                twitter_link=twitter,
                linkedin_link=linkedin,
                status=request.POST.get('status')
            )
            try:
                trainer = TrainerProfile.objects.get(id=pk)
                trainer.img = request.FILES['file']
                trainer.save()
            except Exception as e:
                print('hit exception')
        except Exception as e:
           pass

        return redirect('org-trainer')

    return render(request, 'org-admin/update-trainer.html', {'trainer': trainer})


def delete_trainer(request, pk):
    try:
        TrainerProfile.objects.filter(id=pk).delete()
    except Exception as e:
        pass
    return redirect('org-trainer')