from sentence_transformers import SentenceTransformer
from src.data_ingestion.vector_db import coll
from dotenv import load_dotenv, find_dotenv
from langchain.vectorstores import Chroma

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


def main(query):

    load_dotenv(find_dotenv())

    # Embedding model for query
    emb_model = SentenceTransformer("all-mpnet-base-v2")

    # query = "What is the full form of LEG?"

    docs = query_based_docs_extraction(query, emb_model)
    return docs

docs = main("What is the full form of LEG?")

if __name__=="__main__":
    main()