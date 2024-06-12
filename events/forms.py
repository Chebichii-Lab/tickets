# TicketPlatform/Events/forms.py
from django import forms
from .models import Event, Ticket

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'price_vip', 'price_vvip', 'price_group', 'tickets_vip', 'tickets_vvip', 'tickets_group', 'image', 'location']

     # Optionally add custom widget attributes
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class PurchaseTicketForm(forms.Form):
    TICKET_CHOICES = [
        ('vip', 'VIP'),
        ('vvip', 'VVIP'),
        ('group', 'Group'),
    ]
    ticket_type = forms.ChoiceField(choices=TICKET_CHOICES)