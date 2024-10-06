from django.core.management.base import BaseCommand
from app.models import Crop, District, CropPrice

class Command(BaseCommand):
    help = 'Populate crops and their prices in different districts'

    def handle(self, *args, **kwargs):
        self.populate_crop_prices()

    def populate_crop_prices(self):
        # Define all crops along with a default price and availability status
        crops_data = [
            ('Wheat', 100, 'Available'),
            ('Paddy', 90, 'Available'),
            ('Onion', 70, 'Limited'),
            ('Corn', 80, 'Available'),
            ('Tomato', 60, 'Available'),
            ('Chilly', 120, 'Limited'),
            ('Potato', 50, 'Available'),
            ('Brinjal', 75, 'Available'),
            ('Ginger', 200, 'Available'),
            ('Carrot', 90, 'Limited'),
            ('Banana', 40, 'Available'),
            ('Coconut', 60, 'Limited'),
            ('Mango', 150, 'Available'),
            ('Cucumber', 55, 'Available'),
            ('Pumpkin', 45, 'Available'),
            ('Bitterguard', 65, 'Limited'),
            ('Pea', 85, 'Available'),
            ("Lady's Finger", 100, 'Available'),
        ]

        # List of districts to associate with each crop
        districts = [
            'Kasargod', 'Wayanad', 'Kannur', 'Kozhikode', 
            'Malappuram', 'Palakkad', 'Thrissur', 'Idukki', 
            'Ernakulam', 'Kottayam', 'Alappuzha', 'Pathanamthitta', 
            'Kollam', 'Trivandrum'
        ]

        # Loop through the crops data
        for crop_name, default_cost, default_status in crops_data:
            crop, created = Crop.objects.get_or_create(name=crop_name)

            # Loop through each district and create CropPrice instances
            for district_name in districts:
                district, created = District.objects.get_or_create(name=district_name)
                
                # You can modify the cost and availability_status based on the district if needed
                CropPrice.objects.get_or_create(
                    crop=crop,
                    district=district,
                    cost=default_cost,
                    availability_status=default_status
                )

        self.stdout.write(self.style.SUCCESS('Crop prices populated successfully!'))
