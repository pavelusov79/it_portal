from datetime import date

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from authapp.models import Jobseeker, IndustryType, Employer


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Имя пользователя'
            elif field_name == 'password':
                field.widget.attrs['placeholder'] = 'Пароль'


class EmployerRegisterForm(UserCreationForm):
    industry_type_queryset = IndustryType.objects.all()
    INDUSTRY_TYPE_CHOICES = ()
    if industry_type_queryset:
        INDUSTRY_TYPE_CHOICES = tuple([(i.id, i.descx) for i in industry_type_queryset])
    username = forms.CharField(label='Логин')
    company_name = forms.CharField(label='Название компании')
    email = forms.EmailField(label='Контактный e-mail')
    tax_number = forms.CharField(label='ИНН компании', widget=forms.NumberInput(), max_length=16)
    phone_number = forms.CharField(label='Телефон компании', widget=forms.NumberInput(), max_length=11)
    site = forms.CharField(label='Сайт компании', required=False, help_text='поле необязательное')
    industry_type = forms.ChoiceField(label='Отрасль компании', choices=INDUSTRY_TYPE_CHOICES)
    short_description = forms.CharField(label='Краткое описание вашей компании', widget=forms.Textarea)
    logo = forms.ImageField(label='Ваш логотип', required=False, help_text='Необязательное поле')
    city = forms.CharField(label='Город расположения')
    password1 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password'}), label='Пароль')
    password2 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password'}), label='Подтвердите пароль')

    class Meta(UserCreationForm):
        model = User
        fields = ('username',
                  'company_name',
                  'email',
                  'tax_number',
                  'phone_number',
                  'site',
                  'industry_type',
                  'short_description',
                  'logo',
                  'city',
                  'password1',
                  'password2',
                  )

    def __init__(self, *args, **kwargs):
        super(EmployerRegisterForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            email_db = User.objects.filter(email=data)
        except User.DoesNotExist:
            email_db = None

        if email_db:
            raise forms.ValidationError(f'Пользователь с такой электронной почтой уже зарегистрирован')
        return data


class JobseekerRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    first_name = forms.CharField(label='Имя')
    middle_name = forms.CharField(label='Отчество')
    last_name = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='Контактный e-mail')
    gender = forms.ChoiceField(label='Пол', choices=Jobseeker.GENDER_CHOICES)
    birthday = forms.DateField(label='Дата рождения', input_formats=['%d-%m-%Y', '%d.%m.%Y'])
    city = forms.CharField(label='Город', max_length=64)
    married_status = forms.ChoiceField(label='Статус в браке', choices=Jobseeker.MARRIED_STATUS_CHOICES)
    photo = forms.ImageField(label='Фото', required=False, help_text='Необязательное поле')
    phone_number = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'data-mask': '0(000)000-00-00'}))
    about = forms.CharField(label='О себе', widget=forms.Textarea, max_length=512)
    password1 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password'}), label='Пароль')
    password2 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password'}), label='Подтвердите пароль')

    class Meta(UserCreationForm):
        model = User
        fields = ('username',
                  'first_name',
                  'middle_name',
                  'last_name',
                  'email',
                  'gender',
                  'birthday',
                  'phone_number',
                  'photo',
                  'city',
                  'married_status',
                  'about',
                  'password1',
                  'password2',
                  )

    def __init__(self, *args, **kwargs):
        super(JobseekerRegisterForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_birthday(self):
        data = self.cleaned_data['birthday']
        cur_date = date.today()
        age = (cur_date - data).days // 365
        if age < 18:
            raise forms.ValidationError("Вы слишком молоды для регистрации в качестве соискателя")
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            email_db = User.objects.filter(email=data)
        except User.DoesNotExist:
            email_db = None

        if email_db:
            raise forms.ValidationError(f'Пользователь с такой электронной почтой уже зарегистрирован')
        return data

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        data = ''.join([i for i in data if i.isdigit()])
        return data


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')
        self.fields['username'] = forms.CharField(label='Логин')
        self.fields['email'] = forms.EmailField(label='Ваш email')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class EmployerEditForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('company_name', 'tax_number', 'phone_number', 'site', 'industry_type',
                  'short_description', 'logo', 'city')

    def __init__(self, *args, **kwargs):
        super(EmployerEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserJobseekerEditForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
        self.fields['username'] = forms.CharField(label='Логин')
        self.fields['email'] = forms.EmailField(label='Ваш email')
        self.fields['first_name'] = forms.CharField(label='Имя')
        self.fields['last_name'] = forms.CharField(label='Фамилия')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            email_db = User.objects.filter(email=data)
        except User.DoesNotExist:
            email_db = None
        try:
            email_changed_data = self.changed_data.index('email')
        except ValueError:
            email_changed_data = None
        if email_db and email_changed_data is not None:
            raise forms.ValidationError(f'Пользователь с такой электронной почтой уже зарегистрирован')
        return data


class JobseekerEditForm(forms.ModelForm):
    phone_number = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'data-mask': '0(000)000-00-00'}))

    class Meta:
        model = Jobseeker
        fields = ('middle_name',
                  'gender',
                  'birthday',
                  'city',
                  'married_status',
                  'photo',
                  'phone_number',
                  'about',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        data = ''.join([i for i in data if i.isdigit()])
        return data

    def clean_birthday(self):
        data = self.cleaned_data['birthday']
        cur_date = date.today()
        age = (cur_date - data).days // 365
        if age < 18:
            raise forms.ValidationError("Вы слишком молоды для регистрации в качестве соискателя")
        return data


class SetPasswordForm(forms.Form):

    new_password1 = forms.CharField(label='Введите новый пароль', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')

        return password2

