import fitz
from PIL import Image
import io
import os

# -----------------------------
# SETTINGS
# -----------------------------
INPUT_FOLDER = r"C:\Users\devya\OneDrive\Desktop\devyansh automation\compress\input\ilovepdf_extracted-pages"
OUTPUT_FOLDER = r"C:\Users\devya\OneDrive\Desktop\devyansh automation\compress\output"
TARGET_KB = 230

DEFAULT_DPI = 80
DEFAULT_JPEG_QUALITY = 50
MIN_DPI = 40
MIN_QUALITY = 30
MAX_TRIES = 3

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# -----------------------------
# HELPERS
# -----------------------------
def is_text_page(page):
    return bool(page.get_text().strip())


def compress_image_page(page, dpi, quality):
    pix = page.get_pixmap(dpi=dpi)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)

    img_pdf = fitz.open()
    rect = fitz.Rect(0, 0, pix.width, pix.height)
    new_page = img_pdf.new_page(width=pix.width, height=pix.height)
    new_page.insert_image(rect, stream=buffer.read())
    return img_pdf


# -----------------------------
# MAIN COMPRESSION FUNCTION
# -----------------------------
def compress_pdf(input_path, output_path, target_kb):
    doc = fitz.open(input_path)

    dpi = DEFAULT_DPI
    jpeg_quality = DEFAULT_JPEG_QUALITY
    attempt = 0

    while attempt < MAX_TRIES:
        new_doc = fitz.open()

        for page in doc:
            if is_text_page(page):
                new_doc.insert_pdf(doc, from_page=page.number, to_page=page.number)
            else:
                img_pdf = compress_image_page(page, dpi, jpeg_quality)
                new_doc.insert_pdf(img_pdf)

        # Global compression: garbage collection, deflate, clean
        new_doc.save(output_path, garbage=4, deflate=True, clean=True)
        new_doc.close()

        size_kb = os.path.getsize(output_path) / 1024
        if size_kb <= target_kb:
            doc.close()
            return f"✔ {os.path.basename(input_path)} → {size_kb:.2f} KB ✅"

        # Lower settings for next attempt
        attempt += 1
        dpi = max(MIN_DPI, dpi - 10)
        jpeg_quality = max(MIN_QUALITY, jpeg_quality - 5)

    # After all attempts
    doc.close()
    final_size_kb = os.path.getsize(output_path) / 1024
    return f"⚠️ {os.path.basename(input_path)} → {final_size_kb:.2f} KB (best effort)"


# -----------------------------
# BATCH PROCESSING
# -----------------------------
def batch_compress_folder(input_folder, output_folder, target_kb):
    files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    if not files:
        print("❗ No PDF files found in input folder.")
        return

    for filename in files:
        in_path = os.path.join(input_folder, filename)
        out_path = os.path.join(output_folder, filename)
        try:
            result = compress_pdf(in_path, out_path, target_kb)
            print(result)
        except Exception as e:
            print(f"❌ {filename} failed: {str(e)}")

    print("\n✅ All done.")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    batch_compress_folder(INPUT_FOLDER, OUTPUT_FOLDER, TARGET_KB)
