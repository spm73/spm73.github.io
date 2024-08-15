from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path('new', views.new, name="new"),
    path('random', views.random_page, name="random_page"),
    path('search', views.search, name="search"),
    path('edit/<str:entry_name>', views.edit, name="edit"),
    path("<str:title>", views.entry, name="entry")
]
