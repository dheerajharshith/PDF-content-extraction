import fitz  # PyMuPDF
import os
import json
from PIL import Image
from pathlib import Path

# Create folder for images
image_dir = Path("images")
image_dir.mkdir(exist_ok=True)

# Load the PDF
pdf_path = "IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf"
 # Replace with your file name
doc = fitz.open(pdf_path)

extracted_data = []

# Iterate through each page
for page_num, page in enumerate(doc, start=1):
    print(f"Processing page {page_num}...")
    
    # Extract text
    text = page.get_text()
    
    # Extract images
    image_list = page.get_images(full=True)
    page_images = []
    
    for img_index, img in enumerate(image_list, start=1):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_filename = f"page{page_num}_image{img_index}.{image_ext}"
        image_path = image_dir / image_filename
        
        # Save image
        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)
        
        page_images.append(str(image_path))

    # Create one question per page (you can customize this further)
    if text.strip() or page_images:
        extracted_data.append({
            "page": page_num,
            "question": text.strip().split('\n')[0] if text else "Image-based question",
            "images": page_images[0] if page_images else "",
            "option_images": page_images[1:] if len(page_images) > 1 else []
        })

# Save to JSON
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(extracted_data, f, indent=4)

print("\n✅ Extraction complete. Check 'output.json' and 'images/' folder.")

