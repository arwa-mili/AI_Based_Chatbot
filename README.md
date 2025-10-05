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

Create a `.env.docker` file in the `back/` directory with the following variables:

```env
# Database
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Django
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Other configurations
```

### Frontend Configuration

Environment variables can be added to a `.env` file in the `front/` directory:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ENV=development
```


### View Docker Logs

```bash
cd back
docker compose logs -f
```

### Stop Docker Containers

```bash
cd back
docker compose down
```

## 🔧 Development





## 📝 API Documentation

Once the backend is running, API documentation is available at:
- Swagger UI: `http://localhost:8000/api/schema/docs/`



---

**Note**: Make sure to update the `.env.docker` file with your actual configuration before running the application.
