from django.contrib import admin
from councilmatic_core.models import Bill, Event, Person

admin.site.register(Event)
admin.site.register(Bill)
admin.site.register(Person)


