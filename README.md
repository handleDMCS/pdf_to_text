# 📄 PDF to Text (OCR)

A lightweight utility for extracting text from PDF files using **Tesseract OCR**. This tool is intended for scanned or image-based PDFs where traditional text extraction methods (like `PyPDF2` or `pdfminer`) are insufficient.

## 🧠 Use Case

This script was developed for preprocessing scanned documents as part of a larger pipeline. It is useful for digitizing and extracting content from PDFs that do not contain embedded text, such as scanned books, articles, or handwritten forms.

## 🔍 How It Works

1. Converts each PDF page into an image (using `pdf2image`)
2. Applies Tesseract OCR to recognize text from each image
3. Aggregates and outputs the extracted text into a plain `.txt` file (or similar)

## 🛠️ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/pdf_to_text.git
cd pdf_to_text
pip install -r requirements.txt
