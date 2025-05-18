from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


db = SQLAlchemy()

user_planets=db.Table(
    'user_planets', db.metadata, 
    db.Column('user.id', Integer, ForeignKey('users.id'), primary_key=True),
    db.Column('planet.id', Integer, ForeignKey('planets.id'), primary_key=True)
)

user_characters=db.Table(
    'user_characters', db.metadata,
    db.Column('user.id', Integer, ForeignKey('users.id'), primary_key=True),
    db.Column('character.id', Integer, ForeignKey('characters.id'), primary_key=True)
)

class User(db.Model):
    __tablename__='users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(120))


    favorite_planets:Mapped[List["Planet"]] = relationship("Planet", secondary=user_planets, back_populates="users_who_favorited")
    favorite_characters: Mapped[List["Character"]] = relationship("Character", secondary=user_characters, back_populates="users_who_favorited")

    posts:Mapped[List["Post"]] = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author", cascade="all, delete-orphan")



    def serialize(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "first_name": self.first_name,
            "last_name": self.last_name
        }


class Planet(db.Model):
    __tablename__= 'planets'
    id:  Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    climate: Mapped[str] = mapped_column(String(100))
    terrain: Mapped[str] = mapped_column(String(100))
    population: Mapped[str] = mapped_column(String(100))

    residents: Mapped[List["Character"]] = relationship("Character", back_populates="home_planet", cascade="all, delete-orphan")
    users_who_favorite:Mapped[List["User"]] = relationship ("User", secondary="user_planet", back_populates= "favorite_planets") 




    def serialize(self)-> dict:
        return{
            "id" :self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain" : self.terrain,
            "population": self.population
        }

class Character(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    gender: Mapped[str] = mapped_column(String(30))
    birth_day: Mapped[str] = mapped_column(String(50))
    species: Mapped[str] = mapped_column(String(50))
    height: Mapped[str] = mapped_column(String(30))
    mass: Mapped[str] = mapped_column(String(30))
    planet_id: Mapped[int] = mapped_column(Integer, ForeignKey('planets.id'))


    home_planet:Mapped["Planet"] = relationship("Planet", back_populates="residents")
    users_who_favorite:Mapped[List["User"]]= relationship("User", secondary=user_characters, back_populates="favorite_characters" )



    def serialize(self) -> dict: 
        return{
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_day": self.birth_day,
            "species": self.species,
            "height": self.height,
            "mass": self.mass,
            "planet_id": self.planet_id
        }


class Post(db.Model):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable= False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    author:Mapped[List["User"]] = relationship("User", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="posts", cascade="all, delete-orphan")




    def serialize(self)-> dict:
        return{
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id
        }


class Comment(db.Model):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'), nullable= False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    post: Mapped[List["Post"]] = relationship("Post", back_populates="comments")
    author: Mapped[List["User"]]= relationship("User", back_populates="comments")



    def serialize(self)-> dict:
        return{
            "id": self.id,
            "content": self.content,
            "post_id": self.post_id,
            "user_id": self.user_id
        }
    
