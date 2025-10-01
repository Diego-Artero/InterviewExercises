from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text

class Car(BaseModel):
    model: str
    year: int
    price: float
    transmission: str
    mileage: int
    fueltype: str
    tax: int
    mpg: float
    enginesize: float
    manufacturer: str
    car_age: int
    price_per_engine: float

app = FastAPI()


engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/carsdb")

@app.get("/cars")
def get_cars():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM cars"))
        return [dict(row) for row in result]

@app.post("/cars")
def add_car(car: Car):
    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO cars 
                (model, year, price, transmission, mileage, fueltype, tax, mpg, enginesize, manufacturer, car_age, price_per_engine)
                VALUES (:model, :year, :price, :transmission, :mileage, :fueltype, :tax, :mpg, :enginesize, :manufacturer, :car_age, :price_per_engine)
            """), car.model_dump()
        )
        conn.commit()
    return {"message": "Car added successfully!"}

@app.put("/cars/{car_id}")
def update_car(car_id: int, car: Car):
    with engine.connect() as conn:
        conn.execute(
            text("""
                UPDATE cars SET
                model=:model, year=:year, price=:price, transmission=:transmission,
                mileage=:mileage, fueltype=:fueltype, tax=:tax, mpg=:mpg,
                enginesize=:enginesize, manufacturer=:manufacturer, car_age=:car_age, price_per_engine=:price_per_engine
                WHERE id=:id
            """), {**car.model_dump(), "id": car_id}
        )
        conn.commit()
    return {"message": "Car updated successfully!"}

@app.delete("/cars/{car_id}")
def delete_car(car_id: int):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM cars WHERE id=:id"), {"id": car_id})
        conn.commit()
    return {"message": "Car deleted successfully!"}
