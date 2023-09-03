from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),  # Path to the poll detail view
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),  # Path to the results view
    path('<int:question_id>/vote/', views.vote, name='vote'),  # Path to the vote view
]