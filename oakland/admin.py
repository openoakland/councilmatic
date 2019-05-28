from django.contrib import admin
from councilmatic_core.models import Bill, Event, Person, Organization, Jurisdiction


admin.site.register(Event)
admin.site.register(Bill)
admin.site.register(Person)
admin.site.register(Organization)
admin.site.register(Jurisdiction)
#
