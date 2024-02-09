from django.urls import path

from . import views

app_name = "xss_app"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("search/", views.SearchResultsView.as_view(), name="search"),
    path("create/", views.BlogPostCreateView.as_view(), name="create"),
]