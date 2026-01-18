from http import client
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-004",
    openai_api_key="YOUR_GEMINI_API_KEY",
    openai_api_base="https://generativelanguage.googleapis.com/v1beta/openai/"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning",
    embedding=embedding_model

)

# Take usinput
user_query = input("Enter your query : ")

# Relevant chunks from the vecto db
search_results = vector_db.similarity_search(query=user_query)

context="\n\n\n".join([f"Page Content: {result.page_content}\nPage Number:{result.metadata['page_label']}\nFile Location:{result.metadata['source']}"
for result in search_results
                       ])

SYSTEM_PROMPT = f"""
You are a helpful AI Assistant who answers user query based on the available
context retrieved from a PDF file along with page_content and page number.

You should only ans the user based on the following context and navigate the user
to open the right page number to know mores


Context:
{context}

"""

client = OpenAI(
    api_key="YOUR_GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
]
)

print(f"response: {response.choices[0].message.content}")