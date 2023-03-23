from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/search/", views.search, name="search"),
    path("wiki/new/", views.new, name="new"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("wiki/delete/<str:title>", views.delete, name="delete"),
    path("wiki/random_page/", views.random_page, name="random_page"),
]