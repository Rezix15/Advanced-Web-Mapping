from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from . import models
from django.contrib.gis.geos import Point
from django.http import JsonResponse

# Create your views here.
from .models import Hotel, Restaurant, Profile
from django.core.serializers import serialize


def update_location(request):
    try:
        print(request.POST.get('point', ''))
        user_profile = models.Profile.objects.get(user=request.user)
        if not user_profile:
            raise ValueError("Can't get User details")
        point = request.POST["point"].split(",")
        point = [float(part) for part in point]
        point = Point(point, srid=4326)
        print(point)
        user_profile.location = point
        user_profile.save()
        return JsonResponse({"message": f"Set location to {point.wkt}."}, status=200)
    except Exception as e:
        raise e


def get_location_data(request):
    hotels = serialize('geojson', Hotel.objects.all(), fields=('name', 'location', 'city', 'street', 'phone', 'website', 'wheelchair'))
    restaurants = serialize('geojson', Restaurant.objects.all(), fields=('name', 'location', 'cuisine', 'opening_hours', 'website', 'city', 'street', 'wheelchair'))
    data = {'hotels': hotels, 'restaurants': restaurants}
    return JsonResponse(data)


def search_name(request):
    search_term = request.GET.get('search_result', '').lower()

    searched_hotels = Hotel.objects.all().filter(name__icontains=search_term)
    searched_restaurants = Restaurant.objects.all().filter(name__icontains=search_term)

    hotels_geo = serialize('geojson', searched_hotels, fields=('name', 'location', 'city', 'street', 'phone', 'website', 'wheelchair'))
    restaurants_geo = serialize('geojson', searched_restaurants, fields=('name', 'location', 'cuisine', 'opening_hours', 'website', 'city', 'street', 'wheelchair'))

    data = {'hotels': hotels_geo, 'restaurants': restaurants_geo}
    return JsonResponse(data)


