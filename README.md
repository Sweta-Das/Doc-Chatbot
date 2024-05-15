# ILAB-Doc-Chatbot
Technical Assessment Round-2


**Task-1: Data Preprocessing**
- Installing libraries from requirements.txt `pip install -r requirements.txt`
- PDF Text Extraction through its Table of Contents using PyPDF2 library

**Task-2: Data Ingestion**
- Connecting to Chroma DB Hosted on Docker
    - Starting docker on WSL-Ubuntu with `sudo service docker start`
    - Pulling chromadb image with `docker pull chromadb/chroma`
    - Creating container and opening port with `docker run -d -p 8080:8080 --name chromadb chromadb/chroma`
- Using LangChain and Hugging Face Embeddings to perform embedding using Sentence Transformer library
- Creating collection on Chroma DB to add embeddings, and its metadata

**Task-3: Creating Chat Pipeline**