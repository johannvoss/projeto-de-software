"""Entidades persistidas no SQLite do MVP Anjos da Noite."""
from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def agora_utc():
    # SQLite trabalha com datas sem fuso; usamos UTC de forma consistente.
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Base(DeclarativeBase):
    pass


class Voluntario(UserMixin, Base):
    __tablename__ = "voluntarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    tentativas_falhas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    bloqueado_ate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    doacoes: Mapped[list["Doacao"]] = relationship(back_populates="voluntario")
    marmitas: Mapped[list["Marmita"]] = relationship(back_populates="voluntario")


class Doacao(Base):
    __tablename__ = "doacoes"
    __table_args__ = (CheckConstraint("quantidade > 0", name="ck_doacao_quantidade_positiva"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    alimento: Mapped[str] = mapped_column(String(120), nullable=False)
    quantidade: Mapped[float] = mapped_column(Float, nullable=False)
    data_doacao: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=agora_utc)
    voluntario_id: Mapped[int] = mapped_column(ForeignKey("voluntarios.id"), nullable=False)

    voluntario: Mapped[Voluntario] = relationship(back_populates="doacoes")


class Marmita(Base):
    __tablename__ = "marmitas"
    __table_args__ = (
        CheckConstraint("quantidade_produzida >= 0", name="ck_marmita_produzida"),
        CheckConstraint("quantidade_distribuida >= 0", name="ck_marmita_distribuida"),
        CheckConstraint("quantidade_distribuida <= quantidade_produzida", name="ck_marmita_limite"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    quantidade_produzida: Mapped[int] = mapped_column(Integer, nullable=False)
    quantidade_distribuida: Mapped[int] = mapped_column(Integer, nullable=False)
    data_registro: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=agora_utc)
    voluntario_id: Mapped[int] = mapped_column(ForeignKey("voluntarios.id"), nullable=False)

    voluntario: Mapped[Voluntario] = relationship(back_populates="marmitas")
