# Creating Vector Database using Chroma DB
import os
import sys
import uuid
import chromadb
from dotenv import find_dotenv, load_dotenv
from src.data_preprocessing.text_preprocessing import topic_content
import chromadb.utils.embedding_functions as embedding_functions


# Adding embeddings to collection
def embeddings(pdf_coll, topic_content):
    for i in topic_content:
        id = uuid.uuid1()
        metadata = {'topic': i['topic']}
        docs = i['content']
        # print(id, metadata, docs)
        # print("....................")

        # Adding to collection
        pdf_coll.add(ids=[str(id)],
                    documents=docs,
                    metadatas=[metadata])
        
def main():
    # Environment variables
    load_dotenv(find_dotenv())

    HF_KEY = os.environ['HUGGINGFACE_API_KEY']

    # Connecting to Chroma DB server through HTTP client
    chroma_client = chromadb.HttpClient(host="localhost", port=8000)

    # LLM for embedding function
    hf_ef = embedding_functions.HuggingFaceEmbeddingFunction(
        api_key=HF_KEY,
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    # Creating Chroma DB list to store embeddings
    pdf_coll = chroma_client.get_or_create_collection(name="pdf_embedding_collection",
                                                    embedding_function=hf_ef)
        
    embeddings(pdf_coll, topic_content)

    # Creating pdf_coll_dict to contain information about collection
    pdf_coll_dict = {
        "collection_name": "pdf_embedding_collection",
        "LLM_model": "sentence-transformers/all-mpnet-base-v2"
    }

    return hf_ef, pdf_coll, pdf_coll_dict

hf, coll, coll_dict = main()

if __name__=="__main__":
    main()