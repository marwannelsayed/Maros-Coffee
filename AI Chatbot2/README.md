# Maro's Coffee AI Chatbot
## Project Overview
Maro's Coffee AI Chatbot is a web application designed to simulate a friendly cashier experience for a coffee shop named Maro's Coffee. The chatbot uses AI to interact with customers, take orders, and provide information about the menu.

## Features
- Display a professional menu with drink types, sizes, and prices.
- AI-powered chat interface for customer interaction.
- Dynamic menu loading from a database.
- Session-based customer tracking.
- Token counting for chat messages to manage conversation context.
## Technologies Used
- Python 3
- Django Web Framework
- Djongo (MongoDB connector for Django)
- Google Gemini AI API for chatbot responses
- HTML, CSS, JavaScript for frontend
## Project Structure
```
AI Chatbot2/
├── main/                  # Main Django 
app
│   ├── models.py          # Database 
models (DrinkType, Customer, ChatMessage)
│   ├── views.py           # Views 
handling web requests and AI chat logic
│   ├── templates/main/    # HTML 
templates including index.html
│   ├── urls.py            # URL routing 
for the app
│   └── ...
├── simple_page/           # Django 
project settings and configuration
│   ├── settings.py        # Django 
settings
│   ├── urls.py            # Project URL 
routing
│   └── ...
├── manage.py              # Django 
management script
├── db.sqlite3             # SQLite 
database file
└── requirements.txt       # Python 
dependencies
```
## Setup Instructions
1. 1.
   Clone the repository.
2. 2.
   Create a virtual environment and activate it.
3. 3.
   Install dependencies using pip install -r requirements.txt .
4. 4.
   Set up environment variables, especially GEMINI_API_KEY for the Google Gemini AI API.
5. 5.
   Run database migrations with python manage.py migrate .
6. 6.
   Start the development server using python manage.py runserver .
## Usage
- Access the web app at http://127.0.0.1:8000/ .
- View the menu displayed with drink options and prices.
- Use the chat bubble to interact with Maro AI, the friendly cashier.
- The AI will assist with orders, ask for size preferences, and confirm orders.
## Models
- DrinkType : Stores drink names and prices for different sizes and types.
- Customer : Tracks customers via session keys.
- ChatMessage : Stores chat messages between customer and AI, including token counts.
## Notes
- The menu images are dynamically loaded from Unsplash based on drink names.
- The AI chat uses Google Gemini API to generate responses based on conversation history and menu context.
- The chat interface supports real-time messaging with token management.
## License
This project is open source and free to use.