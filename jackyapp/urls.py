from django.urls import path
from . import views

#  How does one make it so that Django knows which app view to create
#  for a url when using the {% url %} template tag? --> Namespacing URL names
app_name = 'polls'
urlpatterns = [
    # ex: /jackyapp/
    path('', views.index, name='index'),

    # ex: /jackyapp/5/
    path('<int:question_id>/', views.detail, name='detail'),

    # ex: /jackyapp/5/results/
    path('<int:question_id>/results/', views.results, name='results'),

    # ex: /jackyapp/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote')
]