from PIL import Image, ImageOps

def resize_img_to_pdf_page(img, reader, keep_aspect=True, fill_color=(255, 255, 255)):
    """
    Resize (or letterbox) a PIL image so its final size matches the
    first page of a PDF (from PdfReader). Returns a new PIL Image.
    - img: PIL.Image
    - reader: PdfReader
    - keep_aspect: True keeps proportions with letterboxing
    - fill_color: RGB tuple for background fill
    """
    # Get PDF first-page dimensions (points) and round to integers
    page = reader.pages[0]
    width = int(page.mediabox.width)
    height = int(page.mediabox.height)

    # Ensure proper orientation (swap if PDF is landscape)
    if width < height:
        width, height = height, width

    # Work on a copy of the image
    img = img.convert("RGB")
    src_w, src_h = img.size

    if keep_aspect:
        # Scale to fit inside the PDF page, preserving ratio
        scale = min(width / src_w, height / src_h)
        new_w = int(src_w * scale)
        new_h = int(src_h * scale)
        resized = img.resize((new_w, new_h), resample=Image.LANCZOS)

        # Center it on a blank canvas the size of the PDF page
        result = Image.new("RGB", (width, height), fill_color)
        x = (width - new_w) // 2
        y = (height - new_h) // 2
        result.paste(resized, (x, y))
    else:
        # Stretch to full page (may introduce slight softness)
        result = img.resize((width, height), resample=Image.LANCZOS)

    return result
