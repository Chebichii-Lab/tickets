# TicketPlatform/Events/admin.py
from django.contrib import admin
from .models import Event, Ticket

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'price_vip', 'price_vvip', 'price_group', 'tickets_vip', 'tickets_vvip', 'tickets_group', 'organizer')
    search_fields = ('name', 'description', 'organizer__username')

admin.site.register(Event, EventAdmin)
admin.site.register(Ticket)
