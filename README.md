# Securing Citizen Data in E-Governance Platforms using Modern Information Security Techniques

This project is a practical e-Governance portal that secures citizen applications (birth certificate, income certificate, residence certificate, and public grievance) using modern information security techniques.

## Techniques Used

Security Techniques Used:
- AES Encryption
- RSA Algorithm (conceptual in this prototype)
- Authentication (Login + OTP support in backend)
- Digital Signature
- SSL/TLS Protocol (explained for deployment)
- Access Control Mechanism

## Realistic Government Scenario

The system is implemented as a service portal where citizens submit applications with:
- Aadhaar ID (dummy)
- Address
- Purpose/remarks
- Application status tracking

## Frontend

The frontend handles user interaction and display:
- Login page
- Citizen dashboard
- Application form
- Officer/admin panel
- Application detail page with encryption proof

Tech stack:
- HTML
- CSS
- JavaScript (minimal)

## Backend

The backend handles core processing and security:
- Login authentication and session management
- Role-based access control
- Application processing
- Data encryption and decryption
- Digital signature generation for approvals
- Audit logging

Tech stack:
- Python
- Flask
- SQLite

## Implementation Steps

- Step 1: User login implemented using Flask routes and sessions.
- Step 2: Password authentication implemented with bcrypt hashing.
- Step 3: Citizen application submission implemented with validation.
- Step 4: Payload encrypted using AES (Fernet) before storage.
- Step 5: Role-based access implemented for citizen, officer, and admin.
- Step 6: Admin/officer approval workflow implemented with digital signature.
- Step 7: Audit logs captured for login, submission, approval, and rejection.

## Architecture Diagram

User -> Login -> Authentication -> Encryption -> Database -> Admin -> Output

Detailed flow:
- Frontend (HTML/CSS)
- User Input (Login/Application Form)
- Backend (Flask)
- Processing (Authentication + Encryption)
- Database (SQLite)
- Response to Frontend

## Encryption Proof in Project

The application detail page demonstrates encryption clearly by showing:
- Original data
- Encrypted data
- Decrypted view

This is implemented in the UI and backed by encrypted payload storage in the database.

## Threat and Solution

| Threat | Solution |
| --- | --- |
| SQL Injection | Input validation + ORM |
| Data theft | AES encryption |
| Unauthorized access | Authentication + sessions + RBAC |

## Real-World Connection

This system is similar to real-world e-Governance portals used by government departments to securely manage citizen data, application workflows, and approval processes.

## Future Scope

- Blockchain for tamper-resistant record history
- AI-based threat detection and anomaly alerts
- Biometric authentication for stronger identity verification

## Demo Users

- citizen1 / citizen123
- officer1 / officer123
- admin1 / admin123

## MongoDB Atlas Storage Setup

This project now supports MongoDB Atlas as cloud storage sync for:
- `users`
- `applications`
- `audit_logs`

SQLite remains active for core app compatibility, and writes are mirrored to Atlas when configured.

1. Create a MongoDB Atlas cluster and database user.
2. Add your network IP in Atlas Network Access.
3. Copy your Atlas connection string.
4. Set environment variables before running the app:

```bash
export MONGODB_URI="mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority"
export MONGODB_DB_NAME="secure_governance"
```

5. Start the app:

```bash
python3 app.py
```

If `MONGODB_URI` is not set, the app runs normally using SQLite only.
