from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from decouple import config

INTENCOES_RESERVA = [
    "quero reservar um quarto",
    "gostaria de fazer uma reserva",
    "tem quarto disponível?",
    "posso reservar?",
    "quero um quarto",
    "tem vaga para hoje?",
    "quero fazer uma pré-reserva",
    "preciso reservar um quarto",
    "quero alugar um quarto",
    "eu gostaria de um quarto para ficar",
    "tenho interesse em reservar"
]

from langchain_groq import ChatGroq

class IntentionDetector:
    def __init__(self):
        model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.frases_embeds = [self.embeddings.embed_query(f) for f in INTENCOES_RESERVA]
        self.llm = ChatGroq(model=os.environ['LLAMA_V'])

    def detect(self, mensagem_usuario: str, threshold=0.7) -> str:
        if not mensagem_usuario:
            return "mensagem_geral"

        msg_embed = self.embeddings.embed_query(mensagem_usuario)
        scores = cosine_similarity([msg_embed], self.frases_embeds)[0]
        max_score = max(scores)

        if max_score >= threshold:
            return "pre_reserva"
        elif 0.6 <= max_score < threshold:
            prompt = f"""
            Classifique a intenção do usuário com base na mensagem abaixo:
            "{mensagem_usuario}"
            Categorias possíveis: [pre_reserva, mensagem_geral]
            Responda apenas com o nome da categoria.
            """
            resposta = self.llm.invoke(prompt)
            return resposta.content.strip().lower()
        return "mensagem_geral"
