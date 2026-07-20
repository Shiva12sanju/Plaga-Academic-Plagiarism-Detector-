import os
import zipfile
import xml.etree.ElementTree as ET

def extract_text(file_path):
    """
    Extracts text from a document (PDF, DOCX, or TXT).
    """
    if not os.path.exists(file_path):
        return None
        
    ext = file_path.rsplit('.', 1)[1].lower()
    
    if ext == 'txt':
        return _extract_txt(file_path)
    elif ext == 'pdf':
        return _extract_pdf(file_path)
    elif ext == 'docx':
        return _extract_docx(file_path)
        
    return None

def _extract_txt(file_path):
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'utf-16']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    return None

def _extract_pdf(file_path):
    """
    Try parsing using PyMuPDF (fitz) or pdfplumber, with a fallback to PyPDF2.
    """
    text = ""
    
    # Try PyMuPDF (fitz)
    try:
        import fitz
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception as e:
        print(f"Error reading PDF with PyMuPDF: {e}")
        
    # Try pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception as e:
        print(f"Error reading PDF with pdfplumber: {e}")

    # Try PyPDF2
    try:
        import PyPDF2
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception as e:
        print(f"Error reading PDF with PyPDF2: {e}")

    return text if text.strip() else None

def _extract_docx(file_path):
    """
    Reads DOCX file using python-docx if available, or direct XML parsing of document.xml.
    """
    try:
        import docx
        doc = docx.Document(file_path)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)
    except ImportError:
        # Fallback to direct XML parsing of the zip
        try:
            with zipfile.ZipFile(file_path) as docx_zip:
                xml_content = docx_zip.read('word/document.xml')
                root = ET.fromstring(xml_content)
                
                # Namespaces
                ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                
                paragraphs = []
                for p in root.findall('.//w:p', ns):
                    texts = []
                    for t in p.findall('.//w:t', ns):
                        if t.text:
                            texts.append(t.text)
                    if texts:
                        paragraphs.append("".join(texts))
                return "\n".join(paragraphs)
        except Exception as e:
            print(f"XML Fallback docx parsing error: {e}")
            return None
    except Exception as e:
        print(f"python-docx parsing error: {e}")
        return None
