# 🌐 WEB PAGE WORKING PROCESS

## **Secure E-Governance System (Flask Project)**

---

# 🔷 1. USER OPENS WEBSITE

**What happens:**

* User enters URL in browser
* Flask server receives request

👉 Example:

```
http://127.0.0.1:5000/
```

**Behind the scenes:**

* Browser → sends request
* Flask → returns `login.html`

---

# 🔷 2. LOGIN PAGE DISPLAYED

**Page:** `login.html`

**User enters:**

* Username
* Password

👉 This is your **Authentication UI**

---

# 🔷 3. LOGIN REQUEST SENT TO SERVER

**What happens:**

* User clicks "Login"
* Data sent to Flask backend

**Flow:**

```
Browser → Flask (POST request)
```

---

# 🔷 4. AUTHENTICATION PROCESS

**Server checks:**

* Username exists?
* Password correct?

👉 If using encryption:

* Password is hashed/verified (bcrypt)

**Result:**

* ✔ Valid → allow login
* ❌ Invalid → show error

---

# 🔷 4B. AUDIT LOGGING (SECURITY TRACKING) 📝

**What happens:**

* System records login success or failure
* Captures user IP address

👉 Ensures:

* Accountability
* Non-repudiation

---

# 🔷 5. ROLE-BASED REDIRECTION

After login:

* Citizen → Dashboard
* Officer → Approval Panel
* Admin → Admin Panel

👉 This is:
**Access Control (Module 2)**

---

# 🔷 6. USER DASHBOARD WORKING

**Page:** `dashboard.html`

User can:

* Apply for services
* Submit forms

**What happens:**

* User fills form
* Clicks submit

---

# 🔷 7. DATA PROCESSING + VALIDATION

**Server does:**

* Check input validity
* Prevent:

  * SQL Injection
  * XSS

👉 This is:
**Web Security (Module 6)**

---

# 🔷 8. ENCRYPTION PROCESS 🔐

Before storing data:

* Data is encrypted (AES)

**Example:**

```
Name: Ravi → Encrypted: xYz@#12
```

👉 This is:
**Module 3 (Encryption)**

---

# 🔷 9. DATABASE STORAGE

**What happens:**

* Encrypted data stored in:

  * MongoDB / SQLite

👉 Ensures:

* Confidentiality
* Data protection

---

# 🔷 10. ADMIN/OFFICER PANEL WORKING

**Page:** `admin.html`

Admin/Officer can:

* View requests
* Approve / Reject

---

# 🔷 11. DIGITAL SIGNATURE (SIMULATION)

When admin approves:

* System marks:
  **"Digitally Signed"**

👉 This ensures:

* Authenticity
* Non-repudiation

---

# 🔷 11B. AUDIT LOGGING (ADMIN ACTIONS) 📝

**What happens:**

* System logs the approval or rejection action
* Captures officer ID and timestamp

👉 Ensures:

* Transparent workflow tracking

---

# 🔷 12. RESPONSE TO USER

**What happens:**

* User sees:

  * Approved request
  * Download option

---

# 🔷 13. SECURE COMMUNICATION

* Data travels via HTTP (demo)
* Mention:

  * HTTPS (SSL/TLS)

👉 Ensures secure transmission

---

# 🧠 COMPLETE FLOW (SHORT)

```
User → Login Page → Authentication → Audit Log → Role Check → Dashboard  
→ Submit Data → Validation → Encryption → Database  
→ Admin/Officer Review → Digital Signature → Audit Log → Output
```
