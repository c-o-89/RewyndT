from django.urls import path

from . import views

app_name = 'rewyndapp' #see https://docs.djangoproject.com/en/2.1/intro/tutorial03/
urlpatterns = [
    # /rewyndapp/
    path('', views.index, name='index'),

    # /rewyndapp/programs/
    path('programs/', views.programs_page, name='programs_page'),

    # /rewyndapp/programs/5
    path('programs/<int:program_id>/', views.program_listview, name='program_listview'),

    # /rewyndapp/episode/5
    path('episode/<int:id>/', views.episode_page, name='episode_page'),

    # /rewyndapp/about/
    path('about/', views.about_page, name='about_page'),

]
