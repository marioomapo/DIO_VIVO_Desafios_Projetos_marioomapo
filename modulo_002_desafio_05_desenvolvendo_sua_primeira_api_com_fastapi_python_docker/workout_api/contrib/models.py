from uuid import uuid4
from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID # importando para tipagem


# classe Pai que os outros models irão herdar dela
class BaseModel(DeclarativeBase):
    # este campo padrão haverá em todas
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, mullable=False)
    # Mapped[] => recurso nodo do SQLAlchemy
    # mapped_column => recurso para criar colunas no banco de dados
    # importando para a tipagem 