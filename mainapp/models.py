from datetime import datetime

from django.db import models


class News(models.Model):

    title = models.CharField(verbose_name="заголовок", max_length=128)
    published = models.DateField(verbose_name="опубликовано", default=datetime.now)
    description = models.TextField(verbose_name="текст новости")
    is_active = models.BooleanField(verbose_name='новость активна', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Новости'
