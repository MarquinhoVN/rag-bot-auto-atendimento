import os

from decouple import config

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings


os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')


class AIBot:

    def __init__(self):
        self.__chat = ChatGroq(model=os.environ['LLAMA_V'])
        self.__retriever = self.__build_retriever()

    def __build_retriever(self):
        persist_directory = '/api/chroma_data'
        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding,
        )
        n_docs = len(vector_store._collection.get()['ids'])
        k = min(30,n_docs)
        return vector_store.as_retriever(
            search_kwargs={'k': k},
        )

    def __build_messages(self, history_messages, question):
            
        messages = []
        for user_msg, ai_msg in history_messages:
            if user_msg:
                messages.append(HumanMessage(content=user_msg))
            if ai_msg:
                messages.append(AIMessage(content=ai_msg))

        messages.append(HumanMessage(content=question))
        return messages

    def invoke(self, history_messages, question):
        SYSTEM_TEMPLATE = '''
        Você é um atendente virtual de um hotel, responsável por tirar dúvidas de possíveis hóspedes.  
        Responda sempre com simpatia, respeito e clareza, de forma natural e objetiva — como em um diálogo entre duas pessoas.

        IMPORTANTE: 
        - NÃO traduza conteúdos automaticamente.  
        - Responda **apenas com base no contexto fornecido** abaixo, sem inventar informações externas.  
        - Use frases curtas, diretas, e fáceis de entender.  
        - Se necessário, inicie um novo tópico com naturalidade.
        - A linguagem da conversa é: Português BR. Responda apenas nesta linguagem.
        - Dê respostas curtas        

        <context>
        {context}
        </context>
        '''

        docs = self.__retriever.invoke(question)

        question_answering_prompt = ChatPromptTemplate.from_messages(
            [
                ('system', SYSTEM_TEMPLATE),
                MessagesPlaceholder(variable_name='messages'),
            ]
        )
        document_chain = create_stuff_documents_chain(self.__chat, question_answering_prompt)
        response = document_chain.invoke({
            'context': docs,
            'messages': self.__build_messages(history_messages, question)
        })
        
        return response
