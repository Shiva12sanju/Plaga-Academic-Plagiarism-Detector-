from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


db = SQLAlchemy()



# ===================================================
# USER MODEL
# ===================================================

class User(UserMixin, db.Model):

    __tablename__ = "users"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    fullname = db.Column(
        db.String(100),
        nullable=False
    )


    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )


    password_hash = db.Column(
        db.String(255),
        nullable=False
    )


    role = db.Column(
        db.String(20),
        nullable=False,
        default="Student"
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



    # Password handling

    @property
    def password(self):
        raise AttributeError(
            "Password is not readable"
        )


    @password.setter
    def password(self, password):

        self.password_hash = generate_password_hash(
            password
        )


    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )



    # Relationships

    documents = db.relationship(
        "Document",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy=True
    )


    reports = db.relationship(
        "Report",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )


    activities = db.relationship(
        "ActivityLog",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )



    def __repr__(self):

        return f"<User {self.email}>"





# ===================================================
# DOCUMENT MODEL
# ===================================================

class Document(db.Model):

    __tablename__ = "documents"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    filename = db.Column(
        db.String(255),
        nullable=False
    )


    extracted_text = db.Column(
        db.Text,
        nullable=True
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    upload_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



    owner = db.relationship(
        "User",
        back_populates="documents"
    )



    results = db.relationship(
        "Result",
        foreign_keys="Result.document1_id",
        back_populates="document1",
        cascade="all, delete-orphan",
        lazy=True
    )



    matched_results = db.relationship(
        "Result",
        foreign_keys="Result.document2_id",
        back_populates="document2",
        lazy=True
    )



    embeddings = db.relationship(
        "Embedding",
        back_populates="document",
        cascade="all, delete-orphan",
        lazy=True
    )



    def __repr__(self):

        return f"<Document {self.filename}>"





# ===================================================
# EMBEDDING MODEL
# ===================================================

class Embedding(db.Model):

    __tablename__ = "embeddings"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    document_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "documents.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    embedding = db.Column(
        db.LargeBinary,
        nullable=False
    )



    document = db.relationship(
        "Document",
        back_populates="embeddings"
    )



    def __repr__(self):

        return f"<Embedding {self.id}>"





# ===================================================
# RESULT MODEL
# ===================================================

class Result(db.Model):

    __tablename__ = "results"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    document1_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "documents.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    document2_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "documents.id",
            ondelete="CASCADE"
        ),
        nullable=True
    )


    similarity_score = db.Column(
        db.Float,
        default=0
    )


    plagiarism_percentage = db.Column(
        db.Float,
        default=0
    )


    report_path = db.Column(
        db.String(255)
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



    document1 = db.relationship(
        "Document",
        foreign_keys=[document1_id],
        back_populates="results"
    )



    document2 = db.relationship(
        "Document",
        foreign_keys=[document2_id],
        back_populates="matched_results"
    )



    def __repr__(self):

        return f"<Result {self.id}>"





# ===================================================
# REPORT MODEL
# ===================================================

class Report(db.Model):

    __tablename__ = "reports"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    filename = db.Column(
        db.String(255),
        nullable=False
    )


    plagiarism_score = db.Column(
        db.Float,
        default=0
    )


    ai_score = db.Column(
        db.Float,
        default=0
    )


    similarity_score = db.Column(
        db.Float,
        default=0
    )


    matched_file = db.Column(
        db.String(255)
    )


    report_path = db.Column(
        db.String(255)
    )


    upload_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



    user = db.relationship(
        "User",
        back_populates="reports"
    )



    def __repr__(self):

        return f"<Report {self.filename}>"





# ===================================================
# ACTIVITY LOG MODEL
# ===================================================

class ActivityLog(db.Model):

    __tablename__ = "activity_logs"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=True
    )


    action = db.Column(
        db.String(255),
        nullable=False
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



    user = db.relationship(
        "User",
        back_populates="activities"
    )



    def __repr__(self):

        return f"<Activity {self.action}>"