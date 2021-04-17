from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


class IndustryType(models.Model):
    descx = models.CharField(verbose_name='Описание типа отрасли', max_length=64)

    class Meta:
        verbose_name_plural = 'Типы отраслей'

    def __str__(self):
        return self.descx


class Employer(models.Model):
    DRAFT = 'draft'
    NEED_MODER = 'need_moderation'
    MODER_OK = 'moderation_ok'
    MODER_REJECT = 'moderation_reject'
    EMPLOYER_STATUS_CHOICES = (
        (NEED_MODER, 'требуется модерация'),
        (MODER_OK, 'модерация пройдена успешно'),
        (MODER_REJECT, 'отклонено модератором'),
        (DRAFT, 'черновик')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(verbose_name='название компании', max_length=256, unique=True)
    tax_number = models.CharField(verbose_name='ИНН компании', max_length=16, blank=True)
    phone_number = models.CharField(verbose_name='телефон', max_length=11, blank=True)
    site = models.CharField(verbose_name='сайт компании', max_length=32, blank=True)
    industry_type = models.ForeignKey(IndustryType, on_delete=models.CASCADE, null=True, blank=True)
    short_description = models.TextField(verbose_name='краткое описание компании', blank=True)
    logo = models.ImageField(upload_to='company_logo', blank=True)
    city = models.CharField(verbose_name='город расположения компании', max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(verbose_name='статус компании на сайте',
                              choices=EMPLOYER_STATUS_CHOICES, default=NEED_MODER,
                              max_length=32)
    failed_moderation = models.CharField(max_length=512, blank=True, verbose_name='поле '
                        'заполняется в случае отклонения модерации')
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(datetime.now() + timedelta(hours=24)))

    def is_activation_key_expired(self):
        if datetime.now() > self.activation_key_expires:
            return True
        else:
            return False

    class Meta:
        verbose_name_plural = 'Работодатели'

    def __str__(self):
        return self.company_name


class Jobseeker(models.Model):
    NEED_MODER = 'need_moderation'
    MODER_OK = 'moderation_ok'
    MODER_REJECT = 'moderation_reject'
    JOBSEEKER_STATUS_CHOICES = (
        (NEED_MODER, 'требуется модерация'),
        (MODER_OK, 'модерация пройдена успешно'),
        (MODER_REJECT, 'отклонено модератором')
    )
    GENDER_CHOICES = (
        ('m', 'мужской'),
        ('f', 'женский'),
    )
    MARRIED_STATUS_CHOICES = (
        ('h', 'холост'),
        ('m', 'замужем/женат'),
        ('d', 'разведен/разведена'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    middle_name = models.CharField(verbose_name='отчество', max_length=32)
    gender = models.CharField(verbose_name='пол', max_length=16, choices=GENDER_CHOICES)
    birthday = models.DateField(verbose_name='дата рождения', null=True, blank=True)
    city = models.CharField(verbose_name='город', max_length=64)
    married_status = models.CharField(verbose_name='Статус в браке', max_length=1, choices=MARRIED_STATUS_CHOICES)
    photo = models.ImageField(upload_to='jobseeker_photo', blank=True)
    phone_number = models.CharField(verbose_name='телефон', max_length=11)
    about = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    status = models.CharField(verbose_name='статус соискателя на сайте',
                choices=JOBSEEKER_STATUS_CHOICES, default=NEED_MODER, max_length=32)
    failed_moderation = models.CharField(max_length=512, blank=True, verbose_name='поле '
                                            'заполняется в случае отклонения модерации')
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(datetime.now() + timedelta(hours=24)))

    def is_activation_key_expired(self):
        if datetime.now() > self.activation_key_expires:
            return True
        else:
            return False

    class Meta:
        verbose_name_plural = 'Соискатели'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} (статус: {self.status})'
