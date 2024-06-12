# This will define event related details and tickets
from django.db import models
from persons.models import Person

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    price_vip = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_vvip = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_group = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tickets_vip = models.PositiveIntegerField(default=0)
    tickets_vvip = models.PositiveIntegerField(default=0)
    tickets_group = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    organizer = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='organized_events', null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    def is_sold_out(self, ticket_type):
        if ticket_type == 'vip':
            return self.tickets_vip <= 0
        elif ticket_type == 'vvip':
            return self.tickets_vvip <= 0
        elif ticket_type == 'group':
            return self.tickets_group <= 0
        return False

class Ticket(models.Model):
    TICKET_TYPE_CHOICES = [
        ('vip', 'VIP'),
        ('vvip', 'VVIP'),
        ('group', 'Group'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES, null=True, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_ticket_type_display()} ticket for {self.event.name} owned by {self.owner.username}"

