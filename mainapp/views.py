from itertools import chain

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.models import Employer
from employerapp.models import Vacancy, Favorites
from django.contrib.auth.decorators import login_required

from authapp.models import Employer
from employerapp.models import Vacancy
import jobseekerapp.models as jobseek_model
from mainapp.models import News


def main(request, page=None):
    title = 'Главная'
    if page is None:
        page = 1
        return HttpResponseRedirect(reverse('main', kwargs={'page': page}))
    news = News.objects.filter(is_active=True).order_by('-published')
    employers = Employer.objects.filter(is_active=True, status=Employer.MODER_OK).order_by('?')[:6]
    vacancies = Vacancy.objects.filter(action='moderation_ok')
    if vacancies:
        for vacancy in vacancies:
            is_favorite = jobseek_model.Favorite.objects.filter(user=request.user.id,
                                                                vacancy=vacancy.id).first()
            setattr(vacancy, "is_favorite", True if is_favorite else False)
    resume_all = jobseek_model.Resume.objects.all().filter(status='opened').order_by('updated_at')
    if resume_all and request.user.is_authenticated and getattr(request.user, 'employer', None):
        for resume in resume_all:
            is_favorite = Favorites.objects.filter(employer=request.user.employer,
                                                   resume=resume.id).first()
            setattr(resume, "is_favorite", True if is_favorite else False)
    paginator = Paginator(news, 4)
    try:
        news_paginator = paginator.page(page)
    except PageNotAnInteger:
        news_paginator = paginator.page(1)
    except EmptyPage:
        news_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'news': news_paginator,
        'employers': employers,
        'vacancies': vacancies,
        'resume_all': resume_all
    }
    return render(request, 'mainapp/index.html', context)


def news_detail(request, pk):
    one_news = News.objects.get(pk=pk)
    title = one_news.pk
    url = f'http://pavelusov79.pythonanywhere.com{request.path}'
    context = {
        'title': title,
        'one_news': one_news,
        'url': url
    }
    return render(request, 'mainapp/news_detail.html', context)


def search_news(request):
    title = 'Поиск новостей'
    search = request.GET.get('search')
    search_paginator = None
    if search:
        query = []
        results = News.objects.filter(Q(title__icontains=search) | Q(description__icontains=search),
                                      is_active=True).order_by(
            '-published')
        query.append(results)
        query = list(chain(*query))

        page = request.GET.get('page')
        paginator = Paginator(query, 3)
        try:
            search_paginator = paginator.page(page)
        except PageNotAnInteger:
            search_paginator = paginator.page(1)
        except EmptyPage:
            search_paginator = paginator.page(paginator.num_pages)

    context = {'title': title, 'search_news': search_paginator, 'search': search}

    return render(request, 'mainapp/search_news.html', context)


def news(request, page=1):
    title = 'Новости'
    news = News.objects.filter(is_active=True).order_by('-published')
    paginator = Paginator(news, 4)
    try:
        news_paginator = paginator.page(page)
    except PageNotAnInteger:
        news_paginator = paginator.page(1)
    except EmptyPage:
        news_paginator = paginator.page(paginator.num_pages)

    context = {'title': title, 'news': news_paginator}

    return render(request, 'mainapp/news.html', context)
