from django.contrib import admin
from django.urls import path
from home import views  # Import views from the home app


urlpatterns = [
    path("company", views.company, name='company'),
    path("company_post", views.company_post, name='company_details'),
    path("candidate/", views.candidate, name='candidate'),
    path("candidate/<int:id>/", views.candidate, name='candidate_link'),
    path("stop/", views.stop, name='stop'),
    path("play_button/<int:value>/", views.play_button, name='play_button'),

    # path("interview_candidates", views.interview_candidates, name='interview_candidates'),
    path('interview_page/', views.interview_page, name='interview_page'),
    path('score/', views.score, name='score'),
    # path('interview_page/', views.interview_page, name='interview_page'),
   
    path("", views.home, name='home'), 
]
