from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

import models
from database import engine, get_db

# Create DB tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flava Delivery Backend API")

@app.get("/api/shops", status_code=200)
def search_and_filter_shops(
    # 1. Define query parameters for searching and filtering
    search: Optional[str] = Query(None, description="Search keyword for shop name or description"),
    category: Optional[str] = Query(None, description="Filter exactly by category"),
    city: Optional[str] = Query(None, description="Filter exactly by city location"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),

    db: Session = Depends(get_db)
):
    # Initialize a base query object
    query = db.query(models.Shop)

    # Dynamic list to hold our query conditions
    conditions = []

    # ---- SEARCH LOGIC ----
    # SQLite LIKE is case-insensitive by default for ASCII characters.
    # We use `func.lower()` to guarantee bulletproof case-insensitive matching.
    if search:
        search_term = f"%{search.lower()}%"
        conditions.append(
            (func.lower(models.Shop.name).like(search_term)) | 
            (func.lower(models.Shop.description).like(search_term))
        )

    # ---- FILTERING LOGIC ----
    if category:
        conditions.append(models.Shop.category == category)

    if city:
        conditions.append(models.Shop.city == city)

    if is_active is not None:
        conditions.append(models.Shop.is_active == is_active)

    # Apply all filtered conditions dynamically using unpacking (*)
    if conditions:
        query = query.filter(*conditions)

    # Execute query
    results = query.all()

    return {
        "success": True,
        "count": len(results),
        "data": results
    }