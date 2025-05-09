from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Listic as ListicModel, Runda as RundaModel
from ..schemas import Listic, Runda, PlayResponse
from ..services import create_listic
from ..database import SessionLocal
from .runda import izvuci_brojeve as izvuci
from itertools import combinations

router = APIRouter()

def get_db():
    """Provide a database session for dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/provjeri-listic/{listic_id}", response_model=PlayResponse)
def provjeri_listic(listic_id: int, db: Session = Depends(get_db)):
    """
    Check the winnings for a ticket based on its ID and the associated round.
    """
    # Find the ticket in the database
    listic = db.query(ListicModel).filter(ListicModel.id == listic_id).first()
    if not listic:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    
    # Find the round associated with the ticket
    runda = db.query(RundaModel).filter(RundaModel.id == listic.runda_id).first()
    if not runda or not runda.izvuceni_brojevi:
        raise HTTPException(status_code=400, detail="The round for this ticket is not yet completed.")
    
    # Convert the drawn numbers to a list
    izvuceni_brojevi = list(map(int, runda.izvuceni_brojevi.split(",")))
    
    # Convert the ticket numbers to a list
    brojevi_listica = list(map(int, listic.numbers.split(",")))
    
    detalji_dobitaka = []
    pogodjeni = []
    broj_pogodaka = 0
    osvojeni_iznos = 0

    if len(brojevi_listica) == 6:
        # Standard processing
        pogodjeni = [broj for broj in brojevi_listica if broj in izvuceni_brojevi]
        broj_pogodaka = len(pogodjeni)
        zadnji_pogodak = None

        if broj_pogodaka == 6:
            indeksi = [izvuceni_brojevi.index(broj) for broj in pogodjeni]
            indeks_zadnjeg = max(indeksi)
            zadnji_pogodak = izvuceni_brojevi[indeks_zadnjeg]

            if indeks_zadnjeg >= 5:
                koef = calculate_win_amount(zadnji_pogodak, izvuceni_brojevi)
                osvojeni_iznos = koef * float(listic.uplata)

    elif len(brojevi_listica) == 7:
        # System processing for 7 numbers (6 out of 7 system)
        kombinacije_listica = list(combinations(brojevi_listica, 6))
        ulog_po_kombinaciji = float(listic.uplata) / len(kombinacije_listica)
        ukupni_dobitak = 0
        ukupni_pogodjeni = set()

        for kombinacija in kombinacije_listica:
            pogodjeni_komb = [broj for broj in kombinacija if broj in izvuceni_brojevi]
            ukupni_pogodjeni.update(pogodjeni_komb)
            if len(pogodjeni_komb) == 6:
                indeksi = [izvuceni_brojevi.index(broj) for broj in pogodjeni_komb]
                indeks_zadnjeg = max(indeksi)
                zadnji = izvuceni_brojevi[indeks_zadnjeg]

                if indeks_zadnjeg >= 5:
                    koef = calculate_win_amount(zadnji, izvuceni_brojevi)
                    dobitak = round(ulog_po_kombinaciji * koef, 2)
                    ukupni_dobitak += dobitak

                    detalji_dobitaka.append({
                        "kombinacija": kombinacija,
                        "zadnji_pogodjeni": zadnji,
                        "koeficijent": koef,
                        "dobitak": dobitak
                    })

        pogodjeni = list(ukupni_pogodjeni)
        broj_pogodaka = len(pogodjeni)
        osvojeni_iznos = round(ukupni_dobitak, 2)

    else:
        raise HTTPException(status_code=400, detail="The ticket must contain 6 or 7 numbers.")
    
    # Update the winnings in the database
    listic.dobitak = osvojeni_iznos
    db.commit()
    db.refresh(listic)
    
    # Convert SQLAlchemy objects to Pydantic models
    listic_schema = Listic(
        id=listic.id,  # Include the ID field
        numbers=brojevi_listica,
        uplata=float(listic.uplata),
        runda_id=listic.runda_id
    )
    runda_schema = Runda(
        izvuceni_brojevi=izvuceni_brojevi
    )
    
    # Create the response
    return PlayResponse(
        listic=listic_schema,
        runda=runda_schema,
        pogodjeni=pogodjeni,
        broj_pogodaka=broj_pogodaka,
        osvojeni_iznos=osvojeni_iznos,
        detalji_dobitaka=detalji_dobitaka if len(brojevi_listica) == 7 else None
    )


# Function to calculate winnings based on the position of the last matched number
def calculate_win_amount(zadnji_pogodak: int, izvuceni_brojevi: list):
    kvote = [
        10000, 7500, 5000, 2500, 1000, 500, 300, 200, 150, 100, 90, 80, 70, 60, 50, 40,
        30, 25, 20, 15, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1
    ]

    try:
        pozicija = izvuceni_brojevi.index(zadnji_pogodak)
        if pozicija >= 5:
            return kvote[pozicija - 5]
        else:
            return 0
    except ValueError:
        return 0
