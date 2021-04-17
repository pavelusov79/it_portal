from django.contrib.auth.decorators import login_required
from django.urls import path

from jobseekerapp import views

app_name = 'jobseekerapp'

urlpatterns = [
    path('<int:jobseeker_id>/', views.JobseekerDetailView.as_view(), name='cabinet'),
    path('<int:jobseeker_id>/resume/', views.create_resume, name='resume'),
    path('<int:seeker_id>/messages', views.messages, name='messages'),
    path('<int:jobseeker_id>/resume/<int:pk>/', login_required(views.ResumeDetailView.as_view()), name='resume_detail'),
    path('resume/<int:pk>/external/', views.ResumeExternalDetailView.as_view(), name='resume_external_detail'),
    path('<int:jobseeker_id>/resume/<int:pk>/edit/', views.resume_update, name='resume_update'),
    path('<int:jobseeker_id>/resume/<int:pk>/delete/', views.ResumeDeleteView.as_view(), name='resume_delete'),
    path('<int:jobseeker_id>/resume/<int:resume_id>/experience/', views.ResumeExperienceCreateView.as_view(),
         name='resume_experience'),
    path('<int:jobseeker_id>/resume/<int:resume_id>/experience/<int:pk>/edit/',
         views.ResumeExperienceUpdateView.as_view(), name='resume_experience_update'),
    path('<int:jobseeker_id>/resume/<int:resume_id>/experience/<int:pk>/delete/',
         views.ResumeExperienceDeleteView.as_view(), name='resume_experience_delete'),
    path('<int:jobseeker_id>/resume/<int:resume_id>/education/',
         views.ResumeEducationCreateView.as_view(), name='resume_education'),
    path('<int:jobseeker_id>/resume/<int:resume_id>/education/<int:pk>/edit/',
         views.ResumeEducationUpdateView.as_view(), name='resume_education_update'),
    path('<int:jobseeker_id>/resume/<int:resume_id>/education/<int:pk>/delete/',
         views.ResumeEducationDeleteView.as_view(), name='resume_education_delete'),
    path('<int:jobseeker_id>/offer/<int:vacancy_id>/create/', views.JobseekerOfferCreateView.as_view(),
         name='offer_create'),
    # path('<int:jobseeker_id>/offer/', views.JobseekerOfferListView.as_view(), name='offer_list'),
    path('<int:jobseeker_id>/offer/', views.offer_list, name='offer_list'),
    path('<int:jobseeker_id>/favorite/', views.JobseekerFavoriteListView.as_view(), name='favorite_list'),
    path('<int:jobseeker_id>/favorite/<int:pk>/delete/', views.JobseekerFavoriteDeleteView.as_view(),
         name='favorite_delete'),
    path('<int:jobseeker_id>/favorite/create/', views.add_favorite, name='favorite_create'),
    path('<int:jobseeker_id>/search_vacancy/',
         views.SearchVacancyListView.as_view(), name='search_vacancy'),
]