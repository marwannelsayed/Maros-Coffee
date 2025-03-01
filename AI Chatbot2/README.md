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
  - `models.py` - Database models (Pizza, Size, Beverage, Order, etc.)
  - `views.py` - View functions and API endpoints
  - `templates/` - HTML templates
  - `urls.py` - URL configurations

## Features

- Interactive menu display
- AI-powered chatbot for taking orders
- Real-time chat interface
- Dynamic pricing based on pizza size
- Order management system

## Note

Make sure the Ollama server is running before starting the application, as the chatbot relies on it for AI responses.