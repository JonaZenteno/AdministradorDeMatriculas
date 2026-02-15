import pypdf
import os

pdf_path = 'ilovepdf_merged.pdf'
output_path = 'extracted_text.txt'

if not os.path.exists(pdf_path):
    print(f"Error: {pdf_path} not found.")
else:
    try:
        reader = pypdf.PdfReader(pdf_path)
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, page in enumerate(reader.pages):
                f.write(f"\n--- PAGE {i+1} ---\n")
                f.write(page.extract_text())
        print(f"Extracted text saved to {output_path}")
    except Exception as e:
        print(f"Error reading PDF: {e}")
