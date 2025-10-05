# Full Stack Application

A full-stack web application built with React (Frontend) and Django (Backend).

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- - [Configuration](#configuration)
- [Installation](#installation)
-

## ✨ Features

- Modern React frontend with PrimeReact UI
- Django REST Framework backend
- Multi-language support (i18next)
- State management
- AI integration
- Responsive design with Tailwind CSS

## 🛠 Tech Stack

### Frontend
- **React** 18.2.0 - UI library
- **React Router** 6.20.0 - Navigation
- **PrimeReact** 10.9.7 - UI component library
- **Tailwind CSS** 3.3.6 - Styling
- **Axios** - HTTP client
- **i18next** - Internationalization

### Backend
- **Django** - Python web framework
- **PostgreSQL** - Database 
- **Python 3** - Programming language


## ⚙️ Configuration

### Backend Configuration

Create a `.env` file in the `back/config/settings` directory with the following variables:

```env

(You can change your DATABASES configuration in back/config/settings/dev.py )
# Database

SECRET_KEY=super-secret-key

DB_NAME=XXXXXXX
DB_USER=XXXXXXX 
DB_PASSWORD=XXXXXX
DB_HOST=XXXXXX
DB_PORT=XXXXXX

# Django
SECRET_KEY=super-secret-key

#For those you can use my keys to be able to test models 
EDEEPL_API_KEY='your_api_key' or 152a76e2-77c6-4d39-8080-7de0ef0376a8:fx'
GEMINI_API_KEY='your_api_key' or 'AIzaSyAU6oQbS23u_hXPLAqZIwzOpFlDvRikBEs'
OPENROUTER_API_KEY='your_api_key' or 'sk-or-v1-{404}a9824a8650b43b4dad7f8f22ed917dce6020c60db659619df03788f5437ea231' (remove {404} in the middle) or go to : https://openrouter.ai/models , click on your avatar and choose api_keys and create new one 



## 🚀 Installation

### Quick Start (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Make the run script executable:
```bash
chmod +x run.sh
```

3. Run the complete setup and start the application:
```bash
./run.sh all
```

This will automatically:
- Check for required dependencies
- Set up the backend (create venv, install packages, run migrations)
- Set up the frontend (install npm packages)


Frontend will be available at: `http://localhost:3000`



```


## 📝 API Documentation

Once the backend is running, API documentation is available at:
- Swagger UI: `http://localhost:8000/api/schema/docs/`


