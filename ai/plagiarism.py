import os
from difflib import SequenceMatcher

from models import db, Document, Embedding, Result

from ai.embeddings import (
    generate_embedding,
    serialize_embedding,
    deserialize_embedding
)

from ai.hybrid_detector import hybrid_ai_analysis

from ai.sentence_matcher import compare_sentences
from ai.similarity import cosine_similarity
from ai.report_generator import generate_pdf_report

from utils.helper import split_into_paragraphs

from ai.text_processing import (
    clean_text,
    split_sentences,
    extract_keywords
)


# =====================================================
# EMBEDDING HANDLER
# =====================================================

def get_or_create_embedding(document):

    existing = Embedding.query.filter_by(
        document_id=document.id
    ).first()

    if existing:
        return deserialize_embedding(existing.embedding)

    print(f"Generating embedding for {document.filename}")

    embedding = generate_embedding(
        document.extracted_text
    )

    db.session.add(
        Embedding(
            document_id=document.id,
            embedding=serialize_embedding(embedding)
        )
    )

    db.session.commit()

    return embedding


# =====================================================
# SENTENCE SIMILARITY
# =====================================================

def sentence_similarity(text1, text2):

    sentences1 = split_sentences(clean_text(text1))
    sentences2 = split_sentences(clean_text(text2))

    if not sentences1 or not sentences2:
        return 0

    matches = 0

    for s1 in sentences1:

        best = 0

        for s2 in sentences2:

            score = SequenceMatcher(
                None,
                s1,
                s2
            ).ratio()

            if score > best:
                best = score

        # Increased threshold
        if best >= 0.90:
            matches += 1

    return matches / len(sentences1)


# =====================================================
# KEYWORD SIMILARITY
# =====================================================

def keyword_similarity(text1, text2):

    keywords1 = set(extract_keywords(text1))
    keywords2 = set(extract_keywords(text2))

    if not keywords1 or not keywords2:
        return 0

    return len(
        keywords1 & keywords2
    ) / len(
        keywords1 | keywords2
    )


# =====================================================
# OVERALL SIMILARITY
# =====================================================

def overall_similarity(doc1, doc2):

    emb1 = get_or_create_embedding(doc1)
    emb2 = get_or_create_embedding(doc2)

    semantic = cosine_similarity(
        emb1,
        emb2
    )

    sentence = sentence_similarity(
        doc1.extracted_text,
        doc2.extracted_text
    )

    keyword = keyword_similarity(
        doc1.extracted_text,
        doc2.extracted_text
    )

    # ----------------------------
    # Paragraph Similarity
    # ----------------------------

    paragraphs1 = split_into_paragraphs(
        doc1.extracted_text
    )

    paragraphs2 = split_into_paragraphs(
        doc2.extracted_text
    )

    paragraph_score = 0

    if paragraphs1 and paragraphs2:

        total = 0

        for p1 in paragraphs1:

            emb_p1 = generate_embedding(p1)

            best = 0

            for p2 in paragraphs2:

                emb_p2 = generate_embedding(p2)

                score = cosine_similarity(
                    emb_p1,
                    emb_p2
                )

                if score > best:
                    best = score

            total += best

        paragraph_score = total / len(paragraphs1)

    # ----------------------------
    # Final Score
    # ----------------------------

    score = (

        semantic * 0.45 +

        sentence * 0.20 +

        keyword * 0.10 +

        paragraph_score * 0.25

    )

    return round(score, 4)
# =====================================================
# TWO DOCUMENT CHECK
# =====================================================

def check_plagiarism_between_two(doc1, doc2):

    score = overall_similarity(doc1, doc2)

    percentage = round(score * 100, 2)

    analysis = hybrid_ai_analysis(doc1.extracted_text)

    result = Result(
        document1_id=doc1.id,
        document2_id=doc2.id,
        similarity_score=score,
        plagiarism_percentage=percentage,

        ai_score=analysis["overall_score"],
        ai_confidence=analysis["confidence"],
        roberta_score=analysis["roberta"],
        perplexity_score=analysis["perplexity"],
        burstiness_score=analysis["burstiness"],
        stylometry_score=analysis["stylometry"],
        vocabulary_score=analysis["vocabulary"],
        repetition_score=analysis["repetition"],
        readability_score=analysis["readability"]
)

    db.session.add(result)
    db.session.commit()

    matching_paragraphs = find_matching_paragraphs(
        doc1.extracted_text,
        doc2.extracted_text
    )

    matching_sentences = compare_sentences(
        doc1.extracted_text,
        doc2.extracted_text
    )

    from flask import current_app

    os.makedirs(
        current_app.config["REPORTS_FOLDER"],
        exist_ok=True
    )

    report_path = os.path.join(
        current_app.config["REPORTS_FOLDER"],
        f"report_{result.id}.pdf"
    )

    generate_pdf_report(
        report_path,
        doc1,
        doc2,
        result,
        percentage,
        matching_paragraphs,
        matching_sentences
    )

    result.report_path = report_path

    db.session.commit()

    return result


# =====================================================
# DATABASE COMPARISON
# =====================================================

def check_plagiarism_against_db(new_doc):

    documents = Document.query.filter(
        Document.id != new_doc.id
    ).all()

    analysis = hybrid_ai_analysis(
    new_doc.extracted_text
)
    
    print("AI SCORE =", analysis["overall_score"])

    # -------------------------------------
    # FIRST DOCUMENT
    # -------------------------------------

    if not documents:

        result = Result(
            document1_id=new_doc.id,
            document2_id=None,
            similarity_score=0,
            plagiarism_percentage=0,

            ai_score=analysis["overall_score"],
            ai_confidence=analysis["confidence"],
            roberta_score=analysis["roberta"],
            perplexity_score=analysis["perplexity"],
            burstiness_score=analysis["burstiness"],
            stylometry_score=analysis["stylometry"],
            vocabulary_score=analysis["vocabulary"],
            repetition_score=analysis["repetition"],
            readability_score=analysis["readability"]
)

        db.session.add(result)
        db.session.commit()

        from flask import current_app

        os.makedirs(
            current_app.config["REPORTS_FOLDER"],
            exist_ok=True
        )

        report_path = os.path.join(
            current_app.config["REPORTS_FOLDER"],
            f"report_{result.id}.pdf"
        )

        generate_pdf_report(
            report_path,
            new_doc,
            None,
            0,
            [],
            []
        )

        result.report_path = report_path

        db.session.commit()

        return result

    # -------------------------------------
    # FIND BEST MATCH
    # -------------------------------------

    matches = []

    for doc in documents:

        score = overall_similarity(
            new_doc,
            doc
    )

        matches.append({
            "document": doc,
            "score": score
    })
    # -------------------------------------


# Sort highest first
        matches.sort(
            key=lambda x: x["score"],
            reverse=True
)


# Default values
        best_document = None
        highest_score = 0


        if matches:

            best_document = matches[0]["document"]

            highest_score = matches[0]["score"]


# Ignore tiny matches
        if highest_score < 0.15:

            highest_score = 0

            best_document = None
    
    if matches:

        best_document = matches[0]["document"]
        highest_score = matches[0]["score"]

    if highest_score < 0.15:
        highest_score = 0
        best_document = None

    # Ignore tiny matches

    if highest_score < 0.15:

        highest_score = 0

        best_document = None

    percentage = round(
        highest_score * 100,
        2
    )

    result = Result(

        document1_id=new_doc.id,

        document2_id=best_document.id if best_document else None,

        similarity_score=highest_score,

        plagiarism_percentage=percentage,

        ai_score=analysis["overall_score"],

        ai_confidence=analysis["confidence"],

        roberta_score=analysis["roberta"],

        perplexity_score=analysis["perplexity"],

        burstiness_score=analysis["burstiness"],

        stylometry_score=analysis["stylometry"],

        vocabulary_score=analysis["vocabulary"],

        repetition_score=analysis["repetition"],

        readability_score=analysis["readability"]

)

    db.session.add(result)
    db.session.commit()

    paragraphs = []
    sentences = []

    if best_document:

        paragraphs = find_matching_paragraphs(
            new_doc.extracted_text,
            best_document.extracted_text
        )

        sentences = compare_sentences(
            new_doc.extracted_text,
            best_document.extracted_text
        )

    from flask import current_app

    os.makedirs(
        current_app.config["REPORTS_FOLDER"],
        exist_ok=True
    )

    report_path = os.path.join(
        current_app.config["REPORTS_FOLDER"],
        f"report_{result.id}.pdf"
    )


    top_matches = []

    for item in matches[:5]:

        top_matches.append({

        "filename": item["document"].filename,

        "percentage": round(
            item["score"] * 100,
            2
        )

    })
        generate_pdf_report(
                report_path,
                new_doc,
                best_document,
                result,
                percentage,
                paragraphs,
                sentences,
                top_matches
            )

    result.report_path = report_path

    db.session.commit()

    return result

# =====================================================
# PARAGRAPH MATCHING
# =====================================================

def find_matching_paragraphs(
    text1,
    text2,
    threshold=0.80
):

    paras1 = split_into_paragraphs(text1)
    paras2 = split_into_paragraphs(text2)

    matches = []

    if not paras1 or not paras2:
        return matches

    # Generate embeddings only once
    para2_embeddings = []

    for p2 in paras2:

        para2_embeddings.append(
            (
                p2,
                generate_embedding(p2)
            )
        )

    for p1 in paras1:

        emb1 = generate_embedding(p1)

        best_score = 0
        best_match = None

        for paragraph2, emb2 in para2_embeddings:

            score = cosine_similarity(
                emb1,
                emb2
            )

            if score > best_score:

                best_score = score
                best_match = paragraph2

        if best_score >= threshold:

            matches.append(

                {
                    "source_paragraph": p1,
                    "matching_paragraph": best_match,
                    "score": round(best_score * 100, 2)
                }

            )

    return matches