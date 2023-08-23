from sqlalchemy import Column, String

from app import db
from app.models.base_model import BaseModel
from app.models.poem import poem_theme


class Theme(BaseModel, db.Model):
    __tablename__ = "themes"

    name = Column(String(100), nullable=False)

    poem_themes = db.relationship("Poem", secondary=poem_theme)
