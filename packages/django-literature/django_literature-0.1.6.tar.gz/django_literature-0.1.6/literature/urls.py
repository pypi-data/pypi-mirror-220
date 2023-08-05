from django.urls import path

from . import views

app_name = "literature"
urlpatterns = [
    path("submit-csl/", views.process_csl, name="process"),
    path("", views.LiteratureList.as_view(), name="list"),
    path("authors/", views.AuthorList.as_view(), name="author_list"),
    path("authors/<pk>/", views.AuthorDetail.as_view(), name="author_detail"),
    path("<pk>/", views.LiteratureDetail.as_view(), name="detail"),
]
