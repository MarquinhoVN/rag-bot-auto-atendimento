import os
from decouple import config
from langchain_groq import ChatGroq

os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')

class StructuredLLM:

    def __init__(self):
        self.__chat = ChatGroq(model=os.environ['LLAMA_V'])

    def ask(self, prompt: str) -> str:
        """
        Envia um prompt direto para o modelo sem RAG, sem contexto,
        sem histórico — ideal para JSON, parsing e tarefas estruturadas.
        """
        response = self.__chat.invoke(prompt)
        
        return response.content


structured_llm = StructuredLLM()
