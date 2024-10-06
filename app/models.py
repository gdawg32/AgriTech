from django.db import models

class District(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    duration = models.CharField(max_length=100, help_text="Duration of the crop in days")
    harvest_time = models.CharField(max_length=100, help_text="Time of year when the crop is ready to harvest")
    weather = models.CharField(max_length=100, help_text="Weather conditions required for the crop")
    pest_issues = models.CharField(max_length=100, help_text="Pests that commonly affect the crop")
    description = models.TextField(help_text="Description of the crop")
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.CharField(max_length=50, choices=[
        ('Available', 'Available'),
        ('Limited', 'Limited'),
        ('Not Available', 'Not Available')
    ])

    def __str__(self):
        return self.name

class CropPrice(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.CharField(max_length=50, choices=[
        ('Available', 'Available'),
        ('Limited', 'Limited'),
        ('Not Available', 'Not Available')
    ])

    class Meta:
        unique_together = ('crop', 'district')  # Ensures unique prices for each crop in each district

    def __str__(self):
        return f"{self.crop.name} in {self.district.name}: {self.cost} - {self.availability_status}"


class Sale(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.crop.name} sold in {self.district.name} on {self.date}"


class CropSalesReport(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    total_sales = models.PositiveIntegerField(default=0)
    highest_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Report for {self.crop.name} in {self.district.name}"

    @classmethod
    def generate_report(cls):
        # This is where you would implement logic to calculate the highest selling crop
        # per district based on the sales recorded in the Sale model.
        from django.db.models import Sum, Max
        
        # Calculate total sales and highest price for each crop in each district
        results = (
            Sale.objects
            .values('district', 'crop')
            .annotate(total_sales=Sum('quantity_sold'), highest_price=Max('price_per_kg'))
        )
        
        # Clear existing reports
        cls.objects.all().delete()
        
        # Populate the CropSalesReport model
        for result in results:
            district_id = result['district']
            crop_id = result['crop']
            total_sales = result['total_sales']
            highest_price = result['highest_price']

            report, created = cls.objects.get_or_create(district_id=district_id, crop_id=crop_id)
            report.total_sales = total_sales
            report.highest_price = highest_price
            report.save()
