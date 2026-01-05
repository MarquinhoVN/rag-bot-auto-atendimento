from sqlalchemy import text
from app.models.database import db

from llama_index.core import VectorStoreIndex, Document
from llama_index.core.settings import Settings

from bot.reservation.llm import structured_llm

def find_best_room(
    check_in,
    check_out,
    quantity,
    user_description: str
) -> bool:
    """
    Verifica se existe ao menos um quarto disponível que:
    - comporte a quantidade de pessoas
    - esteja disponível no período
    - seja semanticamente compatível com a descrição do usuário
    """

    engine = db.get_engine()

    sql = text("""
        SELECT
            r.id,
            r.room_number,
            r.capacity,
            r.price,
            rt.name AS room_type,
            rt.description AS room_description
        FROM hotel.room r
        INNER JOIN hotel.room_type rt ON r.room_type_id = rt.id
        WHERE r.capacity >= :quantity
        AND r.id NOT IN (
            SELECT ro.room_id
            FROM hotel.room_occupancy ro
            WHERE (
                :check_in < ro.check_out_date
                AND :check_out > ro.check_in_date
            )
        )
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, {
            "check_in": check_in,
            "check_out": check_out,
            "quantity": quantity
        }).fetchall()

    if not result:
        return False

    documents = []
    for room in rooms:
        text_content = f"""
        Tipo do quarto: {room.room_type}
        Descrição: {room.room_description}
        """
        documents.append(Document(text=text_content))

    Settings.llm = structured_llm 
    index = VectorStoreIndex.from_documents(documents)

    query_engine = index.as_query_engine(similarity_top_k=1)

    response = query_engine.query(
        f"O usuário procura um quarto com a seguinte descrição: {user_description}. "
        "Existe algum quarto compatível?"
    )

    if response and response.response.strip():
        return True

    return False