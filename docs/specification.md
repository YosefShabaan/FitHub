# FitHub - System Specification

## 1. System Overview
FitHub is a professional Gym Management System inspired by Mindbody, Glofox, and Zen Planner. It provides a complete solution for managing gym members, subscriptions, and analytics.

## 2. Requirements

### Functional Requirements
- User authentication with JWT
- Role-based access (admin/staff)
- Member CRUD operations
- Subscription management
- Auto-expire subscription logic
- Dashboard analytics

### Non-Functional Requirements
- Secure password hashing (bcrypt)
- RESTful API design
- Scalable database structure

## 3. Database Design

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT PK | Auto increment |
| username | VARCHAR(50) | Unique |
| password | VARCHAR(255) | Hashed |
| role | VARCHAR(20) | admin/staff |

### Members Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT PK | Auto increment |
| name | VARCHAR(100) | Full name |
| phone | VARCHAR(20) | Unique |
| email | VARCHAR(100) | Optional |
| created_at | DATETIME | Auto |

### Subscriptions Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT PK | Auto increment |
| member_id | INT FK | References members |
| plan | VARCHAR(20) | monthly/yearly |
| start_date | DATE | Start date |
| end_date | DATE | Auto calculated |
| status | VARCHAR(20) | active/expired |

## 4. Architecture
- **Backend:** FastAPI + SQLAlchemy ORM
- **Database:** MySQL (Production), SQLite (Testing)
- **Auth:** JWT Tokens
- **Frontend:** HTML + Tailwind CSS
- **CI/CD:** GitHub Actions
- **Deployment:** Render/Railway

## 5. API Endpoints

### Auth
- POST /auth/register
- POST /auth/login
- GET /auth/me

### Members
- GET /members/
- GET /members/search
- GET /members/{id}
- POST /members/
- PUT /members/{id}
- DELETE /members/{id}

### Subscriptions
- GET /subscriptions/
- GET /subscriptions/member/{id}
- POST /subscriptions/
- PUT /subscriptions/{id}
- DELETE /subscriptions/{id}

### Dashboard
- GET /dashboard/stats
