# Loan Management System API

## Overview
The **Loan Management System API** is a Django-based RESTful API designed for managing loan applications with user authentication, role-based access control, and automatic interest calculations. The system allows users to apply for loans, view loan schedules, foreclose loans, and manage payments.

## Features
- User authentication (JWT-based) with OTP verification
- Role-based access control (Admin/User)
- Loan application and approval system
- Automatic interest and repayment schedule calculation
- Loan foreclosure with adjusted interest
- PostgreSQL as the primary database

## Technologies Used
- **Backend:** Django, Django REST Framework (DRF)
- **Authentication:** JWT, OTP (via Nodemailer)
- **Database:** PostgreSQL
- **Tools:** Postman for API testing

---

## Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python (3.10+ recommended)
- PostgreSQL
- Virtual Environment (venv)

### 1. Clone the Repository
```
git clone https://github.com/sreejith-0087/Loan-Management-System-API.git
cd Loan-Management-System-API
```

### 2. Create and Activate Virtual Environment
```
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root and add the following:
```
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://username:password@localhost:5432/loan_db
EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```

### 5. Apply Migrations
```
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser
```
python manage.py createsuperuser
```

### 7. Run the Development Server
```
python manage.py runserver
```
API will be available at `http://127.0.0.1:8000/api/`

---

## API Endpoints

### 1. Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register/` | Register a new user |
| POST | `/api/login/` | Login to get JWT token |
| POST | `/api/verify-otp/` | Verify OTP for email authentication |

### 2. Loan Management
| Method | Endpoint                     | Description |
|--------|------------------------------|-------------|
| POST | `/api/loans/`                | Apply for a loan |
| GET | `/api/loans/`                | List all loans (Admin only) |
| POST | `/api/loans/{id}/foreclose/` | Foreclose a loan |

---

## Testing with Postman
- Import the provided **Postman Collection** (`Loan_Management.postman_collection.json`).
- Set environment variables for authentication.
- Test API endpoints with different roles (Admin/User).


---


## Contact
- **Sreejith S** - [GitHub](https://github.com/sreejith-0087)
- For queries, reach out to: `sreejith.s.official9@gmail.com`

---