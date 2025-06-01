from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Diver(Base):
    __tablename__ = "divers"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    contact_info = Column(String)
    bpm = Column(Integer)
    entry_point = Column(String)
    current_depth = Column(Float)
    status = Column(String)

    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", back_populates="divers")