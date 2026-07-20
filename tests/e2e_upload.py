import sys
import os
from io import BytesIO

# Ensure project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app, db
from models import User, Document, Result, Report

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create a test student
    student = User(fullname='Test Student', email='student@example.com', password='studentpass', role='Student')
    db.session.add(student)
    db.session.commit()
    student_id = student.id

with app.test_client() as client:
    # Login
    res = client.post('/login', data={'email': 'student@example.com', 'password': 'studentpass'}, follow_redirects=True)
    print('Login status:', res.status_code, 'path:', getattr(res.request, 'path', None))

    # Prepare file
    data = {
        'file': (BytesIO(b"This is a test document.\n\nIt contains unique content."), 'testdoc.txt')
    }

    # Upload
    upload = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    print('Upload status:', upload.status_code)

    # Check created document
    with app.app_context():
        docs = Document.query.filter_by(user_id=student_id).all()
        print('Documents created:', len(docs))
        results = Result.query.filter_by(document1_id=docs[0].id).all() if docs else []
        print('Results created for document:', len(results))
        reports = Report.query.filter_by(user_id=student.id).all()
        print('Reports created:', len(reports))
        if reports:
            print('Report path exists:', os.path.exists(reports[0].report_path) if reports[0].report_path else 'no path')
