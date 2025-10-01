from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

# Modelo de carro
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


client = MongoClient("mongodb://localhost:27017/")
db = client["carsdb"]
collection = db["cars"]

app = FastAPI(title="Cars API - MongoDB")


def car_to_dict(car):
    car["_id"] = str(car["_id"])
    return car


@app.get("/cars")
def get_cars():
    cars = list(collection.find())
    return [car_to_dict(car) for car in cars]


@app.get("/cars/{car_id}")
def get_car(car_id: str):
    car = collection.find_one({"_id": ObjectId(car_id)})
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car_to_dict(car)


@app.post("/cars")
def add_car(car: Car):
    result = collection.insert_one(car.model_dump())
    return {"id": str(result.inserted_id)}


@app.put("/cars/{car_id}")
def update_car(car_id: str, car: Car):
    result = collection.update_one(
        {"_id": ObjectId(car_id)},
        {"$set": car.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car updated successfully"}


@app.delete("/cars/{car_id}")
def delete_car(car_id: str):
    result = collection.delete_one({"_id": ObjectId(car_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted successfully"}
