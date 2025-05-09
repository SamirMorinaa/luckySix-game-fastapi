from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from decimal import Decimal
import datetime

Base = declarative_base()

class Listic(Base):
    __tablename__ = 'listici'

    id = Column(Integer, primary_key=True, index=True)
    numbers = Column(String, index=True)  # Numbers will be stored as a string (e.g., "1,2,3,4,5,6")
    uplata = Column(Float)  # Bet amount will be stored as a decimal number
    time_and_date = datetime.datetime.now()  # Time and date when the ticket was created
    dobitak = Column(Float, default=0.0)  # Winnings for the ticket
    runda_id = Column(Integer)  # ID of the associated round
    proknjizeno = Column(Boolean, default=False)  # False - not processed, True - processed


class Runda(Base):
    __tablename__ = 'runde'

    id = Column(Integer, primary_key=True, index=True)
    izvuceni_brojevi = Column(String)  # Similarly, numbers will be stored as a string


