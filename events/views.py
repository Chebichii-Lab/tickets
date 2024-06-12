# TicketPlatform/Events/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.forms import EventForm, PurchaseTicketForm
from .models import Event, Ticket

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})


@login_required
def purchase_ticket(request, event_id, ticket_type):
    event = get_object_or_404(Event, pk=event_id)
    person = request.user
    
    if ticket_type == 'vip':
        price = event.price_vip
        tickets_left = event.tickets_vip
    elif ticket_type == 'vvip':
        price = event.price_vvip
        tickets_left = event.tickets_vvip
    elif ticket_type == 'group':
        price = event.price_group
        tickets_left = event.tickets_group
    else:
        return redirect('event_detail', event_id=event_id)

    if tickets_left <= 0:
        # Handle sold out
        messages.error(request, 'This ticket type is sold out.')
        # return render(request, 'events/event_detail.html', {'event': event, 'error': 'This ticket type is sold out.'})
        return redirect('event_detail', event_id=event_id)
    
    if request.method == 'POST':
        form = PurchaseTicketForm(request.POST)
        if form.is_valid():
            if person.wallet_balance < price:
                # Handle insufficient funds
                messages.error(request, 'Insufficient funds. Please top up your wallet.')
                # return render(request, 'persons/top_up_wallet.html', {'error': 'Insufficient funds. Please top up your wallet.'})
                return redirect('top_up_wallet') # Redirect to top-up page
            
            # Deduct price from wallet and create a ticket
            person.wallet_balance -= price
            person.save()
            Ticket.objects.create(event=event, owner=person, ticket_type=ticket_type)
            
            # Reduce the number of available tickets
            if ticket_type == 'vip':
                event.tickets_vip -= 1
            elif ticket_type == 'vvip':
                event.tickets_vvip -= 1
            elif ticket_type == 'group':
                event.tickets_group -= 1
            event.save()
            messages.success(request, 'Ticket purchased successfully.')
            
            # return render(request, 'events/event_detail.html', {'event': event, 'success': 'Ticket purchased successfully.'})
            return redirect('event_detail', event_id=event_id)
    else:
        form = PurchaseTicketForm(initial={'ticket_type': ticket_type})
    
    return render(request, 'events/purchase_ticket.html', {'form': form, 'event': event, 'ticket_type': ticket_type})


