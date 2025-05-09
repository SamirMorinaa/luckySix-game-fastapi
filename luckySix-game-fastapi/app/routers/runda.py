import random
from ..models import Runda as RundaModel
from ..database import SessionLocal

def izvuci_brojeve():
    """Function that creates a new round, generates 35 numbers, and saves them to the database."""
    # Generate 35 unique numbers between 1 and 48
    brojevi = random.sample(range(1, 49), 35)
    print("Generated numbers for the round:", brojevi)
    
    # Create a new round and save it to the database
    db = SessionLocal()
    try:
        nova_runda = RundaModel(izvuceni_brojevi=",".join(map(str, brojevi)))
        db.add(nova_runda)
        db.commit()
        db.refresh(nova_runda)
        print(f"Created a new round with ID: {nova_runda.id}")
    finally:
        db.close()
    
    return brojevi
