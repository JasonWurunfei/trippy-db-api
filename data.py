from pydantic import BaseModel
from typing import Optional
from enum import Enum


class CarRental(BaseModel):
    id: int
    name: str
    price: float

class Guide(BaseModel):
    id: int
    name: str
    phone_number: str
    email: str

class Hotel(BaseModel):
    id: int
    name: str
    price: float
    telephone: str
    address: str
    destination: str

class Hotel(BaseModel):
    id: int
    name: str
    price: float
    telephone: str
    address: str
    destination: str

class Restaurant(BaseModel):
    id: int
    name: str
    destination: str

class Info(BaseModel):
    info_name: str
    info_content: str

class Package(BaseModel):
    id: int
    title: str
    country: str
    destination: str
    duration: str
    price: float
    description: str
    num_of_sales: str
    hotel_id: Optional[int] = None
    guide_id: Optional[int] = None
    car_rental_id: Optional[int] = None

    hotel: Optional[Hotel] = None
    guide: Optional[Guide] = None
    car_rental: Optional[CarRental] = None

class Attachment(Enum):
    hotel = Hotel
    guide = Guide
    car_rental = CarRental

import hashlib
import os

class User(BaseModel):

    name: str
    password_key: Optional[bytes] = None
    salt: Optional[bytes] = None

    def generate_password_key(self, password: str) -> str:
        self.salt = os.urandom(32)
        self.password_key = hashlib.pbkdf2_hmac(
            'sha256', password.encode('utf-8'), self.salt, 100000)
        return self.password_key

    
    def validate_key(self, key: str) -> bool:
        return hashlib.pbkdf2_hmac(
            'sha256', key.encode('utf-8'), self.salt, 100000) \
            == self.password_key


class Order(BaseModel):
    username: str
    package_id: int
