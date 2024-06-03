# TicketPlatform/Events/forms.py
from django import forms
from .models import Event, Ticket

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'price_vip', 'price_vvip', 'price_group', 'tickets_vip', 'tickets_vvip', 'tickets_group', 'image']

class PurchaseTicketForm(forms.Form):
    TICKET_CHOICES = [
        ('vip', 'VIP'),
        ('vvip', 'VVIP'),
        ('group', 'Group'),
    ]
    ticket_type = forms.ChoiceField(choices=TICKET_CHOICES)