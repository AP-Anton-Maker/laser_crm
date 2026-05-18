from django.urls import path
from .bot_logic.webhook_handler import WebhookView
from django.http import HttpResponse
from crm.models import Order
from django.template.loader import render_to_string
from weasyprint import HTML

def job_ticket_view(request, pk):
    try:
        order = Order.objects.select_related('client', 'material').get(pk=pk)
    except Order.DoesNotExist:
        return HttpResponse("Заказ не найден", status=404)
    
    html_string = render_to_string('orders/job_ticket.html', {'order': order})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="ticket_{pk}.pdf"'
    
    HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(response)
    return response

urlpatterns = [
    path('bot/webhook/', WebhookView.as_view(), name='vk_webhook'),
    path('bot/ticket/<int:pk>/', job_ticket_view, name='order_ticket'),
]
