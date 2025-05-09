from fastapi import APIRouter, HTTPException
import random

router = APIRouter()

# Mapping of numbers to colors
colors = {
    "crvena": [1, 9, 17, 25, 33, 41],
    "zelena": [2, 10, 18, 26, 34, 42],
    "plava": [3, 11, 19, 27, 35, 43],
    "ljubicasta": [4, 12, 20, 28, 36, 44],
    "smedja": [5, 13, 21, 29, 37, 45],
    "zuta": [6, 14, 22, 30, 38, 46],
    "narandzasta": [7, 15, 23, 31, 39, 47],
    "crna": [8, 16, 24, 32, 40, 48],
}

@router.get("/generisi-listic/{boja}")
def generisi_listic(boja: str):
    """
    Generiše listić sa brojevima za odabranu boju.
    """
    if boja not in colors:
        raise HTTPException(status_code=400, detail="Nepoznata boja. Dostupne boje su: " + ", ".join(colors.keys()))
    
    # Generate a ticket with 6 random numbers from the selected color
    brojevi = colors[boja]
    return {"boja": boja, "brojevi": brojevi}