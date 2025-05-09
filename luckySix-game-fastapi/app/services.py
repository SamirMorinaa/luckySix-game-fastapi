import random
from .models import Listic as ListicModel, Runda as RundaModel
from sqlalchemy.orm import Session

def create_listic(numbers: list[int] = None, uplata: float = 1.0, db: Session = None) -> ListicModel:
    """Function to create a ticket in the database"""
    
    # Check the minimum bet amount
    if uplata < 1:
        raise ValueError("The minimum bet is 1.")
    
    # If numbers are not provided, generate 6 random numbers
    if not numbers:
        numbers = random.sample(range(1, 49), 6)  # Generate 6 unique numbers between 1 and 48
    
    # Check if the number of numbers is between 6 and 8
    if len(numbers) < 6 or len(numbers) > 8:
        raise ValueError("The ticket must contain 6, 7, or 8 numbers.")
    
    # Find the round with the highest ID
    poslednja_runda = db.query(RundaModel).order_by(RundaModel.id.desc()).first()
    if poslednja_runda:
        id_nove_runde = poslednja_runda.id + 1
    else:
        id_nove_runde = 1  # If there are no rounds, set the ID to 1
    
    # Create a ticket and associate it with the new round ID
    db_listic = ListicModel(numbers=",".join(map(str, numbers)), uplata=uplata, runda_id=id_nove_runde)
    db.add(db_listic)
    db.commit()
    db.refresh(db_listic)
    return db_listic