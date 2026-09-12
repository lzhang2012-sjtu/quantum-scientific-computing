#!/usr/bin/env python3
"""Extract images from PDF file"""

import fitz  # PyMuPDF
import os
import sys

def extract_images_from_pdf(pdf_path, output_dir):
    """Extract all images from a PDF file"""

    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    image_count = 0

    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]

        # Get images on the page
        image_list = page.get_images(full=True)

        # Extract each image
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # Save the image
            image_filename = f"page_{page_num+1}_img_{img_index+1}.{image_ext}"
            image_path = os.path.join(output_dir, image_filename)

            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)

            print(f"Extracted: {image_filename}")
            image_count += 1

    pdf_document.close()
    print(f"\nTotal images extracted: {image_count}")
    return image_count

if __name__ == "__main__":
    pdf_path = "../material/talk_QNLA_tutorial_0411.pdf"
    output_dir = "images"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        extract_images_from_pdf(pdf_path, output_dir)
    except ImportError:
        print("PyMuPDF (fitz) not installed. Installing...")
        os.system("pip3 install PyMuPDF")
        print("\nPlease run the script again after installation.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
