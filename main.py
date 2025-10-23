from collections import deque
from pypdf import PdfReader, PdfWriter
import copy
from PIL import Image
from io import BytesIO
import resizer

def split_page(page):
    width = page.mediabox.width
    height = page.mediabox.height
    # print(width, height)
    # page.rotate(0)  # Reset rotation to 0 degrees
    
    left_page = copy.deepcopy(page)
    right_page = copy.deepcopy(page)

    if width > height:
        left_page.mediabox.upper_right = (width / 2, height)
        right_page.mediabox.lower_left = (width / 2, 0)
    else:
        left_page.mediabox.lower_right = (width, height / 2)
        right_page.mediabox.upper_right = (width, height / 2)

    return left_page, right_page

def process_book(pages, cover_page):
# pattern: 10|11, 12|9, 8|13, 14|7, 6|15, 16|5, 4|17, 18|3, 2|19, 20|1
    # if cover_pages is not None:
    #     pages.append(cover_pages[0])  # Add cover page at the end
    dq = deque()
    is_odd_page = True
    for page in pages:
        left, right = split_page(page)

        if is_odd_page:
            dq.appendleft(left)
            dq.append(right)
        else:
            dq.appendleft(right)
            dq.append(left)

        is_odd_page = not is_odd_page

    if cover_page is not None:
        left, right = split_page(cover_page)
        dq.appendleft(right)
        dq.append(left)

    return dq

def write_dq(dq):
    output_path = "output.pdf"
    writer = PdfWriter()
    for page in dq:
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)


def main():
    input_path = "content.pdf"
    reader = PdfReader(input_path)

    cover_page = None
    cover_path = "cover.jpg"
    cover_img = Image.open(cover_path)

    if cover_img is not None:
        cover_img = resizer.resize_img_to_pdf_page(cover_img, reader)
        buffer = BytesIO()
        cover_img.save(buffer, format="PDF")
        buffer.seek(0)
        cover_reader = PdfReader(buffer)
        cover_page = cover_reader.pages[0]

    dq = process_book(reader.pages, cover_page)
    write_dq(dq)

main()
