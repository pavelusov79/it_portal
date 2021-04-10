from django.urls import path

from employerapp import views

app_name = 'employerapp'

urlpatterns = [
    path('<int:emp_id>/', views.employer_cabinet, name='main_cabinet'),
    path('<int:emp_id>/drafts/', views.vacancy_draft, name='drafts'),
    path('<int:emp_id>/published/', views.vacancy_published, name='published'),
    path('<int:emp_id>/messages/', views.messages, name='messages'),
    path('<int:emp_id>/hide/', views.vacancy_hide, name='hide'),
    path('<int:emp_id>/responses/', views.responses, name='responses'),
    path('<int:emp_id>/my_offers/', views.my_offers, name="my_offers"),
    path('<int:emp_id>/vacancy_create/', views.vacancy_create, name='vacancy_create'),
    path('<int:emp_id>/vacancy_draft_edit/<int:pk>/', views.vacancy_edit_draft,
         name='vacancy_edit_draft'),
    path('<int:emp_id>/vacancy_edit/<int:pk>/', views.vacancy_edit, name='vacancy_edit'),
    path('<int:emp_id>/vacancy_delete/<int:pk>/', views.vacancy_delete, name='vacancy_delete'),
    path('<int:emp_id>/vacancy_view/<int:pk>/', views.vacancy_view, name='vacancy_view'),
    path('<int:emp_id>/send_offer/<int:pk>', views.send_offer, name='send_offer'),
    path('<int:emp_id>/favorites/', views.favorites, name='favorites'),
    path('<int:emp_id>/favorite/create/', views.add_favorite, name='create_favorite'),
    path('<int:emp_id>/favorite_<int:pk>/delete/', views.delete_favorite, name='delete_favorite'),
    path('<int:emp_id>/search_resume/', views.search_resume, name='search_resume')
]