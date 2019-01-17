from django.shortcuts import render, HttpResponseRedirect
from accounts.forms import AccountLoginForm, AccountRegisterForm, AccountEditForm, AccountProfileEditForm
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import Account
from django.db import transaction


def login(request):
    title = 'вход'
    login_form = AccountLoginForm(data=request.POST or None)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    action = request.GET['action'] if 'action' in request.GET.keys() else ''
    quantity = request.GET['quantity'] if 'quantity' in request.GET.keys() else ''
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        next = request.POST['next'] if 'next' in request.POST.keys() else ''
        action = request.POST['action'] if 'action' in request.POST.keys() else ''
        quantity = request.POST['quantity'] if 'quantity' in request.POST.keys() else ''
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                if action:
                    return HttpResponseRedirect(action + '?next=' + next + '&quantity=' + quantity)
                else:
                    return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('mainapp:main'))

    content = {'title': title,
               'login_form': login_form,
               'next': next,
               'action': action,
               'quantity': quantity}
    return render(request, 'accounts/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def register(request):
    title = 'регистрация'
    if request.method == 'POST':
        register_form = AccountRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('accounts:login'))
            else:
                print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('accounts:login'))
    else:
        register_form = AccountRegisterForm()
    content = {'title': title, 'register_form': register_form}
    return render(request, 'accounts/register.html', content)


@transaction.atomic
def edit(request):
    title = 'редактирование'
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('mainapp:main'))
    if request.method == 'POST':
        edit_form = AccountEditForm(request.POST, request.FILES,
                                     instance=request.user)
        profile_form = AccountProfileEditForm(request.POST,
                                              instance=request.user.accountprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('accounts:edit'))
    else:
        edit_form = AccountEditForm(instance=request.user)
        profile_form = AccountProfileEditForm(
            instance=request.user.accountprofile
        )

    content = {'title': title,
               'edit_form': edit_form,
               'profile_form': profile_form}

    return render(request, 'accounts/edit.html', content)


def send_verify_mail(user):
    verify_link = reverse('accounts:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале \
    {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = Account.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'accounts/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'accounts/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('mainapp:main'))
