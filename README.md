#  Notification Service – Backend Assignment

A backend service to send notifications via **Email**, **SMS**, and **In-App**, built using **Django**, **PostgreSQL**, **RabbitMQ**, and **REST API**.

---

##  Features

*  REST API to send notifications
*  Support for Email, SMS, and In-App types
*  PostgreSQL database
*  RabbitMQ for async message processing
*  Retry mechanism for failed notifications (up to 3 times)
*  View user-specific notification history

---

##  Tech Stack

| Component     | Technology            |
| ------------- | --------------------- |
| Backend       | Django 4.x            |
| Queue         | RabbitMQ              |
| Database      | PostgreSQL            |
| Messaging     | Pika (Python)         |
| API Framework | Django REST Framework |
| Worker Script | Python                |

---

##  Project Structure

```
notification_service/
├── backend/               # Django project
├── notifications/         # App with models, views, etc.
├── worker.py              # Worker to process queue
├── manage.py
├── README.md
├── requirements.txt
```

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/notification_service.git
cd notification_service
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv env
env\Scripts\activate
```

```
Django>=4.2
djangorestframework
psycopg2-binary
pika
```

---

### 3. Setup PostgreSQL Database

* Create a database named `notification_db` using pgAdmin or psql
* Update `backend/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'notification_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}
```

---

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5. Start Django Server

```bash
python manage.py runserver
```

---

### 6. Start RabbitMQ (Using Docker)

```bash
docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

* Open RabbitMQ UI: [http://localhost:15672](http://localhost:15672)
  Login: `guest` / `guest`

---

### 7. Run the Worker Script

In a new terminal (with venv activated):

```bash
python worker.py
```

---

##  API Endpoints

###  Send Notification (tested using Postman)

```
POST /api/notifications
```

**Body:**

```json
{
  "user": 1,
  "type": "email",
  "content": "Hello from the notification service!"
}
```

---

###  Get User Notifications

```
GET /api/users/<user_id>/notifications
```

---

##  Assumptions

* Email/SMS sending is mocked (no external service integrated)
* Retry logic uses a basic counter inside the worker
* Queue processing is handled synchronously for simplicity

---
