# Tajweed AI - Backend System

![Django](https://img.shields.io/badge/Django-5.2.5-brightgreen?logo=django)
![Docker](https://img.shields.io/badge/Docker-28.3.3-blue?logo=docker)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)

## 📋 Prerequisites

- **Docker** 28.0+ ([Install Guide](https://docs.docker.com/engine/install/))
- **Python** 3.10+ ([Download](https://www.python.org/downloads/))
- **Git** ([Install Guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git))

## 🛠️ Initial Setup

### 1. Clone Repository
```bash
git clone https://github.com/Nessryyne/Tajweed-AI-Backend.git tajweed-back
cd tajweed-back
```

### 2. Configure environment files
```bash
cp config/settings/.env.example .env
cp .env.docker.example .env.docker
```

### 3. Edit both files with your credentials
```bash
nano .env
nano .env.docker
```

### 4. Initialize Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 5. Launch services
```bash
make up && make migrate && make createsuperuser && make run
```

### 🧰 Available Make Commands
- `make up` – Start Docker containers  
- `make down` – Stop containers  
- `make migrate` – Run database migrations  
- `make createsuperuser` – Create Django superuser  
- `make run` – Run Django dev server  
- `make collectstatic` – Collect static files  
