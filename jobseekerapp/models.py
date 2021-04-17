from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from authapp.models import Jobseeker


class Resume(models.Model):
    DRAFT = 'draft'
    OPENED = 'opened'
    NEED_MODER = 'need_moderation'
    MODER_REJECT = 'moderation_reject'
    RESUME_STATUS_CHOICES = (
        (DRAFT, 'черновик'),
        (OPENED, 'модерация пройдена успешно'),
        (NEED_MODER, 'требуется модерация'),
        (MODER_REJECT, 'модерация отклонена')
    )
    name = models.CharField(verbose_name='Желаемая должность', max_length=128)
    user = models.ForeignKey(Jobseeker, on_delete=models.CASCADE)
    salary_min = models.IntegerField(verbose_name='Минимальная зарплата', blank=True, null=True)
    salary_max = models.IntegerField(verbose_name='Максимальная зарплата', blank=True, null=True)
    currency = models.CharField(verbose_name='Валюта', max_length=3, blank=True, null=True)
    added_at = models.DateTimeField(verbose_name='Время добавления резюме', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Время обновления резюме', auto_now=True)
    key_skills = models.TextField(verbose_name='Ключевые навыки', blank=True, null=True)
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    status = models.CharField(verbose_name='Статус', choices=RESUME_STATUS_CHOICES,
                              max_length=32)
    failed_moderation = models.TextField(verbose_name='Сообщение в случае непрохождения '
                                                'модерации резюме', max_length=254, blank=True)
    is_active = models.BooleanField(verbose_name='Активный', default=True)

    class Meta:
        verbose_name_plural = verbose_name = 'Резюме'

    def __str__(self):
        return f'{self.name} {self.user.user.first_name} {self.user.user.last_name}'

    def save(self, *args, **kwargs):
        if self.status == 'opened' or self.status == 'moderation_reject':
            self.updated_at = datetime.now()
        super(Resume, self).save(*args, **kwargs)

    def get_experience_items(self):
        return self.experienceitems.select_related().filter(is_active=True)

    def get_education_items(self):
        return self.educationitems.select_related().filter(is_active=True)

    @staticmethod
    def get_user_resumes(user_id):
        return Resume.objects.filter(is_active=True, user_id=user_id)

    def get_favorite_id(self, user_id):
        favorite = self.favoriteresumes.select_related().filter(employer=user_id)
        if favorite:
            return favorite.first().id
        return None


class ResumeEducation(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, verbose_name='Резюме', related_name='educationitems')
    HIGH = 'high'
    ONLINE = 'online'
    EDU_TYPE_CHOICES = (
        ('high', 'высшее'),
        ('online', 'онлайн-курсы'),
    )
    edu_type = models.CharField(verbose_name='Тип образования', max_length=32, choices=EDU_TYPE_CHOICES, blank=False, default=HIGH)
    MASTER = 'master'
    BACHELOR = 'bachelor'
    SPECIALIST = 'specialist'
    SERTIFICATE = 'sertificate'
    DEGREE_CHOICES = (
        (MASTER, 'магистр'),
        (BACHELOR, 'бакалавр'),
        (SPECIALIST, 'специлист'),
        (SERTIFICATE, 'сертификат'),
    )
    degree = models.CharField(verbose_name='Уровень', max_length=64, null=True, choices=DEGREE_CHOICES, blank=False, default=MASTER)
    institution_name = models.CharField(verbose_name='Название учреждения', max_length=64)
    from_date = models.DateField(verbose_name='Начало периода', blank=True, null=True)
    to_date = models.DateField(verbose_name='Конец периода(фактическая или планируемая)')
    course_name = models.CharField(verbose_name='Название курса/кафедры', max_length=256)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активный', default=True)

    class Meta:
        verbose_name = 'Место обучения для резюме'
        verbose_name_plural = 'Места обучения для резюме'

    def __str__(self):
        return f'{self.resume.name} {self.resume.user.user.first_name} {self.resume.user.user.last_name} ' \
               f'({self.get_edu_type_display()}, {self.get_degree_display()})'


class ResumeExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experienceitems')
    company_name = models.CharField(verbose_name='Название компании', max_length=128)
    job_title = models.CharField(verbose_name='Название вакансии', max_length=128)
    from_date = models.DateField(verbose_name='Начало работы')
    to_date = models.DateField(verbose_name='Конец работы', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активный', default=True)

    class Meta:
        verbose_name = 'Место опыта для резюме'
        verbose_name_plural = 'Места опыта для резюме'

    def __str__(self):
        return f'{self.resume.name} {self.resume.user.user.first_name}' \
               f' {self.resume.user.user.last_name} {self.company_name} ' \
               f'{self.job_title}'


class Offer(models.Model):
    date = models.DateField(verbose_name='Дата направления отклика', auto_now_add=True)
    vacancy = models.ForeignKey('employerapp.Vacancy', on_delete=models.CASCADE, verbose_name='Вакансия')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, verbose_name='Резюме')
    cover_letter = models.TextField(verbose_name='Сопроводительное письмо',
                                    blank=True, max_length=524, help_text='поле не обязательное')
    contact_phone = models.CharField(max_length=12, blank=True, help_text='поле не обязательное',
                                     verbose_name='Контактный телефон')

    OUTGOING = 'O'
    INCOMING = 'I'
    DIRECTION_CHOICES = (
        (OUTGOING, 'исходящий'),
        (INCOMING, 'входящий'),
    )
    direction = models.CharField(verbose_name='Направление отклика (входящее/исходящее)', max_length=1,
                                 choices=DIRECTION_CHOICES)

    NEW = 'new'
    READ = 'read'
    APPROVE = 'approve'
    FAIL = 'fail'
    OFFER_STATUSES = (
        (NEW, 'новое (не прочитано)'),
        (READ, 'прочитано'),
        (APPROVE, 'приглашение получено'),
        (FAIL, 'отклонено')
    )
    status = models.CharField(verbose_name='Статус предложения', choices=OFFER_STATUSES, default=NEW, max_length=16)

    class Meta:
        verbose_name_plural = 'Предложения по вакансиям от соискателей'

    def __str__(self):
        return f'{self.vacancy.employer.company_name}/{self.vacancy.vacancy_name} ({self.resume.name})'


class Favorite(models.Model):
    user = models.ForeignKey(Jobseeker, on_delete=models.CASCADE)
    vacancy = models.ForeignKey('employerapp.Vacancy', on_delete=models.CASCADE, related_name='favoritevacancies',
                                verbose_name='Вакансия')
    add_date = models.DateField(verbose_name='Дата добавления в избранное', auto_now_add=True)

    class Meta:
        unique_together = ('user', 'vacancy',)
        verbose_name_plural = 'Избранные вакансии'
        verbose_name = 'Избранная вакансия'
