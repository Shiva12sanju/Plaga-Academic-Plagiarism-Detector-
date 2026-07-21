import os
from difflib import SequenceMatcher

from models import db, Document, Embedding, Result

from ai.embeddings import (
    generate_embedding,
    serialize_embedding,
    deserialize_embedding
)

from ai.document_analysis import writing_quality
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
        return deserialize_embedding(
            existing.embedding
        )

    print(
        f"Generating embedding for {document.filename}"
    )

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
# TEXT SIMILARITY
# =====================================================

def sentence_similarity(text1, text2):

    sentences1 = split_sentences(
        clean_text(text1)
    )

    sentences2 = split_sentences(
        clean_text(text2)
    )


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


            best = max(
                best,
                score
            )


        if best >= 0.80:
            matches += 1


    return matches / len(sentences1)



def keyword_similarity(text1,text2):

    k1 = set(
        extract_keywords(text1)
    )

    k2 = set(
        extract_keywords(text2)
    )


    if not k1 or not k2:
        return 0


    return len(k1 & k2) / len(k1 | k2)



def overall_similarity(doc1,doc2):

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


    score = (
        semantic * 0.60
        +
        sentence * 0.25
        +
        keyword * 0.15
    )


    return round(score,4)



# =====================================================
# TWO DOCUMENT CHECK
# =====================================================

def check_plagiarism_between_two(doc1,doc2):


    score = overall_similarity(
        doc1,
        doc2
    )


    percentage = round(
        score * 100,
        2
    )


    result = Result(
        document1_id=doc1.id,
        document2_id=doc2.id,
        similarity_score=score,
        plagiarism_percentage=percentage
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


    filename = (
        f"report_{result.id}_"
        f"{doc1.id}_vs_{doc2.id}.pdf"
    )


    path = os.path.join(
        current_app.config["REPORTS_FOLDER"],
        filename
    )


    generate_pdf_report(
        path,
        doc1,
        doc2,
        percentage,
        matching_paragraphs,
        matching_sentences
    )


    result.report_path = path

    db.session.commit()


    return result




# =====================================================
# DATABASE COMPARISON
# =====================================================


def check_plagiarism_against_db(new_doc):


    documents = Document.query.filter(
        Document.id != new_doc.id
    ).all()



    if not documents:


        result = Result(
            document1_id=new_doc.id,
            document2_id=None,
            similarity_score=0,
            plagiarism_percentage=0
        )


        db.session.add(result)

        db.session.commit()



        analysis = writing_quality(
            new_doc.extracted_text
        )


        print(
            analysis
        )



        from flask import current_app


        os.makedirs(
            current_app.config["REPORTS_FOLDER"],
            exist_ok=True
        )


        path = os.path.join(
            current_app.config["REPORTS_FOLDER"],
            f"report_{result.id}_{new_doc.id}.pdf"
        )


        generate_pdf_report(
            path,
            new_doc,
            None,
            0,
            []
        )


        result.report_path = path

        db.session.commit()


        return result




    best_document = None

    highest_score = 0



    for doc in documents:


        score = overall_similarity(
            new_doc,
            doc
        )


        if score > highest_score:

            highest_score = score

            best_document = doc




    percentage = round(
        highest_score * 100,
        2
    )



    result = Result(

        document1_id=new_doc.id,

        document2_id=(
            best_document.id
            if best_document
            else None
        ),

        similarity_score=highest_score,

        plagiarism_percentage=percentage
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


    path = os.path.join(
        current_app.config["REPORTS_FOLDER"],
        f"report_{result.id}.pdf"
    )



    generate_pdf_report(
        path,
        new_doc,
        best_document,
        percentage,
        paragraphs,
        sentences
    )


    result.report_path = path

    db.session.commit()



    return result





# =====================================================
# PARAGRAPH MATCHING
# =====================================================


def find_matching_paragraphs(
        text1,
        text2,
        threshold=0.65
):


    paras1 = split_into_paragraphs(text1)

    paras2 = split_into_paragraphs(text2)


    matches = []


    for p1 in paras1:


        emb1 = generate_embedding(
            p1
        )


        best_score = 0

        best_match = None



        for p2 in paras2:


            emb2 = generate_embedding(
                p2
            )


            score = cosine_similarity(
                emb1,
                emb2
            )



            if score > best_score:

                best_score = score

                best_match = p2



        if best_score >= threshold:


            matches.append({

                "source_paragraph":p1,

                "matching_paragraph":best_match,

                "score":round(
                    best_score*100,
                    2
                )

            })



    return matches