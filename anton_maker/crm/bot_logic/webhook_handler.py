from django.views import View
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .handlers import process_message
from crm.models import Client

@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse('error', status=400)

        if data.get('secret') != settings.VK_SECRET_KEY:
            return HttpResponse('error', status=403)

        obj_type = data.get('type')
        
        if obj_type == 'confirmation':
            return HttpResponse(settings.VK_CONFIRMATION_CODE)
        
        if obj_type == 'message_new':
            message_data = data.get('object', {})
            message = message_data.get('message', {})
            user_id = message.get('from_id')
            text = message.get('text', '')
            attachments = message.get('attachments', [])
            
            client, created = Client.objects.get_or_create(
                vk_id=user_id,
                defaults={'full_name': message.get('peer_id', 'Unknown')}
            )
            
            if created and 'first_name' in message:
                first_name = message.get('first_name', '')
                last_name = message.get('last_name', '')
                client.full_name = f"{first_name} {last_name}".strip()
                client.save()
            
            process_message(client, text, attachments)
            
        return HttpResponse('ok')
