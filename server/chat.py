import os
import pickle
from langchain.chains import RetrievalQA
from langchain import OpenAI
from langchain.memory import ConversationBufferMemory,ConversationBufferWindowMemory
import csv
from langchain.prompts import PromptTemplate
from langchain.document_loaders import UnstructuredURLLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter


os.environ['OPENAI_API_KEY'] = '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'

def get_urls():
    urls = []
    with open('utils/saatva_product_urls.txt', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row:
                for url in row: 
                    if url.strip():
                        urls.append(url.strip())
    return urls

def create_vectorized_store(): 
    urls = get_urls()
    loaders = UnstructuredURLLoader(urls=urls)
    data = loaders.load()
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size = 400, chunk_overlap = 30)

    docs = text_splitter.split_documents(data)

    embedding = OpenAIEmbeddings()

    vectorStore_openAI = FAISS.from_documents(docs, embedding)

    with open("faiss_store_openai.pkl", "wb") as f:
        pickle.dump(vectorStore_openAI, f)


def get_relevant_docs(VectorStore, question, k): 
    return VectorStore.similarity_search(question, k)


def queryLLM(message):
    # Uses Retrieval Augmented generation to return results
    if not os.path.exists("faiss_store_openai.pkl"):
        create_vectorized_store()

    with open("faiss_store_openai.pkl", "rb") as f:
        VectorStore = pickle.load(f)

    llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    question = message

    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use a couple of sentences max and keep the answer as concise as possible.
    {context}
    ---
    Question: {question}
    Helpful Answer:"""


    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)
    qa_chain = RetrievalQA.from_chain_type(llm,retriever=VectorStore.as_retriever(search_kwargs={'k': 2}),chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}, return_source_documents=True)
    result = qa_chain({"query": question})
    return result['result']