from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createPage", views.createPage, name="createPage"),
    path("editPage/<str:title>", views.editPage, name="editPage"),
    path("wiki/<str:title>", views.entryPage, name="entryPage"),
    path("wiki/", views.randomPage, name="random")
]
