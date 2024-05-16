from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import RetrievalQA, create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import find_dotenv, load_dotenv
import chromadb
import os

load_dotenv(find_dotenv())

HF_KEY = os.environ['HUGGINGFACE_API_KEY']

client = chromadb.HttpClient(host="localhost", port=8000)

# Defining LLM
llm = HuggingFaceEndpoint(
        repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1",
        huggingfacehub_api_token = HF_KEY)

# Query embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2",
                                   model_kwargs={"device": "cpu"})
    
# Using vector database as retriever
vector_db = Chroma(
        collection_name="pdf_embedding_collection",
        embedding_function=embeddings,
        client=client
    )

def chain_retrievalQA(query):

    # Using vector database as retriever
    retriever = vector_db.as_retriever()

    qa = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type="stuff",
        retriever=retriever,
        verbose=True
    )

    # Defining prompt
    prompt = f"""
    <|system|>You are a PDF Chatbot that gives responses based on the context provided in the PDF. Please given correct response and if there is no answer, say so.
    </s>
    <|user|>
    {query}
    </s>
    <|PDF Chatbot|>
    """

    response = qa.invoke(prompt)
    return response


def conversational_RetrievalChain(input):

    # Prompt to generate search query for retriever
    srch_qry_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}"),
        ("user","Given the above conversation, generate a search query to look up to get information relevant to the conversation")
    ])

    # Using vector database as retriever
    retriever = vector_db.as_retriever()

    # Creating retriever chain to return docs from Chroma DB
    retriever_chain = create_history_aware_retriever(llm, retriever, srch_qry_prompt)

    ans_prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\\n\\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}"),
    ])

    # Creating doc chain to send prompt to LLM
    doc_chain=create_stuff_documents_chain(llm, ans_prompt)        

    # Creating retrieval chain
    retrieval_chain = create_retrieval_chain(retriever_chain, doc_chain)

    # Creating chat history
    chat_history = [
        HumanMessage(
            content="When was the ReAL organized in Nepal?",
        ),
        AIMessage(
            content="The Recovery and Accelerated Learning (ReAL) Plan was organized in Nepal in 2023."
        )
    ]

    res = retrieval_chain.invoke({
        "chat_history": chat_history,
        "input": "What is the motivation of ReAL Plan?"
    })
    return res['answer']  
