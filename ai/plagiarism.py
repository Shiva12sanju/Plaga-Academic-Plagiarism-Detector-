import os
from models import db, Document, Embedding, Result
from ai.embeddings import generate_embedding, serialize_embedding, deserialize_embedding
from ai.similarity import cosine_similarity
from ai.report_generator import generate_pdf_report
from utils.helper import split_into_paragraphs

def get_or_create_embedding(document):
    """
    Checks if an embedding already exists in the database for the given document.
    If not, generates it and saves it.
    Returns the numpy array representation of the embedding.
    """
    existing_emb = Embedding.query.filter_by(document_id=document.id).first()
    if existing_emb:
        return deserialize_embedding(existing_emb.embedding)
        
    # Generate new embedding
    print(f"Generating embedding for document {document.id} ({document.filename})...")
    np_emb = generate_embedding(document.extracted_text)
    serialized = serialize_embedding(np_emb)
    
    new_emb = Embedding(document_id=document.id, embedding=serialized)
    db.session.add(new_emb)
    db.session.commit()
    
    return np_emb

def check_plagiarism_between_two(doc1, doc2):
    """
    Compares two documents and calculates plagiarism percentage and returns a Result object.
    """
    emb1 = get_or_create_embedding(doc1)
    emb2 = get_or_create_embedding(doc2)
    
    score = cosine_similarity(emb1, emb2)
    plag_percentage = round(score * 100, 2)
    if plag_percentage < 0:
        plag_percentage = 0.0
        
    result = Result(
        document1_id=doc1.id,
        document2_id=doc2.id,
        similarity_score=score,
        plagiarism_percentage=plag_percentage
    )
    db.session.add(result)
    db.session.commit()
    
    # Generate report path
    from flask import current_app
    report_filename = f"report_{result.id}_{doc1.id}_vs_{doc2.id}.pdf"
    report_path = os.path.join(current_app.config['REPORTS_FOLDER'], report_filename)
    
    # Analyze matching paragraphs
    matching_paragraphs = find_matching_paragraphs(doc1.extracted_text, doc2.extracted_text)
    
    # Generate report
    generate_pdf_report(report_path, doc1, doc2, plag_percentage, matching_paragraphs)
    
    result.report_path = report_path
    db.session.commit()
    
    return result

def check_plagiarism_against_db(new_doc):
    """
    Compares a new document against all other documents in the database.
    Finds the one with highest similarity, stores the result, and returns it.
    """
    other_docs = Document.query.filter(Document.id != new_doc.id).all()
    
    if not other_docs:
        # No other documents to compare against — still generate a basic report
        result = Result(
            document1_id=new_doc.id,
            document2_id=None,
            similarity_score=0.0,
            plagiarism_percentage=0.0
        )
        db.session.add(result)
        db.session.commit()

        # Ensure reports folder exists and generate a simple report
        from flask import current_app
        os.makedirs(current_app.config.get('REPORTS_FOLDER', 'reports'), exist_ok=True)
        report_filename = f"report_{result.id}_{new_doc.id}_vs_0.pdf"
        report_path = os.path.join(current_app.config.get('REPORTS_FOLDER', 'reports'), report_filename)

        # Generate a minimal report (report_generator will fallback to text if ReportLab missing)
        generate_pdf_report(report_path, new_doc, None, 0.0, [])

        result.report_path = report_path
        db.session.commit()
        return result
        
    emb_new = get_or_create_embedding(new_doc)
    
    best_match_doc = None
    max_score = -1.0
    
    for other_doc in other_docs:
        emb_other = get_or_create_embedding(other_doc)
        score = cosine_similarity(emb_new, emb_other)
        if score > max_score:
            max_score = score
            best_match_doc = other_doc
            
    # Calculate percentage
    plag_percentage = round(max_score * 100, 2)
    if plag_percentage < 0:
        plag_percentage = 0.0
        
    result = Result(
        document1_id=new_doc.id,
        document2_id=best_match_doc.id if best_match_doc else None,
        similarity_score=max_score,
        plagiarism_percentage=plag_percentage
    )
    db.session.add(result)
    db.session.commit()
    
    # Generate report path
    from flask import current_app
    report_filename = f"report_{result.id}_{new_doc.id}_vs_{best_match_doc.id if best_match_doc else 0}.pdf"
    report_path = os.path.join(current_app.config['REPORTS_FOLDER'], report_filename)
    
    # Analyze matching paragraphs
    matching_paragraphs = []
    if best_match_doc:
        matching_paragraphs = find_matching_paragraphs(new_doc.extracted_text, best_match_doc.extracted_text)
        
    # Generate report
    generate_pdf_report(report_path, new_doc, best_match_doc, plag_percentage, matching_paragraphs)
    
    result.report_path = report_path
    db.session.commit()
    
    return result

def find_matching_paragraphs(text1, text2, threshold=0.65):
    """
    Compares individual paragraphs in text1 to those in text2 using cosine similarity.
    Returns a list of dictionaries with matching paragraphs and their scores.
    """
    paras1 = split_into_paragraphs(text1)
    paras2 = split_into_paragraphs(text2)
    
    matches = []
    if not paras1 or not paras2:
        return matches
        
    # Standard sentence transformer or fallback encoding
    for p1 in paras1:
        emb1 = generate_embedding(p1)
        best_match_p2 = None
        best_score = 0.0
        
        for p2 in paras2:
            emb2 = generate_embedding(p2)
            score = cosine_similarity(emb1, emb2)
            if score > best_score:
                best_score = score
                best_match_p2 = p2
                
        if best_score >= threshold:
            matches.append({
                'source_paragraph': p1,
                'matching_paragraph': best_match_p2,
                'score': round(best_score * 100, 2)
            })
            
    return matches
