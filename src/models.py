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

    # Corregido: "usuario" (singular) para que coincida con el atributo en Favorito
    favoritos: Mapped[List["Favorito"]] = relationship(back_populates="usuario")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            # ¡Nunca serializamos el password por seguridad!
        }

class Personaje(db.Model):
    __tablename__ = "personajes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(50))
    gender: Mapped[str] = mapped_column(String(50))
    eye_color: Mapped[str] = mapped_column(String(50))

    # Corregido: "personaje"
    favoritos: Mapped[List["Favorito"]] = relationship(back_populates="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "eye_color": self.eye_color
        }

class Planeta(db.Model):
    __tablename__ = "planetas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(50))
    terrain: Mapped[str] = mapped_column(String(50))
    population: Mapped[str] = mapped_column(String(50))

    # Corregido: "planeta"
    favoritos: Mapped[List["Favorito"]] = relationship(back_populates="planeta")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }

class Favorito(db.Model):
    __tablename__ = "favoritos"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    personaje_id: Mapped[Optional[int]] = mapped_column(ForeignKey("personajes.id"), nullable=True)
    planeta_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planetas.id"), nullable=True)

    usuario: Mapped["Usuario"] = relationship(back_populates="favoritos")
    personaje: Mapped[Optional["Personaje"]] = relationship(back_populates="favoritos")
    planeta: Mapped[Optional["Planeta"]] = relationship(back_populates="favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "personaje_id": self.personaje_id,
            "planeta_id": self.planeta_id,
            # Opcional: puedes traer la información anidada si lo deseas
            "planeta_name": self.planeta.name if self.planeta else None,
            "personaje_name": self.personaje.name if self.personaje else None
        }