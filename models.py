from sqlalchemy import Column, Integer, String, LargeBinary
from db import Base

class Destination(Base):
   __tablename__ = "destinations"

   id = Column(Integer, primary_key=True)
   name = Column(String)
   country = Column(String)
   description = Column(String)
   category = Column(String)
   embedding = Column(LargeBinary)