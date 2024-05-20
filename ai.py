from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
import os

def chat(text):
    WEB_SITE = "https://www.nlight.tw/pages/facts"

    llm = OpenAI()
    OPENAI_EMBEDDING_DEPLOYMENT_NAME = "text-embedding-3-small"

    loader = WebBaseLoader(WEB_SITE)

    # Document loader
    documents = loader.load()

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 100)
    docs = text_splitter.split_documents(documents)

    # Get embeddings
    embeddings = OpenAIEmbeddings(deployment = OPENAI_EMBEDDING_DEPLOYMENT_NAME, chunk_size = 1)
    vector = FAISS.from_documents(docs, embeddings)
    retriever = vector.as_retriever()

    context = []
    prompt = ChatPromptTemplate.from_messages([
        ('system', '請以 zh_TW 語系回答\'s :\n\n{context}'),
        ('user', '問題: {input}'),
    ])

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Response
    try:
        response = retrieval_chain.invoke({
          'input': text,
          'context': context
        })

        return response["answer"]
    except Exception as e:
        print(str(e))
        return os.getenv("BOT_NAME") + " 壞掉了，趕快請人類來修理: " + str(e)

