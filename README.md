# Full Stack Application

A full-stack web application built with React (Frontend) and Django (Backend).

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Development](#development)


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

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v14 or higher)
- **npm** or **yarn**
- **Python 3** (v3.8 or higher)
- **pip** - Python package manager




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


## ⚙️ Configuration

### Backend Configuration

Create a `.env` file in the `back/config/settings` directory with the following variables:

```env
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
OPENROUTER_API_KEY='your_api_key' or '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'


```







## 📝 API Documentation

Once the backend is running, API documentation is available at:
- Swagger UI: `http://localhost:8000/api/schema/docs/`


