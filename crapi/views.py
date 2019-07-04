#render for rendring template and response back it to user.
from django.shortcuts import render
from django.http import HttpResponse

#model for movies
from .models import Movies

#if not data found in database for particular id
from django.core.exceptions import ObjectDoesNotExist

#for json conversion of data
import json


# for regex match
import re

# import beautifulsoap and get for scraping the movies
from bs4 import BeautifulSoup
from requests import get


# Its homepage => "/"
def homepage(request):
    data = json.dumps({
        "status": 200,
        "error": "none",
        "message": "Welcome to crapi"
    })
    return HttpResponse(data, 'application/json')
    

#all movies page
def movies(request):
    try:
        movis = Movies.objects.all()
        if movis:
            results = []
            for movi in movis:
                results.append({
                    "prime_id": movi.prime_id,
                    "name": movi.name,
                    "casts": movi.casts,
                    "rating": movi.rating,
                })
            data = json.dumps(results,indent=4)
            return HttpResponse(data, 'application/json')
        else:
            return HttpResponse("Can't find any a movie data!")
    except ObjectDoesNotExist:
        return HttpResponse("Can't find any a movie data!")


# movie page view
def movie(request,prime_id):
    try:
        movi = Movies.objects.get(prime_id=prime_id)
        results = []
        results.append({
            "prime_id": movi.prime_id,
            "name": movi.name,
            "casts": movi.casts,
            "rating": movi.rating,
        })
        data = json.dumps(results,indent=4)
        return HttpResponse(data, 'application/json')
    except ObjectDoesNotExist:
        return HttpResponse("Can't find any data for id " + str(prime_id) + "!")


# autcomplete ajax method
def autocomplete(request):
    q = request.GET.get('prefix', '').capitalize()
    limit = int(request.GET.get('limit', 5))
    offset = int(request.GET.get('offset', 0))
    if q == "":
        return HttpResponse(json.dumps({
            "message": "prefix is empty",
            "status": 200,
            "error": False
        },indent=4), 'application/json')


    search_qs = Movies.objects.filter(name__startswith=q).order_by('-rating')[offset:offset+limit]
    results = []
    for movi in search_qs:
        results.append({
            "prime_id": movi.prime_id,
            "name": movi.name,
            "casts": movi.casts,
            "rating": movi.rating,
        })
    data = json.dumps(results,indent=4)
    return HttpResponse(data, 'application/json')
    



# scraping
def scrap(request):
    for page_no in range(0, 50):
        calculated = 0

        # check is client provided any page_no or not
        if(int(page_no) > 0):
            calculated = (50*int(page_no)) + 1

        # Here 1000 is limit you can increase
        if(Movies.objects.all().count() < 1000):
            url = "https://www.imdb.com/search/title/?release_date=2019&start="+ str(calculated) +"&ref_=adv_nxt"
            resp = get(url)

            html_soup = BeautifulSoup(resp.text, 'html.parser')
            type(html_soup)
            movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')

            # Lists to store the scraped data in
            names = []
            cast = []
            ratings = []
            
            # Extract data from individual movie container
            for container in movie_containers:
                # If the movie has Metascore, then extract:
                if container.find('div', class_ = 'ratings-metascore') is not None:
                    name = container.h3.a.text
                    names.append(name)

                    # The IMDB rating
                    imdb = float(container.strong.text)
                    ratings.append(imdb)

                    # The description
                    caster = container.find("div", class_='ratings-bar').find_next('p')
                    caster = caster.find_next("p")
                    cast_name = ""
                    for a in caster.findAll('a'):
                        cast_name = cast_name + str(a.text) + ","
                    cast.append(cast_name)
            
            for i in range(0,len(names)):
                Movies.objects.create(name = names[i], casts= cast[i], rating= ratings[i])
    return HttpResponse("Our Work is Done Now!")
