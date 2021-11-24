import sqlite3
from typing import List, Optional
from fastapi import FastAPI, status, Response, Query
from pydantic.main import BaseModel
from db_utils import (
    db_get_info, 
    db_get_popular_packages, 
    db_get_packages_by_country,
    get_available_guide,
    get_nearest_restaurant,
    create_user,
    get_packages_by_username,
    create_order,
    delete_order,
    validate_user_password,
    db_get_packages_by_destination,
    get_available_hotel,
    get_available_flight,
    get_user,
    get_user_order,
    change_user_guide,
    change_user_hotel,
    change_user_flight,
    get_package_id_by_destination,
)
from data import Order

app = FastAPI()


class UserForm(BaseModel):
    username: str
    password: str


@app.get("/info/company")
async def company_info():
    return {"info": db_get_info("company_info")}

@app.get("/info/contact")
async def company_info():
    return {"contact": db_get_info("company_contact")}

@app.get("/package/popular")
async def popular_packages(batch: Optional[int] = 4, showed_package_ids: Optional[List[int]] = Query(None)):
    if showed_package_ids is None:
        showed_package_ids = []
    return {"packages": db_get_popular_packages(batch, showed_package_ids)}

@app.get("/package/country")
async def query_packages_by_country(country: str):
    return {"packages": db_get_packages_by_country(country)}

@app.get("/package/destination")
async def query_packages_by_destination(destination: str):
    return {"package": db_get_packages_by_destination(destination)}

@app.get("/guide/available")
async def available_guide(undesired_guide_ids: Optional[List[int]] = Query(None)):
    if undesired_guide_ids is None:
        undesired_guide_ids = []
    return {"new_guide": get_available_guide(undesired_guide_ids)}

@app.get("/hotel/available")
async def available_hotel(destination: str, undesired_hotel_ids: Optional[List[int]] = Query(None)):
    if undesired_hotel_ids is None:
        undesired_hotel_ids = []
    return {"new_hotel": get_available_hotel(destination, undesired_hotel_ids)}

@app.get("/flight/available")
async def available_flight(undesired_flight_ids: Optional[List[int]] = Query(None)):
    if undesired_flight_ids is None:
        undesired_flight_ids = []
    return {"new_flight": get_available_flight(undesired_flight_ids)}

@app.get("/restaurant/available")
async def change_restaurant(destination: str, old_restaurant_name: str):
    return {
        "new_restaurant": get_nearest_restaurant(
                        destination,
                        old_restaurant_name
                    )
    }

@app.get("/user/checkname")
async def check_username(username: str):
    user = get_user(username)
    if user:
        return {'result': False}
    else:
        return {'result': True}

@app.post("/user/register", status_code=status.HTTP_201_CREATED)
async def register(form: UserForm, response: Response):
    try:
        create_user(form.username, form.password)
        return {'message': f"user {form.username} is created successfully"}
    except sqlite3.IntegrityError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': f"username {form.username} already exists!"}

@app.post("/user/login")
async def login(form: UserForm, response: Response):
    if validate_user_password(form.username, form.password):
        return {'message': "login success", 'username': form.username}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': "invaild username or password!"}

@app.get("/user/orders")
async def get_user_packages(username: str):
    return {'packages': get_packages_by_username(username)}

@app.put("/user/order/guide")
async def change_order_guide(username: str, destination: str, response: Response):
    order = get_user_order(username, destination)
    if order:
        new_guide = change_user_guide(order)
        return {'message': "change success", 'new_guide': new_guide}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f"User '{username}' does not have order to {destination}."}

@app.put("/user/order/flight")
async def change_order_flight(username: str, destination: str, flight_id: int, response: Response):
    order = get_user_order(username, destination)
    if order:
        new_flight = change_user_flight(order, flight_id)
        return {'message': "change success", 'new_flight': new_flight}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f"User '{username}' does not have order to {destination}."}

@app.put("/user/order/hotel")
async def change_order_hotel(username: str, destination: str, hotel_id: int, response: Response):
    order = get_user_order(username, destination)
    if order:
        new_hotel = change_user_hotel(order, hotel_id)
        return {'message': "change success", 'new_hotel': new_hotel}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f"User '{username}' does not have order to {destination}."}

@app.post("/order", status_code=status.HTTP_201_CREATED)
async def create_user_order(order: Order, response: Response):
    try:
        create_order(order.username, order.package_id)
        return {'message': f"user {order.username}\'s order is created successfully"}
    except sqlite3.IntegrityError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': f"user {order.username}\'s order already exists!"}

@app.delete("/order/cancel")
async def cancel_order(username: str, destination: str, response: Response):
    package_id = get_package_id_by_destination(destination)
    if delete_order(username, package_id):
        return {'message': f"Cancel successfully"}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': "order does not exist!"}
