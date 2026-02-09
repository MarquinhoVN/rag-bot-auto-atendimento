FIELD_DESCRIPTIONS = {
    "name": "nome do hóspede",
    "contact": "telefone ou WhatsApp para contato",
    "check_in_date": "data de entrada",
    "check_out_date": "data de saída",
    "room_type": "tipo de quarto desejado (ex: simples, casal, suíte, luxo, etc.)",
    "quantity": "quantidade de pessoas que vão se hospedar",
    "description": "alguma observação opcional que deseja adicionar"
}

def dynamic_question_prompt(field, context):
    return f"""
Você é um assistente educado, natural e especializado em reservas de hotel.

Ao gerar a pergunta, **nunca inicie com saudações** como "olá", "oi", "tudo bem".
Gere APENAS a pergunta direta.

Campo atual: {field}
Significado do campo: {FIELD_DESCRIPTIONS.get(field, field)}
Contexto da conversa: {context}

Gere uma pergunta curta, direta e amigável.
"""
