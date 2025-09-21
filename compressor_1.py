import fitz  # PyMuPDF
from PIL import Image
import io
import os

INPUT_FOLDER = r"C:\Users\devya\OneDrive\Desktop\devyansh automation\compress\input\ilovepdf_extracted-pages"
OUTPUT_FOLDER = r"C:\Users\devya\OneDrive\Desktop\devyansh automation\compress\output"
TARGET_KB = 230
DPI = 60
JPEG_QUALITY = 50 # Lower = smaller size

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def compress_pdf(input_path, output_path):
    doc = fitz.open(input_path)
    new_doc = fitz.open()
    
    for page in doc:
        pix = page.get_pixmap(dpi=DPI)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Compress using Pillow
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="JPEG", quality=JPEG_QUALITY)
        img_buffer.seek(0)
        
        img_pdf = fitz.open()
        rect = fitz.Rect(0, 0, pix.width, pix.height)
        page_img = img_pdf.new_page(width=pix.width, height=pix.height)
        page_img.insert_image(rect, stream=img_buffer.read())  # ✅ insert JPEG bytes
        new_doc.insert_pdf(img_pdf)
    
    new_doc.save(output_path, deflate=True, garbage=4)
    new_doc.close()
    doc.close()

    size_kb = os.path.getsize(output_path) / 1024
    if size_kb > TARGET_KB:
        os.remove(output_path)
        return f"⚠️ {os.path.basename(input_path)} → {size_kb:.2f} KB — too large, removed"
    else:
        return f"✔ {os.path.basename(input_path)} → {size_kb:.2f} KB"

# Batch processing
for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith('.pdf'):
        in_path = os.path.join(INPUT_FOLDER, filename)
        out_path = os.path.join(OUTPUT_FOLDER, filename)
        try:
            result = compress_pdf(in_path, out_path)
            print(result)
        except Exception as e:
            print(f"❌ {filename} failed: {str(e)}")

print("\n✅ All done.")
