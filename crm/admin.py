from django.contrib import admin
from .models import Lead, Customer, Contact, Interaction

# Register your models here.

admin.site.register(Lead)
admin.site.register(Customer)
admin.site.register(Contact)
admin.site.register(Interaction) 