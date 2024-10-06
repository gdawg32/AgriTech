from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Crop, District, Sale, CropPrice, CropSalesReport
import requests

# Create your views here.
OPENWEATHER_API_KEY = '7baab5b3b4ede0ba9b4c4224bee06cd9'

def index(request):
    return render(request, 'index.html')

def crop_plan(request):
    return render(request, 'crop_plan.html')

def market(request):
    return render(request, 'market.html')

def weather(request):
    districts = District.objects.all()
    context = {
        'districts': districts
    }
    return render(request, 'weather.html', context)

def get_weather_data(request, district_name):
    # Call OpenWeather API
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={district_name}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(api_url)
    data = response.json()
    return JsonResponse(data)


def crop_list(request):
    crops = Crop.objects.values('id', 'name')  # Fetching crop id and name
    return JsonResponse(list(crops), safe=False)

def district_list(request):
    districts = District.objects.values('id', 'name')  # Fetching district id and name
    return JsonResponse(list(districts), safe=False)

def crop_details(request):
    crop_name = request.GET.get('crop')
    district_name = request.GET.get('district')

    if crop_name and district_name:
        try:
            # Fetch the crop
            crop = get_object_or_404(Crop, name=crop_name)
            # Fetch the district
            district = get_object_or_404(District, name=district_name)

            # Fetch the sale record for the specific crop and district
            # Fetch the crop price object
            crop_price = CropPrice.objects.filter(crop=crop, district=district).first()
            
            if crop_price:
                response_data = {
                    'availability_status': crop_price.crop.availability_status,
                    'cost': crop_price.cost, 
                }
            else:
                response_data = {
                    'availability_status': 'Not Available',
                    'cost': None
                }

            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Crop and district must be provided'}, status=400)


def sales_report(request):
    crop_name = request.GET.get('crop')
    district_name = request.GET.get('district')


    if not crop_name or not district_name:
        return JsonResponse({'error': 'Crop and district must be provided.'}, status=400)

    try:
        # Filter the report based on the crop and district
        report = CropSalesReport.objects.get(crop__name=crop_name, district__name=district_name)

        # Prepare the response data
        response_data = {
            'total_sales': report.total_sales,
            'highest_price': report.highest_price,
        }

        return JsonResponse(response_data)

    except CropSalesReport.DoesNotExist:
        return JsonResponse({'error': 'Sales report not found for the given crop and district.'}, status=404)


def crop_list_view(request):
    if request.method == 'GET':
        crops = Crop.objects.all()
        crop_data = []

        for crop in crops:
            crop_data.append({
                'name': crop.name,
                'duration': crop.duration,
                'harvest_time': crop.harvest_time,
                'weather': crop.weather,
                'pest_issues': crop.pest_issues,
                'description': crop.description,
                'cost': str(crop.cost),  # Convert Decimal to string for JSON compatibility
                'availability_status': crop.availability_status,
            })

        return JsonResponse(crop_data, safe=False)