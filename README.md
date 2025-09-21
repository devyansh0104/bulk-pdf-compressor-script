PDF Compressor: Smart Optimization for Your Documents
This repository contains a simple yet powerful Python script to compress PDF files. It intelligently handles different page types (text and images) and aims to meet a target file size, making it perfect for preparing documents for email, web uploads, or storage.

🚀 Features
✅ Adaptive Compression
Automatically analyzes each page, preserving the quality of text and vector graphics while aggressively compressing large, image-heavy pages using optimized settings.

✅ Precision Target Sizing
Iteratively adjusts image quality (DPI and JPEG compression) across multiple attempts to get the file size as close as possible to your desired target (in KB).

✅ Batch Processing
Designed to process all PDF files within a designated input folder, making bulk compression a seamless, automated process.

✅ Real-time Feedback
Provides clear, instant feedback on the compression result for every file, including the final file size and any challenges encountered.

🛠️ Tech Stack
Python

PyMuPDF (fitz)

Pillow

▶️ How to Run
1. Clone the repository:

Bash

git clone https://github.com/your-username/python-pdf-compressor.git
cd python-pdf-compressor
2. Install dependencies:
Make sure you have the required libraries installed.

Bash

pip install PyMuPDF Pillow
3. Configure settings:
Open the compressor_2.py file and modify the following variables to match your setup:

INPUT_FOLDER: The path to the folder containing the PDF files you want to compress.

OUTPUT_FOLDER: The path where the compressed PDFs will be saved.

TARGET_KB: The desired file size in kilobytes (e.g., 230 for 230 KB).
4. Execute the script:
Place your PDF files in the INPUT_FOLDER, then run the script from your terminal.

Bash
0
python compressor_2.py
The script will automatically begin processing each PDF, and the final compressed files will be saved in the OUTPUT_FOLDER.
