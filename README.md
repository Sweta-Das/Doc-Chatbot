# ILAB-Doc-Chatbot
Technical Assessment Round-2

## Task-1: Data Preprocessing
- Installing libraries from requirements.txt `pip install -r requirements.txt`
- PDF Text Extraction through its Table of Contents using **PyPDF2** library
- Chunking of texts

## Task-2: Data Ingestion
- Connecting to **Chroma DB** Hosted on **Docker**
    - Starting docker on WSL-Ubuntu with `sudo service docker start`
    - Pulling chromadb image with `docker pull chromadb/chroma`
    - Creating container and opening port with `docker run -d -p 8080:8080 --name chromadb chromadb/chroma`
- Using Hugging Face Embeddings to perform text embedding using **Sentence Transformer** library
- Creating collection on Chroma DB to add embeddings, and its metadata

## Task-3: Creating Chat Pipeline
- **Retrieval**
    - Query Based Documents Extraction -> Extracting relevant documents from vector database based on user's query
    - Ranking the retrieved results based on similarity
- **Chains**
    - Maintaining conversation flow through **LLMChain()** of LangChain
- **Chains with Memory**
    - Maintaining conversation flow using memory with **ConversationChain()** of LangChain
- **Query Processing**
    - Handling incoming queries from users, preprocessing them & passing to LLM to generate response with vector database acting as retriever
- **Chat Pipeline**
    - Creating a chat pipeline class where all the above components will be integrated

Every folder in this project contains a Jupyter notebook (.ipynb) file to display intermediate outputs.

*P.S. This project aims to build the PDF chatbot concentrated on a single PDF file. But, it can be scaled to include multiple PDFs, if they have the same formats, so that they can be chunked properly.*