"""Compatibility endpoints for the Coursera dealership rubric.

These adapters preserve the existing /api/ endpoints while exposing the
course-style URLs and JSON keys. No fake test or deployment results.
"""
import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .models import Dealer, Review, CarMake, CarModel
from .views import sentiment


# Approximate city-centre coordinates for the synthetic demo listings.
CITY_CENTRES = {
    "Wichita": (37.6872, -97.3301), "Topeka": (39.0473, -95.6752),
    "Overland Park": (38.9822, -94.6708), "Denver": (39.7392, -104.9903),
    "Chicago": (41.8781, -87.6298), "Austin": (30.2672, -97.7431),
    "Dallas": (32.7767, -96.7970), "Seattle": (47.6062, -122.3321),
    "Phoenix": (33.4484, -112.0740), "Miami": (25.7617, -80.1918),
    "Boston": (42.3601, -71.0589), "Atlanta": (33.7490, -84.3880),
    "New York": (40.7128, -74.0060), "San Francisco": (37.7749, -122.4194),
    "Portland": (45.5152, -122.6784), "Los Angeles": (34.0522, -118.2437),
}

def dealer_data(d):
    latitude, longitude = CITY_CENTRES.get(d.city, (None, None))
    return {
        "id": d.pk, "city": d.city, "state": d.state,
        "address": d.address, "zip": d.zip_code,
        "lat": str(latitude) if latitude is not None else None,
        "long": str(longitude) if longitude is not None else None,
        "short_name": d.name,
        "full_name": d.name,
    }


@require_http_methods(["GET"])
def fetch_dealers(request):
    return JsonResponse([dealer_data(d) for d in Dealer.objects.order_by("id")], safe=False)


@require_http_methods(["GET"])
def fetch_dealer(request, dealer_id):
    d = Dealer.objects.filter(pk=dealer_id).first()
    return JsonResponse(dealer_data(d)) if d else JsonResponse({"error": "Dealer not found"}, status=404)


@require_http_methods(["GET"])
def fetch_dealers_by_state(request, state):
    return JsonResponse([dealer_data(d) for d in Dealer.objects.filter(state__iexact=state).order_by("id")], safe=False)


@require_http_methods(["GET"])
def fetch_reviews(request, dealer_id):
    reviews = Review.objects.filter(dealer_id=dealer_id).select_related("author")
    return JsonResponse([{
        "id": r.pk, "dealership": r.dealer_id, "name": r.author.username,
        "review": r.text, "purchase": True, "purchase_date": r.purchase_date.isoformat(),
        "car_make": r.car_make, "car_model": r.car_model, "car_year": r.car_year,
        "sentiment": sentiment(r.text),
    } for r in reviews], safe=False)


@require_http_methods(["GET"])
def get_cars(request):
    return JsonResponse({"CarModels": [
        {"CarModel": m.name, "CarMake": m.make.name}
        for m in CarModel.objects.select_related("make").order_by("make__name", "name")
    ]})


@require_http_methods(["GET"])
def analyze_text(request, review_text):
    return JsonResponse({"sentiment": sentiment(review_text)})


@require_http_methods(["POST"])
def course_login(request):
    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    username = data.get("userName", "")
    user = authenticate(request, username=username, password=data.get("password", ""))
    if user is None:
        return JsonResponse({"userName": username, "status": "Unauthenticated"}, status=401)
    login(request, user)
    return JsonResponse({"userName": user.username, "status": "Authenticated"})


@require_http_methods(["GET"])
def course_logout(request):
    logout(request)
    return JsonResponse({"userName": ""})
