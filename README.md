# ai-academic-plagiarism-detector
AI Academic Plagiarism Detector
# 🤖 AI Academic Plagiarism Detector

An **AI-powered Academic Plagiarism Detection System** built using **Python, Flask, Machine Learning, and Natural Language Processing (NLP)**. This application detects plagiarism by comparing uploaded academic documents using **semantic similarity**, **AI embeddings**, and **Cosine Similarity**, providing an accurate plagiarism score along with a detailed report.

---

# 📌 Project Overview

The **AI Academic Plagiarism Detector** helps educational institutions, universities, researchers, and students identify plagiarism in academic documents. Unlike traditional plagiarism checkers that rely only on keyword matching, this system uses **Artificial Intelligence** to detect **exact matches, paraphrased content, and semantic similarities**.

The system extracts text from uploaded documents, preprocesses the content using NLP, converts text into vector embeddings, compares documents using semantic similarity algorithms, and generates a plagiarism report.

---

# 🎯 Objectives

- Detect plagiarism in academic documents.
- Identify exact and paraphrased content.
- Generate plagiarism percentage.
- Produce downloadable plagiarism reports.
- Securely manage users and uploaded documents.
- Improve academic integrity using Artificial Intelligence.

---

# ✨ Features

- 🔐 User Registration & Login
- 📄 Upload PDF/DOCX/TXT Documents
- 🤖 AI-based Plagiarism Detection
- 🧠 Semantic Similarity Detection
- 📊 Plagiarism Percentage Calculation
- 📑 Highlight Matching Content
- 📥 Download PDF Report
- 👨‍💼 Admin Dashboard
- 📂 Document Management
- 📈 Analytics Dashboard
- 🔍 Fast Search
- 🔒 Secure Authentication

---

# 🚀 Technologies Used

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Jinja2 Templates

## Backend

- Python 3.x
- Flask
- Flask SQLAlchemy
- Flask Login
- Werkzeug

## Artificial Intelligence

- Sentence Transformers
- BERT
- Machine Learning
- Natural Language Processing (NLP)

## NLP Libraries

- spaCy
- NLTK

## Similarity Algorithms

- Cosine Similarity
- TF-IDF (Optional)
- Semantic Embeddings

## Database

- SQLite (Development)
- MySQL (Production)
- PostgreSQL (Optional)

## PDF Processing

- PyMuPDF
- pdfplumber
- PyPDF2

## Report Generation

- ReportLab

## Deployment

- Render
- Railway
- AWS EC2
- Docker (Optional)

---

# 🆕 Modern Technologies Used

This project incorporates several modern AI technologies:

- Artificial Intelligence (AI)
- Machine Learning (ML)
- Natural Language Processing (NLP)
- Sentence Transformers
- BERT Transformer Model
- Semantic Search
- Text Embeddings
- Cosine Similarity
- Vector Representation
- PDF Text Extraction
- Secure Authentication
- RESTful Architecture

---

# 🏗️ Project Architecture

```
                  User

                    │

                    ▼

          Login / Register

                    │

                    ▼

         Upload Academic Document

                    │

                    ▼

          Text Extraction Module

                    │

                    ▼

          NLP Preprocessing

                    │

                    ▼

     AI Embedding Generation

                    │

                    ▼

     Semantic Similarity Engine

                    │

                    ▼

    Plagiarism Score Calculation

                    │

                    ▼

     Generate PDF Report

                    │

                    ▼

       Save Results in Database

                    │

                    ▼

          Admin Dashboard
```

---

# 🔄 Workflow

### Step 1

User registers or logs into the application.

↓

### Step 2

Uploads an academic document.

↓

### Step 3

The uploaded file is stored securely.

↓

### Step 4

Text is extracted from the document.

↓

### Step 5

NLP preprocessing removes stop words, punctuation, and performs tokenization and lemmatization.

↓

### Step 6

The AI model converts the processed text into embeddings.

↓

### Step 7

Stored documents are converted into embeddings.

↓

### Step 8

Cosine Similarity compares embeddings.

↓

### Step 9

Plagiarism percentage is calculated.

↓

### Step 10

Matching paragraphs are identified.

↓

### Step 11

A detailed plagiarism report is generated.

↓

### Step 12

Results are stored in the database.

↓

### Step 13

Users and administrators can download reports.

---

# 📂 Project Structure

```
AI-Academic-Plagiarism-Detector/

│
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── README.md
│
├── instance/
│   └── plagiarism.db
│
├── uploads/
│   ├── pdfs/
│   └── documents/
│
├── reports/
│   └── plagiarism_reports/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── upload.html
│   ├── dashboard.html
│   ├── report.html
│   ├── admin.html
│   └── profile.html
│
├── static/
│   ├── css/
│   │     └── style.css
│   ├── js/
│   ├── images/
│   └── icons/
│
├── ai/
│   ├── preprocess.py
│   ├── embeddings.py
│   ├── similarity.py
│   ├── plagiarism.py
│   └── report_generator.py
│
├── utils/
│   ├── pdf_reader.py
│   ├── helper.py
│   └── validators.py
│
└── database/
    ├── schema.sql
    └── seed.py
```

---

# 🗄️ Database Design

## Users

| Field | Type |
|---------|------|
| id | Integer |
| name | String |
| email | String |
| password | String |

---

## Documents

| Field | Type |
|---------|------|
| id | Integer |
| user_id | Integer |
| filename | String |
| upload_date | Date |
| extracted_text | Text |

---

## Embeddings

| Field | Type |
|---------|------|
| id | Integer |
| document_id | Integer |
| embedding | BLOB |

---

## Results

| Field | Type |
|---------|------|
| id | Integer |
| document1 | Integer |
| document2 | Integer |
| similarity_score | Float |
| plagiarism_percentage | Float |
| report_path | String |

---

# 🔗 Database Workflow

```
User Upload

      │

      ▼

Extract Text

      │

      ▼

NLP Processing

      │

      ▼

Generate Embeddings

      │

      ▼

Store Document

      │

      ▼

Store Embeddings

      │

      ▼

Compare Existing Documents

      │

      ▼

Generate Score

      │

      ▼

Save Result

      │

      ▼

Generate Report
```

---

# 🧠 AI Detection Pipeline

```
Document

↓

Extract Text

↓

Clean Text

↓

Tokenization

↓

Stop-word Removal

↓

Lemmatization

↓

Sentence Embeddings

↓

Vector Generation

↓

Cosine Similarity

↓

Similarity Score

↓

Plagiarism Percentage

↓

Report Generation
```

---

# 📊 Future Enhancements

- AI-generated content detection
- OCR support for scanned PDFs
- Multilingual plagiarism detection
- Citation verification
- Real-time plagiarism detection
- Cloud storage integration
- FAISS Vector Database
- ChromaDB Integration
- Pinecone Vector Search
- Retrieval-Augmented Generation (RAG)
- Large Language Model (LLM) Integration
- Email notifications
- REST API support
- Docker deployment
- Kubernetes deployment

---

# 🔒 Security Features

- Password Hashing
- Secure Login
- Session Management
- Role-Based Access Control
- File Validation
- Secure File Upload
- SQL Injection Protection
- CSRF Protection

---

# 📈 Advantages

- AI-powered plagiarism detection
- Detects paraphrased content
- High semantic accuracy
- Fast processing
- Secure architecture
- User-friendly interface
- Detailed plagiarism reports
- Scalable for educational institutions

---

# 👨‍💻 Installation

```bash
git clone https://github.com/yourusername/AI-Academic-Plagiarism-Detector.git

cd AI-Academic-Plagiarism-Detector
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

# 📦 Requirements

```
Flask
Flask-SQLAlchemy
Flask-Login
Werkzeug
sentence-transformers
torch
transformers
scikit-learn
spaCy
nltk
PyMuPDF
pdfplumber
PyPDF2
reportlab
numpy
pandas
```

---

# 📚 Applications

- Universities
- Colleges
- Schools
- Research Organizations
- Academic Journals
- Online Learning Platforms
- Thesis Evaluation
- Assignment Verification

---

# 👨‍💻 Author

**Your Name**

Final Year Project

Artificial Intelligence | Machine Learning | NLP | Flask | Python

---

# ⭐ If you found this project useful, don't forget to Star ⭐ the repository.