# FitHub - Test Cases

## 1. Authentication Tests

### TC-001: Register New User
- **Input:** username: "ahmed", password: "pass123"
- **Steps:** POST /auth/register
- **Expected:** 200 OK, "User created successfully"

### TC-002: Register Duplicate Username
- **Input:** Same username twice
- **Steps:** POST /auth/register x2
- **Expected:** 400 Bad Request

### TC-003: Login Success
- **Input:** Valid username & password
- **Steps:** POST /auth/login
- **Expected:** 200 OK, access_token returned

### TC-004: Login Wrong Password
- **Input:** Wrong password
- **Steps:** POST /auth/login
- **Expected:** 401 Unauthorized

---

## 2. Members Tests

### TC-005: Add Member
- **Input:** name, phone, email
- **Steps:** POST /members/
- **Expected:** 200 OK, member created with ID

### TC-006: Get All Members
- **Input:** Valid token
- **Steps:** GET /members/
- **Expected:** 200 OK, list of members

### TC-007: Search Member
- **Input:** query="Ahmed"
- **Steps:** GET /members/search?query=Ahmed
- **Expected:** 200 OK, filtered list

### TC-008: Update Member
- **Input:** member_id, new name
- **Steps:** PUT /members/{id}
- **Expected:** 200 OK, updated data

### TC-009: Delete Member
- **Input:** member_id
- **Steps:** DELETE /members/{id}
- **Expected:** 200 OK, deleted message

### TC-010: Get Non-existent Member
- **Input:** id=99999
- **Steps:** GET /members/99999
- **Expected:** 404 Not Found

---

## 3. Subscription Tests

### TC-011: Create Monthly Subscription
- **Input:** member_id, plan="monthly", start_date
- **Steps:** POST /subscriptions/
- **Expected:** 200 OK, end_date = start + 30 days

### TC-012: Create Yearly Subscription
- **Input:** member_id, plan="yearly", start_date
- **Steps:** POST /subscriptions/
- **Expected:** 200 OK, end_date = start + 365 days

### TC-013: Auto-Expire Logic
- **Input:** Subscription with past end_date
- **Steps:** GET /subscriptions/
- **Expected:** status = "expired"

---

## 4. Dashboard Tests

### TC-014: Dashboard Stats
- **Input:** Valid token
- **Steps:** GET /dashboard/stats
- **Expected:** total_members, active_subscriptions, expired_subscriptions
