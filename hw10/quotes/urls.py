from django.urls import path
from . import views

app_name="quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("author/<str:author_fullname>", views.author, name="author"),
]
