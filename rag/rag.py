import os
import sys
import shutil
from decouple import config

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings

os.environ['HUGGINGFACE_API_KEY'] = config('HUGGINGFACE_API_KEY')

persist_directory = '/app/chroma_data'

if __name__ == '__main__':

    if '--reset' in sys.argv:
        if os.path.exists(persist_directory):
            shutil.rmtree(persist_directory)
            print("Banco vetorial limpo.")

    folder_path = '/app/rag/documents'
    all_docs = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            full_path = os.path.join(folder_path, filename)
            loader = PyPDFLoader(full_path)
            docs = loader.load()
            all_docs.extend(docs)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )
    chunks = text_splitter.split_documents(documents=all_docs)

    embedding = HuggingFaceEmbeddings()
    vector_store = Chroma(
        embedding_function=embedding,
        persist_directory=persist_directory,
    )
    vector_store.add_documents(documents=chunks)
