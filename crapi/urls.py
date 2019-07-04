from django.urls import path
from . import views

app_name = "crapi"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    
    path('movies', views.movies, name="movies"),
    path('movies/<int:prime_id>/', views.movie, name="movie"),
    path('autocomplete', views.autocomplete, name="autocomplete"),

    path('scrap', views.scrap, name="scrap"),
]
