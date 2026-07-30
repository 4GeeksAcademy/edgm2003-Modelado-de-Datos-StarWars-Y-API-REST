from flask_sqlalchemy import SQLAlchemy
from typing import List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)

    favoritos: Mapped[List["Favorito"]] = relationship(back_populates="usuarios")

class Personaje(db.Model):
    __tablename__ = "personajes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(50))
    gender: Mapped[str] = mapped_column(String(50))
    eye_color: Mapped[str] = mapped_column(String(50))

    favoritos: Mapped[List["Favorito"]] = relationship(back_populates="personajes")

class Planeta(db.Model):
    __tablename__ = "planetas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(50))
    terrain: Mapped[str] = mapped_column(String(50))
    population: Mapped[str] = mapped_column(String(50))

    favoritos: Mapped[List["Favorito"]] = relationship(back_populates="planetas")

class Favorito(db.Model):
    __tablename__ = "favoritos"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)

    personaje_id: Mapped[Optional[int]] = mapped_column(ForeignKey("personajes.id"), nullable=True)
    planeta_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planetas.id"), nullable=True)

    usuario: Mapped["Usuario"] = relationship(back_populates="favoritos")
    personaje: Mapped[Optional["Personaje"]] = relationship(back_populates="favoritos")
    planeta: Mapped[Optional["Planeta"]] = relationship(back_populates="favoritos")