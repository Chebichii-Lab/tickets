# TicketPlatform/Events/urls.py
from django.urls import path
from django.conf.urls.static import static
from ticket import settings
from .views import event_list, event_detail, add_event, purchase_ticket

urlpatterns = [
    path('', event_list, name='event_list'),
    path('<int:event_id>/', event_detail, name='event_detail'),
    path('add/', add_event, name='add_event'),
    path('<int:event_id>/purchase/<str:ticket_type>/', purchase_ticket, name='purchase_ticket'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)