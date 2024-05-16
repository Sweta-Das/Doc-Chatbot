# Text Preprocessing Before Embedding
from src.data_preprocessing.pdf_reader import fltr_toc
from dotenv import load_dotenv, find_dotenv
import os
import PyPDF2
import sys

# Extracting text from PDF
def extract_text_from_pdf(pdf_pth, start_page, end_page):
    with open(pdf_pth, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(start_page, end_page):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

# Initial chunking of text based on pages
def init_chunking_text(pdf_pth, toc_entries):
    initial_txt = []
    for i in range(len(toc_entries)):
        start_pg = toc_entries[i]['pg']
        end_pg = toc_entries[i+1]['pg'] if i < len(toc_entries)-1 else 30
        txt = extract_text_from_pdf(pdf_pth, start_pg, end_pg)
        initial_txt.append(txt)
    initial_txt = [i for i in initial_txt if i.strip()] # Removed empty strings
    return initial_txt
    
def main():
    
    # Loading environment variables
    load_dotenv(find_dotenv())

    pdf_pth = os.environ['pdf_path']
    sys_path = os.environ['sys_path']
    sys.path.append(sys_path)

    # Total number of pages in pdf
    with open(pdf_pth, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
    txt_chnks = init_chunking_text(pdf_pth, fltr_toc)

    # Extracting foreword and abbraviations
    frwd_abb = txt_chnks[0].split('|')
    frwd = frwd_abb[0]
    abb = ' | '.join(part.strip() for part in frwd_abb[1:])

    # Removing Table of Contents
    toc_c = txt_chnks[1].split('|')
    content = ' | '.join(part.strip() for part in toc_c[1:])

    chunks = [frwd, abb, content, txt_chnks[2]]

    # Creating topic_content list
    topic_content = []
    for i in range(len(chunks)):
        topic_content_dict = {
            "topic": fltr_toc[i]['topic'],
            "content": chunks[i]
        }
        topic_content.append(topic_content_dict)

    return topic_content

topic_content = main()

if __name__=="__main__":
    main()