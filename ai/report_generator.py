import os
from datetime import datetime

def generate_pdf_report(report_path, doc1, doc2, plagiarism_percentage, matching_paragraphs=None):
    """
    Generates a PDF report using reportlab and saves it to report_path.
    If reportlab is not installed, it writes a basic text report as a fallback.
    """
    if matching_paragraphs is None:
        matching_paragraphs = []
        
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        
        # Setup document
        doc = SimpleDocTemplate(
            report_path,
            pagesize=letter,
            rightMargin=54, leftMargin=54,
            topMargin=54, bottomMargin=54
        )
        
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#2C3E50"),
            spaceAfter=12
        )
        
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#7F8C8D"),
            spaceAfter=20
        )
        
        heading2_style = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#2C3E50"),
            spaceBefore=15,
            spaceAfter=10
        )
        
        body_style = ParagraphStyle(
            'Body',
            parent=styles['BodyText'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#34495E")
        )
        
        bold_body_style = ParagraphStyle(
            'BoldBody',
            parent=body_style,
            fontName='Helvetica-Bold'
        )

        story = []
        
        # Title
        story.append(Paragraph("Plagiarism Analysis Report", title_style))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))
        story.append(Spacer(1, 10))
        
        # Summary Box Data
        score_color = "#E74C3C" # Red
        if plagiarism_percentage < 20:
            score_color = "#2ECC71" # Green
        elif plagiarism_percentage < 50:
            score_color = "#F39C12" # Orange
            
        summary_data = [
            [Paragraph("Document Audited:", bold_body_style), Paragraph(doc1.filename, body_style)],
            [Paragraph("Compared Against:", bold_body_style), Paragraph(doc2.filename if doc2 else "Database Repository", body_style)],
            [Paragraph("Overall Plagiarism Score:", bold_body_style), Paragraph(f"<font color='{score_color}'><b>{plagiarism_percentage}%</b></font>", bold_body_style)]
        ]
        
        summary_table = Table(summary_data, colWidths=[150, 350])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FA")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Findings Section
        story.append(Paragraph("Plagiarism Analysis Findings", heading2_style))
        if plagiarism_percentage == 0:
            story.append(Paragraph("No significant plagiarism detected. The document is unique based on comparison algorithms.", body_style))
        else:
            story.append(Paragraph(f"The analysis detected that {plagiarism_percentage}% of the document contains matches or significant similarity with previously uploaded documents.", body_style))
        story.append(Spacer(1, 15))
        
        # Matching Paragraphs Detail
        if matching_paragraphs:
            story.append(Paragraph("Detailed Paragraph Matches", heading2_style))
            
            for idx, match in enumerate(matching_paragraphs, 1):
                match_header_style = ParagraphStyle(
                    f'MatchHeader_{idx}',
                    parent=body_style,
                    fontName='Helvetica-Bold',
                    textColor=colors.HexColor("#2980B9")
                )
                
                story.append(Paragraph(f"Match #{idx} (Similarity: {match['score']}%):", match_header_style))
                story.append(Spacer(1, 5))
                
                # Table for paragraphs side-by-side
                p_table_data = [
                    [Paragraph("<b>Source Document</b>", bold_body_style), Paragraph("<b>Matched Document</b>", bold_body_style)],
                    [Paragraph(match['source_paragraph'], body_style), Paragraph(match['matching_paragraph'], body_style)]
                ]
                p_table = Table(p_table_data, colWidths=[245, 245])
                p_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
                    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
                    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('PADDING', (0,0), (-1,-1), 8),
                ]))
                story.append(p_table)
                story.append(Spacer(1, 15))
        
        # Build Document
        doc.build(story)
        print(f"Report successfully generated at: {report_path}")
        
    except ImportError:
        # Fallback to Text report if reportlab is not available
        print("ReportLab is not installed. Creating plain-text report fallback.")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("             PLAGIARISM ANALYSIS REPORT\n")
            f.write("="*60 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Source Document: {doc1.filename}\n")
            f.write(f"Target Document: {doc2.filename if doc2 else 'Database Repository'}\n")
            f.write(f"Plagiarism Score: {plagiarism_percentage}%\n\n")
            f.write("="*60 + "\n")
            f.write("DETAILED MATCHES:\n")
            f.write("="*60 + "\n")
            for idx, match in enumerate(matching_paragraphs, 1):
                f.write(f"\nMatch #{idx} (Similarity: {match['score']}%):\n")
                f.write(f"Source: {match['source_paragraph']}\n")
                f.write(f"Matched: {match['matching_paragraph']}\n")
                f.write("-"*60 + "\n")
    except Exception as e:
        print(f"Error generating report: {e}")
