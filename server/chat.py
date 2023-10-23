import openai 
import os
import pickle
from langchain.chains import RetrievalQAWithSourcesChain, ConversationalRetrievalChain, RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain import OpenAI
import csv
from langchain.prompts import PromptTemplate
from langchain.document_loaders import UnstructuredURLLoader
import faiss 
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
                    if len(url): 
                        urls.append(url)
    return urls

def create_vectorized_store(): 
    urls = get_urls()

    loaders = UnstructuredURLLoader(urls=urls)
    data = loaders.load()


    # try using HTMLHeaderTextSplitter? 
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size = 400, chunk_overlap = 30)

    docs = text_splitter.split_documents(data)

    embedding = OpenAIEmbeddings()

    vectorStore_openAI = FAISS.from_documents(docs, embedding)

    with open("faiss_store_openai.pkl", "wb") as f:
        pickle.dump(vectorStore_openAI, f)



def queryGPT(message): 

    with open("faiss_store_openai.pkl", "rb") as f:
        VectorStore = pickle.load(f)

    llm = OpenAI(temperature=0)

    # chain = RetrievalQAWithSourcesChain(llm=llm, chain_type="stuff", retriever = VectorStore.as_retriever())

    # # qa = ConversationalRetrievalChain.from_llm(llm, retriever=VectorStore.as_retriever(), return_only_outputs=True)
    # # print(qa)


    # print(chain({'question' : "What is the price of the saatva-classic mattress?"}, return_only_outputs=True))
    # question = "Which mattress should i buy for kids?"
    # docs = VectorStore.similarity_search(question) 
    # # print("HERE")
    # print(docs)

    question = message

    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use one sentence maximum and keep the answer as concise as possible. 
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)
    # print(QA_CHAIN_PROMPT)

    qa_chain = RetrievalQA.from_chain_type(llm,retriever=VectorStore.as_retriever(),chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}, return_source_documents=True)
    result = qa_chain({"query": question})
    # print(result)
    # print(result["result"])
    return result['result']