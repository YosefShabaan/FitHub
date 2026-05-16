# FitHub

Professional Gym Management System built with FastAPI, SQLAlchemy, and a static HTML/CSS/JS frontend.

## Features

- Public member portal with membership plan selection.
- One-step member signup that creates both a member and a subscription.
- Admin authentication with JWT.
- Admin dashboard for members, subscriptions, and summary stats.
- Member CRUD and subscription management APIs.
- Automated tests and GitHub Actions CI.

## Default Admin Login

The app seeds a default admin user automatically when it starts:

```text
Username: admin
Password: admin123
```

You can override these values in `.env`:

```env
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_PASSWORD=admin123
```

## Run Locally

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open:

- Member portal: `http://127.0.0.1:8000/frontend/pages/index.html`
- Admin login: `http://127.0.0.1:8000/frontend/pages/login.html`
- API docs: `http://127.0.0.1:8000/docs`

## Member Flow

1. Open the member portal.
2. Choose Monthly or Yearly.
3. Submit name, phone, email, and plan.
4. The backend creates a member and an active subscription.
5. Log in as admin and open the dashboard to see updated stats.

## Tests

```bash
pytest -q
```

## Main API Routes

| Method | Route | Description |
| --- | --- | --- |
| `POST` | `/portal/join` | Public member signup and subscription creation |
| `POST` | `/auth/login` | Admin login |
| `GET` | `/dashboard/stats` | Dashboard summary stats |
| `GET` | `/members/` | List members |
| `POST` | `/members/` | Create member as admin |
| `GET` | `/subscriptions/` | List subscriptions |
| `POST` | `/subscriptions/` | Create subscription as admin |

## UML Use Case Diagram

```mermaid
flowchart LR
    Member[Member]
    Admin[Admin]

    Member --> Join[Join membership]
    Join --> SelectPlan[Select monthly or yearly plan]
    Join --> CreateProfile[Create member profile]
    Join --> CreateSubscription[Create active subscription]

    Admin --> Login[Log in]
    Admin --> ViewDashboard[View dashboard]
    Admin --> ManageMembers[Manage members]
    Admin --> ManageSubscriptions[Manage subscriptions]
```

## UML Class Diagram

```mermaid
classDiagram
    class User {
        int id
        string username
        string password
        string role
    }

    class Member {
        int id
        string name
        string phone
        string email
        datetime created_at
    }

    class Subscription {
        int id
        int member_id
        string plan
        date start_date
        date end_date
        string status
    }

    Member "1" --> "0..*" Subscription : has
```

## UML Sequence Diagram

```mermaid
sequenceDiagram
    participant M as Member Portal
    participant API as FastAPI Backend
    participant DB as Database
    participant A as Admin Dashboard

    M->>API: POST /portal/join
    API->>DB: Insert Member
    API->>DB: Insert Subscription
    API-->>M: Membership created
    A->>API: GET /dashboard/stats
    API->>DB: Count members and subscriptions
    API-->>A: Dashboard stats
```
