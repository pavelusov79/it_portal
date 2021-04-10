from django.urls import path, re_path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/employer/', authapp.register_employer, name='register_employer'),
    path('register/jobseeker/', authapp.register_jobseeker, name='register_jobseeker'),
    path('edit/', authapp.edit, name='edit'),
    path('jobseeker/<int:pk>/edit/', authapp.JobseekerUpdateView.as_view(), name='edit_jobseeker'),
    path('edit/password/', authapp.UpdatePasswordView.as_view(), name='edit_password'),
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.verify, name='verify'),
    re_path(r'^seeker_verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.seeker_verify, name='seeker_verify'),
    path('email_verify/', authapp.email_verify, name='email_verify'),
    path('edit/employer_password/', authapp.employer_change_password,
         name='employer_change_password')
]
