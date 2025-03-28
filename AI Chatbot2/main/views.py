from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.db.models import Sum
from .models import DrinkType, Customer, ChatMessage
import json
import os
from dotenv import load_dotenv
import tiktoken
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key='AIzaSyChlpXw1ueiMB4119F0ONzFlglFWB5w0hQ')
model = genai.GenerativeModel("gemini-2.0-flash")

def index(request):
    drinks = DrinkType.objects.all()
    context = {
        'drinks': drinks
    }
    return render(request, 'main/index.html', context)

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').lower()
            
            # Get or create customer using session
            customer = Customer.get_from_session(request.session)

            # Count tokens in user message
            encoding = tiktoken.get_encoding("cl100k_base")
            user_tokens = len(encoding.encode(user_message))
            
            # Save user message with token count
            ChatMessage.objects.create(
                customer=customer,
                content=user_message,
                is_bot=False,
                token_count=user_tokens
            )

            # Get chat history
            chat_history = ChatMessage.objects.filter(customer=customer).order_by('timestamp')
            conversation_history = '\n'.join([f"{'Bot' if msg.is_bot else 'Customer'}: {msg.content}" for msg in chat_history])

            # Get menu items from database
            drinks = list(DrinkType.objects.values('drink_type', 'price_small', 'price_medium', 'price_large', 'simple', 'double'))

            # Create context for the AI prompt
            menu_items = {
                'drinks': drinks
            }
            menu_context = menu_items

            menu_drinks = []
            for d in menu_items['drinks']:
                price_options = [
                    f"{size}: ${d[f'price_{size.lower()}']}" 
                    for size in ['Small', 'Medium', 'Large'] 
                    if f'price_{size.lower()}' in d and float(d[f'price_{size.lower()}']) > 0
                ]
                
                if not price_options:  # If no size prices, use simple/double prices
                    price_options.append(f"Simple: ${d.get('simple', 'N/A')}, Double: ${d.get('double', 'N/A')}")

                menu_drinks.append(f"{d['drink_type']} ({' - '.join(price_options)})")

            menu_text = ", ".join(menu_drinks)

            system_prompt = f"""
            You are Maro AI, a friendly cashier at Maro's Coffee. Here's our menu:

            Drinks:
            {menu_text}

            Previous conversation:
            {conversation_history}

            Guidelines for responses:
            1. Keep all responses short and direct
            2. Use simple, friendly language
            3. Only mention prices when asked
            4. For orders:
            - Confirm drink choice
            - For drinks with size options (small/medium/large prices > 0), ask for size preference
            - For drinks with simple/double options (both simple and double prices > 0), ask if they want simple or double
            - For delivery: get address
            5. Show final price only after order confirmation
            """

                        # Generate response using Gemini
            response = model.generate_content(
                contents=system_prompt + "\nCustomer: " + user_message,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 1024
                }
            )
            
            if response.text:
                bot_response = response.text
                # Count tokens in bot response
                bot_tokens = len(encoding.encode(bot_response))
                
                # Save bot response with token count
                chat_message = ChatMessage.objects.create(
                    customer=customer,
                    content=bot_response,
                    is_bot=True,
                    token_count=bot_tokens
                )
                
                # Calculate total tokens for this conversation
                total_tokens = ChatMessage.objects.filter(customer=customer).aggregate(total=models.Sum('token_count'))['total']
                
                return JsonResponse({
                    'response': bot_response,
                    'menu_items': menu_context,
                    'customer_id': customer.customer_id,
                    'message_tokens': bot_tokens,
                    'total_tokens': total_tokens
                })
            else:
                return JsonResponse({'response': 'Sorry, I encountered an error.'}, status=500)
                
        except Exception as e:
            return JsonResponse({'response': f'Error: {str(e)}'}, status=500)
    
    return JsonResponse({'response': 'Method not allowed'}, status=405)
