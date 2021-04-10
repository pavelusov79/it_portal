from urllib import request

from django import forms
from django.core.validators import RegexValidator

from django.shortcuts import get_object_or_404

from authapp.models import Employer
from employerapp.models import Vacancy, SendOffers


class VacancyCreationForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('vacancy_name', 'vacancy_type', 'city', 'min_salary', 'max_salary', 'currency',
                  'description', 'requirements', 'conditions', 'contact_person', 'contact_email',
                  'action')

    def __init__(self, *args, **kwargs):
        super(VacancyCreationForm, self).__init__(*args, **kwargs)
        blank_choice = (('', '----------'),)
        action_choice = (
            (Employer.DRAFT, 'сохранить черновик'),
            (Employer.NEED_MODER, 'опубликовать на портале')
        )
        self.fields['action'] = forms.ChoiceField(label='Выберите действие',
                                                  choices=blank_choice + action_choice)
        self.fields['min_salary'] = forms.CharField(validators=[RegexValidator(regex='^[1-9]{1}['
                                                                                     '0-9]{2,6}$',
        message='Для поля "минимальный уровень з/п" допускаются только цифры от 3-х до 7-ми '
        'цифр.')], label='Минимальный уровень з/п', help_text='Поле необязательно к заполнению')
        self.fields['max_salary'] = forms.CharField(validators=[RegexValidator(regex='^[1-9]{1}['
                                                                                     '0-9]{2,6}$',
        message='Для поля "максимальный уровень з/п" допускаются только цифры от 3-х до 7-ми '
        'цифр.')], label='Максимальный уровень з/п', help_text='Поле необязательно к заполнению')

    def clean_max_salary(self):
        min_salary = self.cleaned_data.get('min_salary')
        max_salary = self.cleaned_data.get('max_salary')

        if int(max_salary) < int(min_salary):
            raise forms.ValidationError('Максимальный уровень з/п должен быть больше или равен '
                                        'минимальному уровню')
        return max_salary


class VacancyEditForm(forms.ModelForm):
    class Meta:
        class DateInput(forms.DateInput):
            input_type = 'date'

        model = Vacancy
        fields = ('vacancy_name', 'vacancy_type', 'city', 'min_salary', 'max_salary', 'currency',
        'description', 'requirements', 'conditions', 'contact_person', 'contact_email')

    def __init__(self, *args, **kwargs):
        super(VacancyEditForm, self).__init__(*args, **kwargs)

    def clean_max_salary(self):
        min_salary = self.cleaned_data.get('min_salary')
        max_salary = self.cleaned_data.get('max_salary')

        if int(max_salary) < int(min_salary):
            raise forms.ValidationError('Максимальный уровень з/п должен быть больше или равен '
                                        'минимальному уровню')
        return max_salary


class SendOfferForm(forms.ModelForm):
    class Meta:
        model = SendOffers
        fields = ('vacancy', 'cover_letter', 'contact_phone')

    def __init__(self, *args, **kwargs):
        if 'employer' in kwargs and kwargs['employer'] is not None:
            employer = kwargs.pop('employer')
            qs = Vacancy.objects.filter(action=Employer.MODER_OK, hide=False,
                                        employer=employer)
        super(SendOfferForm, self).__init__(*args, **kwargs)
        # self.fields['vacancy'] = forms.ModelChoiceField(queryset=self.qs, to_field_name=None,
        # label='выберите вакансию по которой хотите направить предложение соискателю')
        self.fields['vacancy'].queryset = qs
        self.fields['contact_phone'] = forms.CharField(label='контактный тел.',
            validators=[RegexValidator(regex='^8[0-9]{10}$', message='Допускаются только цифры '
            'начиная с 8-ки, например 84952354422 или 89147900000. ')],
                            help_text='поле необязательно к заполнению', required=False)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

