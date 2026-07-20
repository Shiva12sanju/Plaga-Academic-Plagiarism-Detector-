import os
import sys

# Add root folder to sys.path so we can import from app, models, etc.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, User, Document, Result

def seed_database():
    print("Seeding database...")
    with app.app_context():
        # Recreate tables
        db.create_all()
        
        # Check if user already exists
        admin = User.query.filter_by(email="admin@plagdetector.edu").first()
        if not admin:
            admin = User(name="Administrator", email="admin@plagdetector.edu")
            admin.password = "admin1234"
            db.session.add(admin)
            db.session.commit()
            print("Admin user created (admin@plagdetector.edu / admin1234)")
        else:
            print("Admin user already exists.")
            
        student = User.query.filter_by(email="student@plagdetector.edu").first()
        if not student:
            student = User(name="John Doe", email="student@plagdetector.edu")
            student.password = "student1234"
            db.session.add(student)
            db.session.commit()
            print("Student user created (student@plagdetector.edu / student1234)")
        else:
            print("Student user already exists.")
            
        # Add sample document
        sample_doc = Document.query.filter_by(filename="sample_academic_paper.txt").first()
        if not sample_doc:
            sample_text = """
            Abstract:
            Artificial Intelligence (AI) and Natural Language Processing (NLP) are rapidly transforming 
            academic plagiarism detection. Traditional systems relied on exact keyword matches, whereas 
            modern engines utilize semantic similarity and vector representation models like BERT to 
            compare texts conceptually.
            
            Introduction:
            The rise of digitized academic publications has elevated the importance of digital integrity tools. 
            By converting text chunks into dense vectors using neural networks, NLP systems can detect not only 
            verbatim copying but also heavy paraphrasing and conceptual theft. This paper demonstrates a 
            fully automated web application framework powered by Flask and sentence embeddings to perform 
            real-time plagiarism audits on thesis papers.
            """
            sample_doc = Document(
                user_id=student.id,
                filename="sample_academic_paper.txt",
                extracted_text=sample_text.strip()
            )
            db.session.add(sample_doc)
            db.session.commit()
            print("Sample document added.")
        else:
            print("Sample document already exists.")
            
    print("Database seeding completed successfully.")

if __name__ == '__main__':
    seed_database()
