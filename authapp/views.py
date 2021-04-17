import hashlib
import random

from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

from authapp.forms import UserLoginForm, EmployerRegisterForm, JobseekerRegisterForm, UserEditForm, \
    EmployerEditForm, JobseekerEditForm, UserJobseekerEditForm, SetPasswordForm
from authapp.models import Employer, Jobseeker, IndustryType
from recruitsite import settings


def send_verify_mail(user):
    if user.employer:
        verify_link = reverse('auth:verify', args=[user.email, user.employer.activation_key])
        title = f'Подтверждение почты {user.email}'
        message = f'Сообщение с сайта IT Recrut\nПросим вас в течении 24-х часов  с момента получения ' \
                  f'данного письма подтвердить адрес своей электронной почты\nПросим пройти по ссылке {settings.DOMAIN_NAME}{verify_link}'

        return send_mail(title, message, 'it.portal.gb@gmail.com', [user.email], fail_silently=False)
    else:
        print('user has no object employer')


def send_verify_mail_seeker(user):
    if user.jobseeker:
        verify_link = reverse('auth:seeker_verify', args=[user.email, user.jobseeker.activation_key])
        title = f'Подтверждение почты {user.email}'
        message = f'Сообщение с сайта IT Recrut\nПросим вас в течении 24-х часов  с момента получения ' \
                  f'данного письма подтвердить адрес своей электронной почты\nПросим пройти по ссылке {settings.DOMAIN_NAME}{verify_link}'

        return send_mail(title, message, 'it.portal.gb@gmail.com', [user.email], fail_silently=False)
    else:
        print('user has no object seeker')


def verify(request, email, activation_key):
    title = 'Подтверждение регистрации'
    user = User.objects.get(email=email)
    if user.employer.activation_key == activation_key and not \
            user.employer.is_activation_key_expired():
        user.is_active = True
        user.save()
        return render(request, 'authapp/verification.html', {'user': user, 'title': title})


def seeker_verify(request, email, activation_key):
    title = 'Подтверждение регистрации'
    user = User.objects.get(email=email)
    if user.jobseeker.activation_key == activation_key and not \
            user.jobseeker.is_activation_key_expired():
        user.is_active = True
        user.save()
        return render(request, 'authapp/verification.html', {'user': user, 'title': title})


def email_verify(request):
    title = 'подтверждение почты'
    context = {'title': title}
    return render(request, 'authapp/email_verify.html', context)


def login(request):
    """
    Функция аутентификации, проверят есть ли правло у пользователя зайти на портал.
    """
    title = 'вход'

    login_form = UserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect(reverse('admin:index'))
            else:
                return HttpResponseRedirect(reverse('main'))

    content = {
        'title': title,
        'login_form': login_form,
    }
    return render(request, 'authapp/login.html', context=content)


def logout(request):
    """
    Функция выхода из портала, использует стандартный метод Django.
    """
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register_employer(request):
    """
    Функция регистрации как работодатель. Использует :model:`authapp.Employer`.

    **Template:**
    :template: `authapp/register_employer.html`
    """
    title = 'Регистрация работодателя'

    if request.method == 'POST':
        register_form = EmployerRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            user.is_active = False
            user.save()
            employer = Employer.objects.create(user=user)
            employer.company_name = register_form.cleaned_data.get('company_name')
            employer.tax_number = register_form.cleaned_data.get('tax_number')
            employer.phone_number = register_form.cleaned_data.get('phone_number')
            employer.site = register_form.cleaned_data.get('site')
            industry_type_id = register_form.cleaned_data.get('industry_type')
            industry_type = IndustryType.objects.get(id=industry_type_id)
            employer.industry_type = industry_type
            employer.short_description = register_form.cleaned_data.get('short_description')
            employer.logo = register_form.cleaned_data.get('logo')
            employer.city = register_form.cleaned_data.get('city')
            employer.status = Employer.NEED_MODER
            salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
            employer.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
            employer.save()
            if send_verify_mail(user):
                return HttpResponseRedirect(reverse('auth:email_verify'))
            else:
                return HttpResponse('ошибка отправки сообщения о регистрации')

    else:
        register_form = EmployerRegisterForm()

    content = {
        'title': title,
        'register_form': register_form,
    }
    return render(request, 'authapp/register_employer.html', context=content)


def register_jobseeker(request):
    """
    Функция регистрации как соискателя. Использует :model:`authapp.Jobseeker`.

    **Template:**
    :template: `authapp/register_jobseeker.html`
    """
    title = 'Регистрация соискателя'

    if request.method == 'POST':
        register_form = JobseekerRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            user.is_active = False
            user.save()
            jobseeker = Jobseeker.objects.create(user=user)
            jobseeker.middle_name = register_form.cleaned_data.get('middle_name')
            jobseeker.gender = register_form.cleaned_data.get('gender')
            jobseeker.phone_number = register_form.cleaned_data.get('phone_number')
            jobseeker.birthday = register_form.cleaned_data.get('birthday')
            jobseeker.married_status = register_form.cleaned_data.get('married_status')
            jobseeker.about = register_form.cleaned_data.get('about')
            jobseeker.photo = register_form.cleaned_data.get('photo')
            jobseeker.city = register_form.cleaned_data.get('city')
            salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
            jobseeker.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
            jobseeker.save()
            if send_verify_mail_seeker(user):
                return HttpResponseRedirect(reverse('auth:email_verify'))

            else:
                return HttpResponse('ошибка отправки сообщения о регистрации')

    else:
        register_form = JobseekerRegisterForm()

    content = {
        'title': title,
        'register_form': register_form,
    }
    return render(request, 'authapp/register_jobseeker.html', context=content)


@login_required
def edit(request):
    """
    Редактирование данных работодателя. Использует модель из forms EmployerEditForm.

     **Template:**
    :template: `authapp/edit.html`
    """
    title = 'редактирование работодателя'
    sent = False
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, instance=request.user)
        employer_form = EmployerEditForm(request.POST, request.FILES,
                                         instance=request.user.employer)
        if edit_form.is_valid() and employer_form.is_valid():
            edit_form.save()
            employer_form.save()
            user.employer.status = user.employer.NEED_MODER
            user.employer.failed_moderation = ''
            user.employer.save()
            sent = True
    else:
        edit_form = UserEditForm(instance=request.user)
        employer_form = EmployerEditForm(instance=request.user.employer)

    content = {'title': title, 'edit_form': edit_form, 'employer_form': employer_form,
               'sent': sent}

    return render(request, 'authapp/edit.html', content)


@login_required
def employer_change_password(request):
    title = 'Смена пароля'
    sent = False
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        password_form = SetPasswordForm(request.POST)
        if password_form.is_valid():
            user.set_password(password_form.cleaned_data['new_password1'])
            user.save()
            update_session_auth_hash(request, user)
            sent = True
    else:
        password_form = SetPasswordForm()
    context = {'title': title, 'form': password_form, 'user': user, 'sent': sent}
    return render(request, 'authapp/employer_change_password.html', context)


class JobseekerUpdateView(UpdateView):
    """
    Редактирование данных соискателя. Использует модель из forms JobseekerEditForm.

    **Template:**
    :template: `authapp/edit_jobseeker.html`
    """
    model = Jobseeker
    template_name = 'authapp/edit_jobseeker.html'
    form_class = JobseekerEditForm

    def get_success_url(self):
        return reverse_lazy('jobseeker:cabinet', kwargs={'jobseeker_id': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование'
        context['sent'] = False
        if self.request.POST:
            context['user_form'] = UserJobseekerEditForm(self.request.POST, self.request.FILES,
                                                         instance=self.request.user)
        else:
            context['user_form'] = UserJobseekerEditForm(instance=self.request.user)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.user = self.request.user
        user_form = context['user_form']
        with transaction.atomic():
            self.object = form.save()
            if user_form.is_valid():
                user_form.instance = self.object.user
                user_form.save()
                self.object.status = Jobseeker.NEED_MODER
                self.object.failed_moderation = ''
                self.object.save()
                context['sent'] = True

        return super().form_valid(form)


class UpdatePasswordView(PasswordChangeView):
    """
    Обновление пароля

    *Template*
    :template: `authapp/edit_password.html`
    """

    form_class = PasswordChangeForm
    template_name = 'authapp/edit_password.html'

    def get_success_url(self):
        if getattr(self.request.user, 'employer', None):
            return reverse_lazy('employer:main', kwargs={'emp_id': self.request.user.id})
        else:
            return reverse_lazy('jobseeker:cabinet', kwargs={'jobseeker_id': self.request.user.id})
