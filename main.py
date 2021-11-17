import sqlite3
from fastapi import FastAPI, status, Response
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
    db_get_packages_by_destination
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
async def popular_packages():
    return {"packages": db_get_popular_packages()}

@app.get("/package/country")
async def query_packages_by_country(country: str):
    return {"packages": db_get_packages_by_country(country)}

@app.get("/package/destination")
async def query_packages_by_destination(destination: str):
    return {"packages": db_get_packages_by_destination(destination)}

@app.get("/guide/change")
async def change_guide(old_guide_name: str):
    return {"new_guide": get_available_guide(old_guide_name)}

@app.get("/restaurant/available")
async def change_restaurant(destination: str, old_restaurant_name: str):
    return {
        "newRestaurant": get_nearest_restaurant(
                        destination,
                        old_restaurant_name
                    )
    }

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
    return get_packages_by_username(username)

@app.post("/order", status_code=status.HTTP_201_CREATED)
async def create_user_order(order: Order, response: Response):
    try:
        create_order(order.username, order.package_id)
        return {'message': f"user {order.username}\'s order is created successfully"}
    except sqlite3.IntegrityError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': f"user {order.username}\'s order already exists!"}

@app.delete("/order/cancel")
async def cancel_order(username: str, package_id: int, response: Response):
    if delete_order(username, package_id):
        return {'message': f"Cancel successfully"}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': "order does not exist!"}
