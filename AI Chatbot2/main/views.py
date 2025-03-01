from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pizza, Size, Beverage, Customer, ChatMessage
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
            user_message = data.get('message', '').lower()
            customer_id = data.get('customer_id')

            # Get or create customer
            if customer_id:
                customer = Customer.objects.get(id=customer_id)
            else:
                customer = Customer.objects.create()

            # Save user message
            ChatMessage.objects.create(
                customer=customer,
                content=user_message,
                is_bot=False
            )

            # Get chat history
            chat_history = ChatMessage.objects.filter(customer=customer).order_by('timestamp')
            conversation_history = '\n'.join([f"{'Bot' if msg.is_bot else 'Customer'}: {msg.content}" for msg in chat_history])

            # Get menu items from database
            pizzas = list(Pizza.objects.values('name', 'description', 'base_price'))
            sizes = list(Size.objects.values('name', 'price_multiplier'))
            beverages = list(Beverage.objects.values('name', 'price'))

            # Create context for the AI prompt
            menu_context = {
                'pizzas': pizzas,
                'sizes': sizes,
                'beverages': beverages
            }

            # Ollama API call with enhanced prompt
            system_prompt = f"""
            You are a professional cashier at Maro's Pizza and your name is Maro AI. Here's our current menu:

            Pizzas:
            {', '.join([f"{p['name']} (${p['base_price']})" for p in pizzas])}

            Sizes:
            {', '.join([f"{s['name']} (x{s['price_multiplier']})" for s in sizes])}

            Beverages:
            {', '.join([f"{b['name']} (${b['price']})" for b in beverages])}

            Previous conversation:
            {conversation_history}

            Act as a helpful and professional cashier. If the customer asks about menu items but don't mention any prices except only if the customer asks,
            Calculate the pizza price by (base price of pizza * the price multiplier of it's size). Never tell the price of the size only!
            If a customer wants to order, first ask which pizza he wants, then ask which size he wants, then ask which beverage he wants (it is optional so he can proceed his order without it), then ask if this is his final order,
            after the customer confirms an order, ask him if he wants the food delivered or taken away, if he wants it delivered ask for the address,
            after that say that the food is being prepared and thank him for trying out Maro's pizza.
            Be polite and professional at all times.
            Never tell any prices except only when the customer asks about the prices or when he confirms an order and whether it's take away or delivered and after he confirms the address if delivered.
            Don't type the mathematic calculations, just say how much the pizza costs with it's size and then the beverage price and then the total.
            Don't tell the customer what to type. let him decide.
            """

            response = requests.post('http://localhost:11434/api/generate', 
                json={
                    "model": "llama3.2",
                    "prompt": f"{system_prompt}\nCustomer: {user_message}",
                    "stream": False
                })
            
            if response.status_code == 200:
                bot_response = response.json().get('response', '')
                # Save bot response
                ChatMessage.objects.create(
                    customer=customer,
                    content=bot_response,
                    is_bot=True
                )
                return JsonResponse({
                    'response': bot_response,
                    'menu_items': menu_context,
                    'customer_id': customer.id
                })
            else:
                return JsonResponse({'response': 'Sorry, I encountered an error.'}, status=500)
                
        except Exception as e:
            return JsonResponse({'response': f'Error: {str(e)}'}, status=500)
    
    return JsonResponse({'response': 'Method not allowed'}, status=405)
