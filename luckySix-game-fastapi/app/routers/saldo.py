from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Listic as ListicModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/saldo")
def get_saldo(db: Session = Depends(get_db)):
    """
    Ruta za izračunavanje ukupnih uplata, dobitaka i salda za sve listiće.
    """
    listici = db.query(ListicModel).all()

    ukupna_uplata = sum(float(listic.uplata) for listic in listici)
    ukupni_dobitak = sum(float(listic.dobitak) for listic in listici if hasattr(listic, 'dobitak'))
    saldo = ukupna_uplata - ukupni_dobitak

    return {
        "ukupna_uplata": round(ukupna_uplata, 2),
        "ukupni_dobitak": round(ukupni_dobitak, 2),
        "saldo": round(saldo, 2)
    }