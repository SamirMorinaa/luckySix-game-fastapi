from pydantic import BaseModel
from typing import List,Optional
import decimal

class Listic(BaseModel):
    numbers: List[int]
    id: int
    uplata: float
    runda_id: int

    class Config:
        orm_mode = True  # Omogućava da Pydantic model bude kompatibilan s SQLAlchemy modelima

class ListicCreate(BaseModel):
    numbers: Optional[List[int]] = None  # Brojevi su opcioni (mogu se generisati)
    uplata: float

class Runda(BaseModel):
    izvuceni_brojevi: List[int]

    class Config:
        orm_mode = True  # Omogućava da Pydantic model bude kompatibilan s SQLAlchemy modelima

class PlayResponse(BaseModel):
    listic: Listic
    runda: Runda
    pogodjeni: List[int]
    broj_pogodaka: int
    osvojeni_iznos: float
    detalji_dobitaka: Optional[List[dict]] = None  # Detalji dobitaka samo za listiće sa 7 brojeva
    

