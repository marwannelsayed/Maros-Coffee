# Maro's Pizza Project

This is a Django-based web application for Maro's Pizza, featuring an AI chatbot for taking orders. Which is the first AI chatbot I have ever built.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd AI Chatbot2
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install required packages:
```bash
pip install django requests
```

4. Set up the database:
```bash
python manage.py migrate
```

5. Install and start Ollama:
- Visit [Ollama's website](https://ollama.ai/) to download and install Ollama
- Pull the required model:
```bash
ollama pull llama3.2
```
- Start the Ollama server

6. Start the development server:
```bash
python manage.py runserver
```

7. Access the application:
- Open your web browser and navigate to `http://localhost:8000`
- For admin access, go to `http://localhost:8000/admin`

## Project Structure

- `main/` - Main application directory
  - `models.py` - Database models (Order, Customer, ChatMessage)
  - `views.py` - View functions and API endpoints
  - `templates/` - HTML templates
  - `urls.py` - URL configurations
  - `kegeldb_service.py` - Service for interacting with Kegeldb API

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   - Create a `.env` file in the project root
   - Add your Kegeldb API key:
     ```
     KEGELDB_API_KEY=your_kegeldb_api_key_here
     ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Start the development server:
   ```
   python manage.py runserver
   ```

## Kegeldb API Integration

The application uses the Kegeldb API to fetch menu data (pizzas, sizes, and beverages). The integration is handled by the `KegeldbService` class in `kegeldb_service.py`. The service includes caching to improve performance and reduce API calls.

### API Endpoints Used

- `/pizzas` - Get all available pizzas
- `/sizes` - Get all available pizza sizes
- `/beverages` - Get all available beverages

## Technologies Used

- Django
- Python
- JavaScript
- HTML/CSS
- Kegeldb API
- Ollama API (for AI chatbot)

## Features

- Interactive menu display
- AI-powered chatbot for taking orders
- Real-time chat interface
- Dynamic pricing based on pizza size
- Order management system
- Integration with Kegeldb API for menu data

## Note

Make sure the Ollama server is running before starting the application, as the chatbot relies on it for AI responses.