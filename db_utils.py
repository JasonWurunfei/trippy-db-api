from os import name
import sqlite3
from typing import List, Tuple, Generic, TypeVar
from data import *
import random

DB_PATH = 'trippy.db'
DataT = TypeVar("DataT")

def db_get_info(info_name: str) -> str:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            select info_content from info 
            where info_name=:name
        """, {"name": info_name})
        return cur.fetchone()[0]


def tuple_to_dataclass(tuple: Tuple, dataT: Generic[DataT]) -> DataT:
    '''Convert a dataset to a dict'''
    if tuple is None:
        return
    field_keys = dataT.__fields__.keys()
    d = {}
    for i, key in enumerate(field_keys):
        if i < len(tuple):
            d.update({key: tuple[i]})
    d = dataT.parse_obj(d)
    return d


def db_get_attachment_by_id(
    cur: sqlite3.Cursor,
    attachment_id: int, 
    attachment: Attachment) -> Attachment:
    '''use the foreign key to get related data'''
    cur.execute(f"""
        SELECT * FROM {attachment.name} WHERE id=:attachment_id 
        LIMIT 1
    """, {"attachment_id": attachment_id})
        
    return tuple_to_dataclass(cur.fetchone(), attachment.value)


def db_get_hotel_by_id(id: int) -> Hotel:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        return db_get_attachment_by_id(cur, id, Attachment.hotel)


def db_get_guide_by_id(id: int) -> Guide:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        return db_get_attachment_by_id(cur, id, Attachment.guide)


def db_get_car_rental_by_id(id: int) -> CarRental:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        return db_get_attachment_by_id(cur, id, Attachment.car_rental)


def db_get_attachment_by_package(
    cur: sqlite3.Cursor,
    package: Package,
    attachment: Attachment) -> Attachment:
    '''use the foreign key to get related data'''
    return db_get_attachment_by_id(
        cur, package.__getattribute__(attachment.name+"_id"), attachment)


def set_package_attachment(
    package: Package, cur: sqlite3.Cursor) -> None:
    package.hotel = db_get_attachment_by_package(cur, package, Attachment.hotel)
    package.guide = db_get_attachment_by_package(cur, package, Attachment.guide)
    package.car_rental = db_get_attachment_by_package(cur, package, Attachment.car_rental)


def db_get_popular_packages(limit: int=3) -> List[Package]:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM package 
            Order by num_of_sales DESC 
            LIMIT :limit
        """, {"limit": limit})
        packages = []
        for res in cur.fetchall():
            obj = tuple_to_dataclass(res, Package)
            set_package_attachment(obj, cur)
            packages.append(obj)
        return packages


def db_get_packages_by_country(country: str) -> List[Package]:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM 'package' where country=:country
        """, {"country": country})

        packages = []
        for res in cur.fetchall():
            obj = tuple_to_dataclass(res, Package)
            set_package_attachment(obj, cur)
            packages.append(obj)
        return packages

def db_get_packages_by_destination(destination: str) -> List[Package]:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM 'package' where destination=:destination
        """, {"destination": destination})

        packages = []
        for res in cur.fetchall():
            obj = tuple_to_dataclass(res, Package)
            set_package_attachment(obj, cur)
            packages.append(obj)
        return packages

def db_get_hotels_by_destination(destination: str) -> List[Hotel]:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM hotel WHERE destination=:destination 
        """, {"destination": destination})
        hotels = []
        for res in cur.fetchall():
            hotel = tuple_to_dataclass(res, Hotel)
            hotels.append(hotel)
        return hotels


def db_get_restaurants_by_destination(destination: str) -> List[Restaurant]:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM restaurant WHERE destination=:destination 
        """, {"destination": destination})
        restaurants = []
        for res in cur.fetchall():
            restaurant = tuple_to_dataclass(res, Restaurant)
            restaurants.append(restaurant)
        return restaurants


def get_available_guide(old_guide_name: str) -> Guide:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM guide")
        guides = []
        for res in cur.fetchall():
            guide = tuple_to_dataclass(res, Guide)
            if guide.name != old_guide_name:
                guides.append(guide)

        if len(guides) == 0:
            return None
        
        return random.sample(guides, 1)[0]


def get_nearest_restaurant(
    destination: str, 
    old_restaurant_name: str) -> Restaurant:

    restaurants = db_get_restaurants_by_destination(destination)
    restaurants = [
        restaurant for restaurant in restaurants \
            if restaurant.name != old_restaurant_name
    ]
    if len(restaurants) == 0:
        return None
    return random.sample(restaurants, 1)[0]


def create_user(username: str, password: str) -> User:
    u = User.parse_obj({
        "name": username
    })
    u.generate_password_key(password)
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            insert into user (name, password_key, salt) 
            values (:name, :password_key, :salt)
        """, {"name": u.name, "password_key":u.password_key, "salt": u.salt})
        conn.commit()
        return u


def get_user_by_name(username: str) -> User:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor() 
        cur.execute("""
            SELECT * FROM user WHERE name=:username
        """, {"username": username})
        res = cur.fetchone()
        user = tuple_to_dataclass(res, User)
        return user


def validate_user_password(username: str, target_password: str) -> bool:
    user = get_user_by_name(username)
    return user.validate_key(target_password)


def create_order(username: str, package_id: int) -> Order:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor() 
        cur.execute("""
            insert into 'order' (username, package_id) 
            values (:username, :package_id)
        """, {"username": username, "package_id":package_id})
        conn.commit()
        return Order(username=username, package_id=package_id)


def get_packages_by_username(username: str) -> List[Package]:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor() 
        cur.execute("""
            SELECT 'package'.*
            FROM 'order' JOIN 'package' ON 'order'.package_id='package'.id
            WHERE 'order'.username=:username
        """, {"username": username})
        packages = []
        for res in cur.fetchall():
            obj = tuple_to_dataclass(res, Package)
            set_package_attachment(obj, cur)
            packages.append(obj)
        return packages


def delete_order(username: str, package_id: int) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor() 
        cur.execute("""
            DELETE FROM 'order' 
            WHERE username=:username and package_id=:package_id
        """, {'username': username, 'package_id': package_id})
        rows_affected = cur.rowcount
        conn.commit()
        return rows_affected



if __name__ == "__main__":
    delete_order("Jason", 2)
