from django.contrib import admin
from .models import *

admin.site.register(TUser)
admin.site.register(Waste)
admin.site.register(ProcesssingPlant)
admin.site.register(TransportVehicle)
admin.site.register(Landfill)

