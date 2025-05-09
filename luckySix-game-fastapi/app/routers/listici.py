from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..services import create_listic
from ..schemas import Listic as ListicSchema, ListicCreate
from ..database import SessionLocal
from ..models import Listic as ListicModel
from app.routers.game import provjeri_listic  # Import the function provjeri_listic

router = APIRouter()

def get_db():
    """Provide a database session for dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/listici", response_model=ListicSchema)
def kreiraj_listic(listic: ListicCreate, db: Session = Depends(get_db)):
    """
    Route to create a ticket. The user can enter numbers or generate them randomly.
    """
    try:
        db_listic = create_listic(numbers=listic.numbers, uplata=listic.uplata, db=db)
        db_listic.numbers = list(map(int, db_listic.numbers.split(",")))
        return db_listic
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/listici", response_model=list[ListicSchema])
def get_all_listici(db: Session = Depends(get_db)):
    """
    Route to retrieve all tickets from the database.
    """
    listici = db.query(ListicModel).all()
    for listic in listici:
        listic.numbers = list(map(int, listic.numbers.split(",")))  # Convert numbers to a list of integers
    return listici

@router.get("/listici/ponovi/{listic_id}")
def ponovi_listic(listic_id: int, db: Session = Depends(get_db)):
    """
    Route to repeat a ticket. Returns the numbers and bet amount based on the ticket ID.
    """
    # Find the ticket in the database
    listic = db.query(ListicModel).filter(ListicModel.id == listic_id).first()
    if not listic:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    
    # Convert numbers from a string to a list of integers
    brojevi = list(map(int, listic.numbers.split(",")))
    
    return {
        "brojevi": brojevi,
        "uplata": listic.uplata
    }

@router.get("/listici/provjeri-neprovjerene")
def provjeri_neprovjerene_tikete(db: Session = Depends(get_db)):
    """
    Route to check all unchecked tickets.
    """
    neprovjereni_listici = db.query(ListicModel).filter(ListicModel.proknjizeno == False).all()
    checked_count = 0

    for listic in neprovjereni_listici:
        # Call the function provjeri_listic for each ticket
        try:
            provjeri_listic(listic.id, db)
            listic.proknjizeno = True  # Mark the ticket as processed
            db.commit()
            checked_count += 1
        except Exception as e:
            # If an error occurs, skip this ticket and continue
            print(f"Error checking ticket ID {listic.id}: {e}")
    return {"checked_count": checked_count}