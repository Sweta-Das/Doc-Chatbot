# Reading PDF
from dotenv import load_dotenv, find_dotenv
import os
import re
import PyPDF2

load_dotenv(find_dotenv())

pdf_pth = os.environ['pdf_path']


# Extracting Table of Contents
def extract_ToC(pdf_pth, page):

    with open(pdf_pth, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        toc_entries = []

        toc_page = pdf_reader.pages[page]
        text = toc_page.extract_text()
            
        toc_lines = text.splitlines()

        for i in toc_lines:
            toc_entries.append(i)
        
        return toc_entries
    
toc = extract_ToC(pdf_pth, 5)

# Removing unnecessary contents
toc = toc[:-2]

# Parsing table of contents
def parsing_toc(toc_ls):
    toc_entries = []
    toc_pattern = re.compile(r'^(.*?)\s+(\d+)\s*$')

    for entry in toc_ls:
        match = toc_pattern.match(entry)
        if match:
            topic = re.sub(r'\.{2,}', '', match.group(1)).strip()
            page = int(match.group(2))
            ToC_dict = {
                "topic": topic,
                "pg": page
            }
            toc_entries.append(ToC_dict)
    return toc_entries


toc_entries = parsing_toc(toc)
toc_entries = toc_entries[:-2]

# Improvising the table of content
topics_to_keep = [
    'FOREWORD',
    'ABBREVIATIONS',
    'Recovery and Accelerated Learning (ReAL)',
    'The Road Map for Recovery and Accelerated Learning'
]

fltr_toc = [entry for entry in toc_entries if entry['topic'] in topics_to_keep]