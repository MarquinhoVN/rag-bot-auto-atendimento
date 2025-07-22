from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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

class IntencaoDetector:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings()
        self.frases_embeds = [self.embeddings.embed_query(f) for f in INTENCOES_RESERVA]

    def detectar(self, mensagem_usuario: str, threshold=0.7) -> str:
        if not mensagem_usuario:
            return "mensagem_geral"
        
        msg_embed = self.embeddings.embed_query(mensagem_usuario)
        scores = cosine_similarity([msg_embed], self.frases_embeds)[0]
    
        if max(scores) >= threshold:
            return "pre_reserva"
        return "mensagem_geral"
