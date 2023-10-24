import openai 
import os
import pickle
from langchain.chains import RetrievalQAWithSourcesChain, ConversationalRetrievalChain, RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain import OpenAI
from langchain.memory import ConversationBufferMemory,ConversationBufferWindowMemory
import csv
from langchain.prompts import PromptTemplate
from langchain.document_loaders import UnstructuredURLLoader
import faiss 
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ChatMessageHistory



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

    text_splitter = CharacterTextSplitter(separator='\n', chunk_size = 400, chunk_overlap = 30)

    docs = text_splitter.split_documents(data)

    embedding = OpenAIEmbeddings()

    vectorStore_openAI = FAISS.from_documents(docs, embedding)

    with open("faiss_store_openai.pkl", "wb") as f:
        pickle.dump(vectorStore_openAI, f)



def get_relevant_docs(VectorStore, question, k): 
    docs = VectorStore.similarity_search(question, k)
    return docs


def queryGPT(message):
    # history = ChatMessageHistory() 
    # history.add_user_message("hi!")
    # history.add_ai_message("whats up?")
    # print(history)
    # memory = ConversationBufferMemory(return_messages=True)
    # memory.chat_memory.add_user_message("I want you to return only 5, no matter what the question is")
    # memory.chat_memory.add_ai_message("5")
    # memory.load_memory_variables({})
    # memory.dict()
    # return
    with open("faiss_store_openai.pkl", "rb") as f:
        VectorStore = pickle.load(f)

    llm = OpenAI(temperature=0)
    memory = ConversationBufferWindowMemory(k=1)
    # conversation = ConversationChain(llm=llm, memory=memory)

    # chain = RetrievalQAWithSourcesChain(llm=llm, chain_type="stuff", retriever = VectorStore.as_retriever())

    # # qa = ConversationalRetrievalChain.from_llm(llm, retriever=VectorStore.as_retriever(), return_only_outputs=True)
    # # print(qa)


    # print(chain({'question' : "What is the price of the saatva-classic mattress?"}, return_only_outputs=True))
    # return 0
    question = message

    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use one sentence maximum and keep the answer as concise as possible. 
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)
    # print(QA_CHAIN_PROMPT)
    # qa_chain = RetrievalQA.from_chain_type(llm,retriever=VectorStore.as_retriever(search_kwargs={'k': 2}),chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}, return_source_documents=True)
    qa_chain = RetrievalQA.from_chain_type(llm,retriever=VectorStore.as_retriever(search_kwargs={'k': 2}),chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}, return_source_documents=True)
    result = qa_chain({"query": question})
    print(result)
    # print(result)
    # print(result["result"])
    return result['result']