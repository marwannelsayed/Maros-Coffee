from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pizza, Size, Beverage
import json
import requests

def index(request):
    pizzas = Pizza.objects.all()
    sizes = Size.objects.all()
    beverages = Beverage.objects.all()
    context = {
        'pizzas': pizzas,
        'sizes': sizes,
        'beverages': beverages
    }
    return render(request, 'main/index.html', context)

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # Ollama API call
            response = requests.post('http://localhost:11434/api/generate', 
                json={
                    "model": "llama3.2",
                    "prompt": f"You are a helpful pizza restaurant assistant. User message: {user_message}",
                    "stream": False
                })
            
            if response.status_code == 200:
                bot_response = response.json().get('response', '')
                return JsonResponse({'response': bot_response})
            else:
                return JsonResponse({'response': 'Sorry, I encountered an error.'}, status=500)
                
        except Exception as e:
            return JsonResponse({'response': f'Error: {str(e)}'}, status=500)
    
    return JsonResponse({'response': 'Method not allowed'}, status=405)
