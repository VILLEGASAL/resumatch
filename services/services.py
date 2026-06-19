import fitz

async def extract_text_from_file(file_name:str):

    document = fitz.open(f"uploaded_files/{file_name}")

    document_texts = ""

    for page_num in range(len(document)):

        page = document.load_page(page_num)

        document_texts += page.get_text()

    print(document_texts)

    document.close()