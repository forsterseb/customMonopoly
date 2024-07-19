import fitz  # PyMuPDF
import sys
from PIL import Image
import io

def crop_pdf(input_path: str, output_path: str):
    """Crop a pdf file to its contents.
    
    The result is stored at the output_path

    Parameters
    -----
    input_path: str: the path to the pdf file
    output_path: str: the path to the output file. can be a pdf or png/jpg file 
    """

    document = fitz.open(input_path)
    
    # Iterate over each page
    for page_number in range(len(document)):
        page = document.load_page(page_number)

        bbox = fitz.Rect(0, 0, 0, 0)
        
        # Get the bounding box of the text content
        for block in page.get_text("blocks"):
            bbox |= fitz.Rect(block[:4])
        
        # Get the bounding box of images
        for img in page.get_images(full=True):
            img_rect = page.get_image_bbox(img)
            bbox |= img_rect
        
        # Get the bounding box of drawings
        for draw in page.get_drawings():
            draw_rect = draw["rect"]
            bbox |= fitz.Rect(draw_rect)

        # Apply the crop if bbox is valid
        if bbox.is_empty or bbox.is_infinite:
            print(f"Skipping page {page_number + 1} due to empty content.")
        else:
            # validate bbox bounds
            x1 = max(0, bbox[0])
            x2 = max(0, bbox[1])
            x3 = min(page.mediabox.bottom_right.x, bbox[2])
            x4 = min(page.mediabox.bottom_right.y, bbox[3])
            bbox = fitz.Rect([x1,x2,x3,x4])
            page.set_cropbox(bbox)
    
    # Save the cropped PDF to a new file
    if output_path.split(".")[-1] in ['jpg', 'png']:
        pdf_to_img(document, output_path)
    else:
        document.save(output_path)
    document.close()

def pdf_to_img(pdf_doc:fitz.Document, out_path:str):
    """Save the first page of a pdf file to image. 
    
    Parameters
    -----
    pdf_doc: The loaded pdf using fitz
    out_path: str:  the path to the output image file 
    """

    page = pdf_doc.load_page(0)
    pixmap = page.get_pixmap(dpi=300)
    img = pixmap.tobytes()

    image = Image.open(io.BytesIO(img))
    image.save(out_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python crop_pdf.py input.pdf output.pdf")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        crop_pdf(input_path, output_path)
        print(f"Cropped PDF saved as {output_path}")
