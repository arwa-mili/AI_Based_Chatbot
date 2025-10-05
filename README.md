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
- [Docker Deployment](#docker-deployment)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- Modern React frontend with PrimeReact UI components & tailwind CSS
- Django REST Framework backend
- Multi-language support (i18next)
- State management with Zustand
- Responsive design with Tailwind CSS
- Docker support for easy deployment

## 🛠 Tech Stack

### Frontend
- **React** 18.2.0 - UI library
- **React Router** 6.20.0 - Navigation
- **PrimeReact** 10.9.7 - UI component library
- **Tailwind CSS** 3.3.6 - Styling
- **Axios** - HTTP client
- **i18next** - Internationalization
- **Zustand** - State management
- **React Hot Toast** - Notifications
- **jsPDF** - PDF generation

### Backend
- **Django** - Python web framework
- **PostgreSQL** - Database (Docker)
- **Python 3** - Programming language

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v14 or higher)
- **npm** or **yarn**
- **Python 3** (v3.8 or higher)
- **pip** - Python package manager
- **Docker** and **Docker Compose** (optional, for containerized deployment)

## 📁 Project Structure

```
.
├── front/                  # React frontend
│   ├── public/            # Static files
│   ├── src/               # Source files
│   ├── package.json       # Frontend dependencies
│   └── tailwind.config.js # Tailwind configuration
│
├── back/                  # Django backend
│   ├── manage.py          # Django management script
│   ├── requirements.txt   # Python dependencies
│   ├── Makefile          # Backend commands
│   ├── .env.docker       # Docker environment variables
│   └── venv/             # Python virtual environment
│
├── run.sh                # Setup and run script
└── README.md             # This file
```

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
- Start both services

### Manual Installation

#### Backend Setup

```bash
cd back

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed initial data
python manage.py seed_languages

# Create superuser (optional)
python manage.py createsuperuser
```

#### Frontend Setup

```bash
cd front

# Install dependencies
npm install

# Or with yarn
yarn install
```

## 💻 Usage

### Using the run.sh Script

```bash
# Setup only
./run.sh setup

# Run services (after setup)
./run.sh run

# Complete setup and run
./run.sh all

# Run with Docker
./run.sh docker

# Run backend only
./run.sh backend

# Run frontend only
./run.sh frontend

# Show help
./run.sh help
```

### Manual Usage

#### Start Backend
```bash
cd back
source venv/bin/activate
python manage.py runserver
```

Backend will be available at: `http://localhost:8000`

#### Start Frontend
```bash
cd front
npm start
```

Frontend will be available at: `http://localhost:3000`

### Stopping Services

Press `Ctrl+C` in the terminal where services are running. The run.sh script handles graceful shutdown automatically.

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

## 🐳 Docker Deployment

### Using Docker Compose

```bash
cd back
docker compose --env-file .env.docker up -d
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

### Backend Commands

```bash
# Run migrations
make migrate

# Create new migrations
make makemigrations

# Create superuser
make createsuperuser

# Install new packages
make install

# Update requirements.txt
make freeze
```

### Frontend Commands

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject configuration (irreversible)
npm run eject
```

## 🧪 Testing

### Backend Tests
```bash
cd back
source venv/bin/activate
python manage.py test
```

### Frontend Tests
```bash
cd front
npm test
```

## 📝 API Documentation

Once the backend is running, API documentation is available at:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

(Note: Update these URLs based on your actual API documentation setup)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- React team for the amazing framework
- Django team for the robust backend framework
- PrimeReact for the beautiful UI components
- All contributors who helped with this project

## 📞 Support

For support, email your-email@example.com or open an issue in the repository.

---

**Note**: Make sure to update the `.env.docker` file with your actual configuration before running the application.