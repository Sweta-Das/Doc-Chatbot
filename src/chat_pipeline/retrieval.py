from sentence_transformers import SentenceTransformer
from src.data_ingestion.vector_db import hf, coll, coll_dict
from dotenv import load_dotenv, find_dotenv
from langchain.vectorstores import Chroma
import chromadb
import sys
import os

# Docs extraction from querying the vector database
def query_based_docs_extraction(query: str, emb_model):
    try:
        query_vector = emb_model.encode(query).tolist()
        result = coll.query(
            query_embeddings=[query_vector],
            n_results=4,
            include=['metadatas', 'distances']
        )
        print(f"Query: {query}")
        print("\n-----------------")
        print(f"Result: {result}")

        return result
        
    except Exception as e:
        print("Vector Search failed! ", e)


def main():

    load_dotenv(find_dotenv())
    client = chromadb.HttpClient(host="localhost", port=8000)

    # Embedding model for query
    emb_model = SentenceTransformer("all-mpnet-base-v2")

    query = "What is the full form of LEG?"

    docs = query_based_docs_extraction(query, emb_model)
    return docs

docs = main()

if __name__=="__main__":
    main()