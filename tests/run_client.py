import sys
import os

# Ensure project root is on sys.path when running from the tests folder
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app, db, User

with app.app_context():
    db.drop_all()
    db.create_all()
    admin = User(fullname='System Admin', email='admin@example.com', password='admin123', role='Admin')
    db.session.add(admin)
    db.session.commit()

with app.test_client() as client:
    r = client.post('/login', data={'email':'admin@example.com','password':'admin123'}, follow_redirects=True)
    print('POST /login ->', r.status_code, 'path=', getattr(r.request, 'path', None))
    print('GET / ->', client.get('/').status_code)
    print('GET /faculty_dashboard ->', client.get('/faculty_dashboard').status_code)
    print('GET /upload ->', client.get('/upload').status_code)
    print('GET /student_dashboard ->', client.get('/student_dashboard').status_code)
