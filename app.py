"""
SECURING CITIZEN DATA IN E-GOVERNANCE PLATFORMS USING MODERN INFORMATION SECURITY TECHNIQUES
A Flask-based application demonstrating information security concepts

MODULES IMPLEMENTED:
✓ Module 1: Introduction to Information Security (CIA Triad)
✓ Module 2: Security Investigations (Access Control, Threats)
✓ Module 3: Encryption & Key Management (AES)
✓ Module 4: Digital Signature & Authentication
✓ Module 5: Email & IP Security (Theory)
✓ Module 6: Web Security (Input validation, HTTPS concepts)
"""

from app import create_app

if __name__ == '__main__':
    app = create_app()
    
    # Print startup information
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   SECURING CITIZEN DATA IN E-GOVERNANCE PLATFORMS        ║
    ║   Running on: http://127.0.0.1:5000                       ║
    ║                                                            ║
    ║   SETUP: Visit http://127.0.0.1:5000/setup                ║
    ║   LOGIN: http://127.0.0.1:5000/login                      ║
    ║                                                            ║
    ║   Sample Users:                                           ║
    ║   - citizen1 / citizen123 (role: citizen)                ║
    ║   - officer1 / officer123 (role: officer)                ║
    ║   - admin1 / admin123 (role: admin)                      ║
    ║                                                            ║
    ║   Scenario: Birth Certificate / Income Certificate       ║
    ║   / Public Grievance Portal                               ║
    ║                                                            ║
    ║   Press CTRL+C to stop the server                        ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
