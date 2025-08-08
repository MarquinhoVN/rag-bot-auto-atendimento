# Sistema de Atendimento Automatizado via Whatsapp

Este projeto consiste no desenvolvimento de um sistema de atendimento automatizado utilizando **Processamento de Linguagem Natural (PLN)** e técnicas de **Geração Aumentada por Recuperação (RAG)**, implementado por meio de um bot no **Whatsapp**. O objetivo é oferecer respostas contextualizadas a partir da identificação de intenções e da extração de informações de **documentos institucionais**, como PDFs, manuais e bases internas.

---

## Funcionalidades

- Identificação da intenção do usuário via PLN (ex: solicitação de reserva).
- Geração de respostas com base em arquivos institucionais usando RAG.
- Interface com usuários por meio do Telegram Bot API.
- Armazenamento e consulta de logs de interação.

---

## Tecnologias Utilizadas

- **Python**
- **Transformers (Hugging Face)**
- **LangChain / Groq (LLAMA) / RAG**
- **Evolution API** (API para whatsapp)
- **ChromaDB** (para banco vetorial)
- **Flask** (para serviços locais, se necessário)

---

## ⚙️ .ENV para rodar o projeto
```# EVO-GLOBAL-API-KEY
AUTHENTICATION_API_KEY=

# EVO-DP
DATABASE_ENABLED=true
DATABASE_PROVIDER=
DATABASE_CONNECTION_URI=
DATABASE_CONNECTION_CLIENT_NAME=
DATABASE_SAVE_DATA_INSTANCE=true
DATABASE_SAVE_DATA_NEW_MESSAGE=true
DATABASE_SAVE_MESSAGE_UPDATE=true
DATABASE_SAVE_DATA_CONTACTS=true
DATABASE_SAVE_DATA_CHATS=true
DATABASE_SAVE_DATA_LABELS=true
DATABASE_SAVE_DATA_HISTORIC=true

# EVO-REDIS
CACHE_REDIS_ENABLED=true
CACHE_REDIS_URI=
CACHE_REDIS_PREFIX_KEY=
CACHE_REDIS_SAVE_INSTANCES=false
CACHE_LOCAL_ENABLED=false


# Atualizar de acordo com a versão do whatsapp: https://wppconnect.io/5241253647586979438ytr4e3w2q/whatsapp-versions/
CONFIG_SESSION_PHONE_VERSION=

# POSTGRESS-CREDENTIALS
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=


# GROQ
GROQ_API_KEY=''

# HUGGINGFACE
HUGGINGFACE_API_KEY=''

# LLAMA-V
LLAMA_V=''
```

