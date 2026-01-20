from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore


#Vector Embeddings
embedding_model=OpenAIEmbeddings(
    model="text-embedding-004",
    openai_api_key="",
    openai_api_base="https://generativelanguage.googleapis.com/v1beta/openai/"
    
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning",
    embedding=embedding_model

)

client = OpenAI(
    api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def process_query(query:str):
    print("Searching Chunks", query)
    search_results = vector_db.similartiy_search(query=query)


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
    
    response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query}
    ]
    )
    print(f"response:{response.choices[0].message.content}")
    return response.choices[0].message.content
   
    
    
    # print(f"response: {response.choices[0].message.content}")
    