from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    divers = relationship("Diver", back_populates="group")
