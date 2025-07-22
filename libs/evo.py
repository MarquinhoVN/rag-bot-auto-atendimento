import requests

class EvoAPI:
    def __init__(self):
        self.__api_url = 'http://evolution-api:8080'
    def enviar_mensagem(self, instance, apikey, sender_number, message):
        url = f"{self.__api_url}/message/sendText/{instance}"

        payload = {
            "number": sender_number,
            "text": message,
            "delay": 2000,
        }
        headers = {
            "apikey": apikey,
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        return response
    
    