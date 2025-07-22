from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # url匹配是，会将匹配到的int赋值给question_id
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote")
]