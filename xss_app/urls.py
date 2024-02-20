from django.urls import path

from . import views

app_name = "xss_app"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("search/", views.SearchResultsView.as_view(), name="search"),
    path("create/", views.BlogPostCreateView.as_view(), name="create"),
    path("resetAll/", views.ResetAllPostsView.as_view(), name="resetAll"),
    path("resetEx1/", views.ResetExercise1View.as_view(), name="resetEx1"),
    path("resetEx2/", views.ResetExercise2View.as_view(), name="resetEx2"),
    path("exercise2/", views.Exercise2View.as_view(), name="exercise2")
]