import json
import re
from datetime import datetime
from dateutil.parser import parse as date_parse
from bot.reservation.llm import structured_llm

def parse_date_or_none(value):
    try:
        return date_parse(value, dayfirst=True).date()
    except:
        return None

def extract_fields_with_llm(message, current_data, current_step):
    cleaned = message.strip().lower()

    if cleaned.isdigit():
        number = int(cleaned)
        if len(cleaned) >= 10:
            return {"contact": cleaned}
        if 1 <= number <= 10:
            return {"quantity": number}

    prompt = f"""
        Extraia somente os campos abaixo da mensagem do usuário.
        Retorne SOMENTE um JSON válido.

        Campos possíveis:
        - name
        - contact
        - check_in_date
        - check_out_date
        - quantity

        Regras:
        - Se estiver pedindo check_in_date, NÃO retorne check_out_date.
        - Se estiver pedindo check_out_date, NÃO retorne check_in_date.
        - Quantity deve ser inteiro até 10.
        - Se não houver campo identificável, retorne {{}}.

        Mensagem: "{message}" 
        Passo atual: {current_step}
        Dados atuais: {current_data}
    """

    response = structured_llm.ask(prompt)
    print(message)
    print(response)
    try:
        data = json.loads(response)
    except:
        match = re.search(r"\{.*\}", response, flags=re.DOTALL)
        if not match:
            return {}
        try:
            data = json.loads(match.group(0))
        except:
            return {}

    if "check_out_date" in data and current_data.get("check_in_date"):
        check_in = current_data["check_in_date"]
        if isinstance(check_in, str):
            check_in = parse_date_or_none(check_in)

        check_out = data["check_out_date"]
        if isinstance(check_out, str):
            check_out = parse_date_or_none(check_out)

        if not check_out or not check_in:
            return {"__error__": "A data informada é inválida. Use algo como 10/02."}
        if check_out <= check_in:
            return {"__error__": "A data de saída deve ser posterior à data de entrada."}

    return data
