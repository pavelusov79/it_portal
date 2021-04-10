from django import forms

from jobseekerapp.models import Resume, ResumeEducation, ResumeExperience, Offer

DATE_INPUT_RESUME_FORMATS = [
    '%m.%Y',
    '%d.%m.%Y',
    '%Y-%m-%d',
    '%Y-%m',
]
RUB = 'руб'
EUR = 'EUR'
USD = 'USD'
CURRENCY_CHOICES = (
    (RUB, 'руб.'),
    (EUR, 'EUR'),
    (USD, 'USD')
)


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ('user', 'is_active', 'status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'] = forms.ChoiceField(label='Валюта', choices=CURRENCY_CHOICES)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in ('salary_min', 'salary_max', 'currency'):
                field.widget.attrs['style'] = 'width: 20%; display: inline;'

    def clean_salary_max(self):
        salary_max = self.cleaned_data['salary_max']
        salary_min = self.cleaned_data['salary_min']

        if not salary_min or not salary_max:
            return salary_max
        elif salary_min > salary_max:
            raise forms.ValidationError(f'Максимальный уровень зп меньше минимального')
        else:
            return salary_max


class ResumeEducationForm(forms.ModelForm):
    class Meta:
        model = ResumeEducation
        exclude = ('is_active', 'resume',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_date'] = forms.DateField(label='Дата начала', input_formats=DATE_INPUT_RESUME_FORMATS)
        self.fields['to_date'] = forms.DateField(label='Дата окончания', input_formats=DATE_INPUT_RESUME_FORMATS)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_to_date(self):
        to_date = self.cleaned_data['to_date']
        from_date = self.cleaned_data['from_date']
        if to_date and from_date:
            if to_date < from_date:
                raise forms.ValidationError(f'Дата окончания раньше даты начала.')
        return to_date


class ResumeExperienceForm(forms.ModelForm):
    class Meta:
        model = ResumeExperience
        exclude = ('is_active', 'resume',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_date'] = forms.DateField(label='Дата начала', input_formats=DATE_INPUT_RESUME_FORMATS)
        self.fields['to_date'] = forms.DateField(label='Дата окончания', input_formats=DATE_INPUT_RESUME_FORMATS)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_to_date(self):
        to_date = self.cleaned_data['to_date']
        from_date = self.cleaned_data['from_date']
        if to_date and from_date:
            if to_date < from_date:
                raise forms.ValidationError(f'Дата окончания раньше даты начала.')
        return to_date


class JobseekerOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('resume',
                  'cover_letter')

    def __init__(self, *args, **kwargs):
        jobseeker = kwargs.pop('jobseeker_id')
        super(JobseekerOfferForm, self).__init__(*args, **kwargs)
        self.fields['resume'].queryset = Resume.objects.filter(user=jobseeker, is_active=True)
        self.fields['resume'].empty_label = None
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
