from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:contact_id>', views.show_contact, name='show_contact'),
    path('search', views.search, name='search'),
]
