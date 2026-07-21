import os
from datetime import datetime


def generate_pdf_report(
    report_path,
    doc1,
    doc2,
    plagiarism_percentage,
    matching_paragraphs=None,
    matching_sentences=None
):
    """
    Generates a plagiarism PDF report.
    Falls back to text report if ReportLab is unavailable.
    """

    if matching_paragraphs is None:
        matching_paragraphs = []

    if matching_sentences is None:
        matching_sentences = []

    try:

        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle
        )

        from reportlab.lib.styles import (
            getSampleStyleSheet,
            ParagraphStyle
        )

        from reportlab.lib import colors

        doc = SimpleDocTemplate(
            report_path,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "Title",
            parent=styles["Heading1"],
            fontSize=22,
            leading=28,
            textColor=colors.darkblue,
            spaceAfter=15
        )

        heading_style = ParagraphStyle(
            "Heading",
            parent=styles["Heading2"],
            fontSize=15,
            leading=18,
            textColor=colors.darkred,
            spaceAfter=10
        )

        body_style = ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontSize=10,
            leading=15
        )

        bold_style = ParagraphStyle(
            "Bold",
            parent=body_style,
            fontName="Helvetica-Bold"
        )

        story = []

        ###################################################
        # TITLE
        ###################################################

        story.append(
            Paragraph(
                "Academic Plagiarism Detection Report",
                title_style
            )
        )

        story.append(
            Paragraph(
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),
                body_style
            )
        )

        story.append(Spacer(1, 20))

        ###################################################
        # SUMMARY
        ###################################################

        if plagiarism_percentage < 20:
            color = "green"

        elif plagiarism_percentage < 50:
            color = "orange"

        else:
            color = "red"

        table = Table(

            [

                [
                    "Uploaded File",
                    doc1.filename
                ],

                [
                    "Matched File",
                    doc2.filename if doc2 else "No Match"
                ],

                [
                    "Plagiarism",
                    f"{plagiarism_percentage}%"
                ]

            ],

            colWidths=[170, 300]

        )

        table.setStyle(

            TableStyle(

                [

                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),

                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

                    ("BACKGROUND", (0, 1), (0, -1), colors.whitesmoke),

                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

                ]

            )

        )

        story.append(table)

        story.append(Spacer(1, 20))

        ###################################################
        # RESULT
        ###################################################

        story.append(
            Paragraph(
                "Analysis",
                heading_style
            )
        )

        story.append(

            Paragraph(

                f"<font color='{color}'>"

                f"<b>{plagiarism_percentage}% plagiarism detected.</b>"

                "</font>",

                body_style

            )

        )

        story.append(Spacer(1, 20))

        ###################################################
        # MATCHED PARAGRAPHS
        ###################################################

        if matching_paragraphs:

            story.append(
                Paragraph(
                    "Matched Paragraphs",
                    heading_style
                )
            )

            for i, item in enumerate(
                matching_paragraphs,
                start=1
            ):

                story.append(

                    Paragraph(

                        f"<b>Paragraph {i}</b> "
                        f"({item['score']}%)",

                        bold_style

                    )

                )

                story.append(

                    Paragraph(

                        item["source_paragraph"],

                        body_style

                    )

                )

                story.append(Spacer(1, 5))

                story.append(

                    Paragraph(

                        item["matching_paragraph"],

                        body_style

                    )

                )

                story.append(Spacer(1, 15))

        ###################################################
        # MATCHED SENTENCES
        ###################################################

        if matching_sentences:

            story.append(
                Paragraph(
                    "Matched Sentences",
                    heading_style
                )
            )

            story.append(Spacer(1, 10))

            for item in matching_sentences:

                story.append(

                    Paragraph(

                        f"<font color='red'><b>Student:</b></font> "
                        f"{item['sentence']}",

                        body_style

                    )

                )

                story.append(

                    Paragraph(

                        f"<b>Matched ({item['similarity']}%)</b>",

                        bold_style

                    )

                )

                story.append(

                    Paragraph(

                        item["matched_sentence"],

                        body_style

                    )

                )

                story.append(
                    Spacer(1, 10)
                )

        ###################################################
        # END
        ###################################################

        story.append(Spacer(1, 20))

        story.append(

            Paragraph(

                "Generated by AI Academic Plagiarism Detector",

                body_style

            )

        )

        doc.build(story)

        print("PDF Report Generated")

    except ImportError:

        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write("PLAGIARISM REPORT\n")
            f.write("=" * 50 + "\n")
            f.write(
                f"Generated : {datetime.now()}\n"
            )
            f.write(
                f"Uploaded : {doc1.filename}\n"
            )
            f.write(
                f"Matched : {doc2.filename if doc2 else 'No Match'}\n"
            )
            f.write(
                f"Plagiarism : {plagiarism_percentage}%\n\n"
            )

            f.write(
                "Matched Paragraphs\n"
            )

            for item in matching_paragraphs:

                f.write(
                    "-" * 50 + "\n"
                )

                f.write(
                    item["source_paragraph"] + "\n\n"
                )

                f.write(
                    item["matching_paragraph"] + "\n\n"
                )

            if matching_sentences:

                f.write("\nMatched Sentences\n")

                for item in matching_sentences:

                    f.write("-" * 50 + "\n")

                    f.write(
                        item["sentence"] + "\n"
                    )

                    f.write(
                        item["matched_sentence"] + "\n"
                    )

    except Exception as e:

        print(e)