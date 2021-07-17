from django.urls import path

from . import views

urlpatterns = [
    path('search/<str:genre>', views.search, name='search'),
    path('download/', views.download, name='download'),
    path('downloading/', views.downloading, name='downloading')
]