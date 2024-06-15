import os
import glob
import subprocess

def convert_docx_to_pdf(docx_path, pdf_path):
    print("execute: docx -> pdf")
    subprocess.run(['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(pdf_path), docx_path])
    print("complete: docx -> pdf")


docx_dir = '../data/docx/'
pdf_dir = '../data/pdf/'
os.makedirs(pdf_dir, exist_ok=True)

# DOCXファイルのパスを取得
docx_files = glob.glob(os.path.join(docx_dir, '*.docx'))
print(docx_files)

# 各DOCXファイルをPDFに変換
for docx_path in docx_files:
    base_name = os.path.splitext(os.path.basename(docx_path))[0]
    pdf_path = os.path.join(pdf_dir, f"{base_name}.pdf")
    convert_docx_to_pdf(docx_path, pdf_path)

print("DOCX to PDF conversion complete.")
