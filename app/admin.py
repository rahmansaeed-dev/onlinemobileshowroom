from django.contrib import admin
from .models import CustomUser, Mobile, MobileCompany, Cart

# Register your models here.

# custom user admin 
@admin.register(CustomUser)
class CustomUserModel(admin.ModelAdmin):
    list_display = ['first_name','last_name','email','date_joined','is_staff']

# mobile admin model 
@admin.register(Mobile)
class MobileModelAdmin(admin.ModelAdmin):
    list_display = ['company','name','description','mobile_ram','color','price','screen_size','image','image1','image2','image3']


# Mobile company model
@admin.register(MobileCompany)
class MobileCompanyModelAdmin(admin.ModelAdmin):
    list_display = ['name','description','company_image']

# cart model 
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['user','product','quantity']


