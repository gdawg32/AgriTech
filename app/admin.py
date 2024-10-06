from django.contrib import admin
from .models import District, Crop, Sale, CropSalesReport, CropPrice

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('crop', 'district', 'quantity_sold', 'price_per_kg', 'date')


@admin.register(CropSalesReport)
class CropSalesReportAdmin(admin.ModelAdmin):
    list_display = ('crop', 'district', 'total_sales', 'highest_price')


@admin.register(CropPrice)
class CropPriceAdmin(admin.ModelAdmin):
    list_display = ('crop', 'district', 'cost', 'availability_status')