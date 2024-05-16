from typing import Any
from retrieval import main 
from query_processing import lemmatization
from memory import memory_with_VectorStore
from chains import chain_retrievalQA, conversational_RetrievalChain

class chatPipeline:
    def __init__(self):
        self.docs_retrieval = main
        self.query_preprocessing = lemmatization
        self.chainQA = chain_retrievalQA
        self.convChainQA = conversational_RetrievalChain
        self.memoryChain = memory_with_VectorStore

    def __call__(self, query):
        # Preprocessing of query
        preprocessed_query = self.query_preprocessing(query)
        print(preprocessed_query)

        # Performing query based doc retrieval
        if self.docs_retrieval:
            docs = self.docs_retrieval(preprocessed_query)
            if docs:
                return docs
            else:
                return f"No relevant docs based on {preprocessed_query}."

        # Performing QA chain on vector database
        if self.chainQA:
            response = self.chainQA(preprocessed_query)
            if response:
                return response
        
        # Performing QA conversation chain on vector database
        if self.convChainQA:
            response = self.convChainQA(preprocessed_query)
            if response:
                return response
        
        # Performing memory chain on vector database
        if self.memoryChain:
            response = self.memoryChain(preprocessed_query)
            if response:
                return response
        
        # Handling cases where no specific retrieval methods apply
        return f"Sorry, I couldn't find relevant information for '{query}'."
    
chatbot = chatPipeline()
response = chatbot("What is ReAL Objectives?")
print(response)