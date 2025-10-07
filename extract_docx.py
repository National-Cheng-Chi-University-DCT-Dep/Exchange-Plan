#!/usr/bin/env python3
"""
Temporary script to extract text from docx files for review
"""
import os
import sys

try:
    from docx import Document
except ImportError:
    print("python-docx not installed, installing...")
    os.system("pip install python-docx")
    from docx import Document

def extract_text_from_docx(file_path):
    """Extract text from a docx file"""
    try:
        doc = Document(file_path)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return '\n'.join(text)
    except Exception as e:
        return f"Error reading file: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_docx.py <docx_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    text = extract_text_from_docx(file_path)
    print(text)

