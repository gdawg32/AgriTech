from django.core.management.base import BaseCommand
from app.models import Crop, District, Sale, CropPrice, CropSalesReport
from random import randint, choice
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate Sale and CropSalesReport models with extensive sample data for maximum reporting'

    def handle(self, *args, **kwargs):
        # Sample data for crops and districts
        crops = Crop.objects.all()
        districts = District.objects.all()

        # Ensure we have crops and districts to work with
        if not crops.exists() or not districts.exists():
            self.stdout.write(self.style.ERROR('Crops or districts are missing. Please add them first.'))
            return

        # Generate extensive sample sales data
        for _ in range(1000):  # Generate 1000 sales records
            crop = choice(crops)
            district = choice(districts)
            quantity_sold = randint(1, 500)  # Random quantity between 1 and 500
            cost = CropPrice.objects.get(crop=crop, district=district).cost
            date = datetime.now() - timedelta(days=randint(0, 365))  # Random date within the last 365 days (1 year)

            Sale.objects.create(
                crop=crop,
                district=district,
                quantity_sold=quantity_sold,
                price_per_kg=cost,
                date=date
            )

        # Generate the sales report
        self.stdout.write(self.style.SUCCESS('Extensive sales data populated successfully!'))
        
        # Call the generate_report method to update CropSalesReport
        CropSalesReport.generate_report()
        self.stdout.write(self.style.SUCCESS('Comprehensive crop sales report generated successfully!'))
