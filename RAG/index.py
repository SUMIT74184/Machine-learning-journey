from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
pdf_path= Path(__file__).parent/"springboot.pdf"

# Load this file in python program
loader=PyPDFLoader(file_path = pdf_path)
docs = loader.load()

print(docs[12])


# Split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=490
)

chunks = text_splitter.split_documents(documents=docs)

# Vector Embeddings
embedding_model=OpenAIEmbeddings(
    model="text-embedding-004",
    openai_api_key="YOUR_GEMINI_API_KEY",
    openai_api_base="https://generativelanguage.googleapis.com/v1beta/openai/"
    
)

vector_store=QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning"

)

print("Indexing your chunks completely")

# we are using gemini key and using openAI sdk to setup our RAG model

# llm = ChatOpenAI(
#     model="gemini-2.5-flash",
#     openai_api_key="YOUR_GEMINI_API_KEY",
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",

# )

# response=llm.invoke("Explain Springboot in short")
# print(response.content)