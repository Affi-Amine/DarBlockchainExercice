# 📚 Book Review & Management Service

This project is a **Django-based** Book Review & Management Service with **PostgreSQL** as the database and **Redis** for caching.  
It supports **JWT authentication**, **API documentation using Swagger**, and is containerized using **Docker & Docker Compose**.

---

## 🚀 Features

✅ **User Authentication** (JWT-based)  
✅ **Book Management** (CRUD operations)  
✅ **Review & Rating System**  
✅ **Caching with Redis**  
✅ **API Documentation** (Swagger & DRF Spectacular)  
✅ **Dockerized for Easy Deployment**  
✅ **PostgreSQL Database Support**  
✅ **Logging & Debugging Enabled**  

---

## 📦 Installation & Setup

### 1️⃣ Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python 3.10+](https://www.python.org/)
- [PostgreSQL 15+](https://www.postgresql.org/)

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/Affi-Amine/DarBlockchainExercice.git
cd book-review-service
```

---

### 3️⃣ Environment Variables (Plain Text)

Create a `.env` file in the root directory and define:
```bash
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=darblockchain
DATABASE_USER=admin
DATABASE_PASSWORD=admin
DATABASE_HOST=db
DATABASE_PORT=5432
SECRET_KEY="q@d&npxdld)(@3_x^9hv69g0jwvu(@yo^g=*50d#v2w9io6@=6"
LOCATION=“redis://127.0.0.1:6379/0”
```
---

### **4️⃣ Build & Run with Docker**  

#### Using Docker Compose:
```bash
docker-compose up --build
```
This will:
✅ Start the Django app
✅ Start PostgreSQL & Redis
✅ Apply database migrations
✅ Collect static files

To run in detached mode, use:
```bash
docker-compose up -d
```

---

### 5️⃣ Running Without Docker

#### Create & Activate Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
#### Install Dependencies:
```bash
pip install -r requirements.txt
```
#### Install Dependencies:
```bash
python manage.py migrate
python manage.py runserver
```

---

### 🛠 API Documentation
#### The API documentation is available at:
	•	Swagger UI: http://127.0.0.1:8000/swagger/
	•	Redoc: http://127.0.0.1:8000/redoc/

 ---

### 🗄 Database Migrations
#### Run migrations manually if needed:
```bash
docker-compose exec web python manage.py migrate
```

---

### 🐳 Docker Details
#### Docker Compose Services:
	•	web - Django application
	•	db - PostgreSQL database
	•	redis - Redis cache
#### Docker Volumes:
	•	postgres_data - Stores PostgreSQL data
	•	static_volume - Stores static files
#### To rebuild the containers:
```bash
docker-compose down
docker-compose up --build
```

---

### 🔑 Authentication
#### This project uses JWT authentication. Obtain a token by making a POST request to:
```bash
obtain this jwt token when logging in the endpoint /login
```

---

### 🌍 Deployment Notes
	•	Set DEBUG=False in production.
	•	Use a stronger SECRET_KEY.
	•	Set ALLOWED_HOSTS to your domain.
	•	Use Gunicorn for running the app.
