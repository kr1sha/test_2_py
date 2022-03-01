from django.urls import path

from .views import IndexView, DetailView, ResultView, vote

app_name = 'test'

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('<int:pk>/', DetailView.as_view(), name='question_detail'),
    path('<int:pk>/results/', ResultView.as_view(), name='question_results'),
    path('<int:question_id>/vote/', vote, name='question_vote'),
]
