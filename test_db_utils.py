import unittest
import sqlite3
from data import CarRental, Guide, Package, Attachment, Hotel
from db_utils import *
import db_utils

DB_PATH = 'trippy.db.test'
db_utils.DB_PATH = DB_PATH

class TestDbUtils(unittest.TestCase):

    def test_tuple_to_dataclass(self):
        t = (1, 'Simply Japan', 'Japan', 'Tokyo', 15, 5214.0, "Fushimi Inari-taisha Japan.", 1000, 1, 1, 1)
        expected = Package.parse_obj({
            'id': 1, 
            'title': 'Simply Japan', 
            'country': 'Japan', 
            'destination': 'Tokyo', 
            'duration': 15, 
            'price': 5214.0, 
            'description': "Fushimi Inari-taisha Japan.", 
            'num_of_sales': 1000, 
            'hotel_id': 1, 
            'guide_id': 1, 
            'car_rental_id': 1, 
            'hotel': None,
            'guide': None, 
            'car_rental': None
        })
        actual = tuple_to_dataclass(t, Package)
        self.assertEqual(expected, actual)


    def test_db_get_hotel_by_package(self):
        package = Package.parse_obj({
            'id': 1, 
            'title': 'Simply Japan', 
            'country': 'Japan', 
            'destination': 'Tokyo', 
            'duration': 15, 
            'price': 5214.0, 
            'description': "Fushimi Inari-taisha Japan.", 
            'num_of_sales': 1000, 
            'hotel_id': 1, 
            'guide_id': 1, 
            'car_rental_id': 1, 
            'hotel': None,
            'guide': None, 
            'car_rental': None
        })
        expected = Hotel.parse_obj({
            'id': 1, 
            'name': 'Crowne Plaza', 
            'price': 100.0, 
            'telephone': '080-7977-4814', 
            'address': '高橋町井高4-9-10', 
            'destination': 'Tokyo'
        })
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            actual = db_get_attachment_by_package(cur, package, Attachment.hotel)
            self.assertEqual(actual, expected)


    def test_db_get_guide_by_package(self):
        package = Package.parse_obj({
            'id': 1, 
            'title': 'Simply Japan', 
            'country': 'Japan', 
            'destination': 'Tokyo', 
            'duration': 15, 
            'price': 5214.0, 
            'description': "Fushimi Inari-taisha Japan.", 
            'num_of_sales': 1000, 
            'hotel_id': 1, 
            'guide_id': 1, 
            'car_rental_id': 1, 
            'hotel': None,
            'guide': None, 
            'car_rental': None
        })
        expected = Guide.parse_obj({
            'id': 1, 
            'name': 'Jason', 
            'phone_number': '+86 13806889121', 
            'email': 'Jason@gmail.com'
        })
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            actual = db_get_attachment_by_package(cur, package, Attachment.guide)
            self.assertEqual(actual, expected)


    def test_db_get_car_rental_by_package(self):
        package = Package.parse_obj({
            'id': 1, 
            'title': 'Simply Japan', 
            'country': 'Japan', 
            'destination': 'Tokyo', 
            'duration': 15, 
            'price': 5214.0, 
            'description': "Fushimi Inari-taisha Japan.", 
            'num_of_sales': 1000, 
            'hotel_id': 1, 
            'guide_id': 1, 
            'car_rental_id': 1, 
            'hotel': None,
            'guide': None, 
            'car_rental': None
        })
        expected = CarRental.parse_obj({
            'id': 1, 
            'name': 'fast car rental', 
            'price': 10.0
        })
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            actual = db_get_attachment_by_package(cur, package, Attachment.car_rental)
            self.assertEqual(actual, expected)


    def test_set_package_attachment(self):
        expected = Package.parse_obj({
            'id': 1, 
            'title': 'Simply Japan', 
            'country': 'Japan', 
            'destination': 'Tokyo', 
            'duration': 15, 
            'price': 5214.0, 
            'description': "Fushimi Inari-taisha Japan.", 
            'num_of_sales': 1000, 
            'hotel_id': 1, 
            'guide_id': 1, 
            'car_rental_id': 1, 
            'hotel': None,
            'guide': None, 
            'car_rental': None
        })
        hotel = Hotel.parse_obj({
            'id': 1, 
            'name': 'Crowne Plaza', 
            'price': 100.0, 
            'telephone': '080-7977-4814', 
            'address': '高橋町井高4-9-10', 
            'destination': 'Tokyo'
        })
        guide = Guide.parse_obj({
            'id': 1, 
            'name': 'Jason', 
            'phone_number': '+86 13806889121', 
            'email': 'Jason@gmail.com'
        })
        car_rental = CarRental.parse_obj({
            'id': 1, 
            'name': 'fast car rental', 
            'price': 10.0
        })
        actual = expected.copy()
        expected.hotel = hotel
        expected.guide = guide
        expected.car_rental = car_rental
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            set_package_attachment(actual, cur)
            self.assertEqual(actual, expected)


    def test_db_get_hotel_by_id(self):
        expected = Hotel.parse_obj({
            'id': 1, 
            'name': 'Crowne Plaza', 
            'price': 100.0, 
            'telephone': '080-7977-4814', 
            'address': '高橋町井高4-9-10', 
            'destination': 'Tokyo'
        })
        actual = db_get_hotel_by_id(1)
        self.assertEqual(actual, expected)

    
    def test_db_get_guide_by_id(self):
        expected = Guide.parse_obj({
            'id': 1, 
            'name': 'Jason', 
            'phone_number': '+86 13806889121', 
            'email': 'Jason@gmail.com'
        })
        actual = db_get_guide_by_id(1)
        self.assertEqual(actual, expected)


    def test_db_get_car_rental_by_id(self):
        expected = CarRental.parse_obj({
            'id': 1, 
            'name': 'fast car rental', 
            'price': 10.0
        })
        actual = db_get_car_rental_by_id(1)
        self.assertEqual(actual, expected)


    def test_db_get_hotels_by_destination(self):
        expected = [Hotel.parse_obj({
            'id': 1, 
            'name': 'Crowne Plaza', 
            'price': 100.0, 
            'telephone': '080-7977-4814', 
            'address': '高橋町井高4-9-10', 
            'destination': 'Tokyo'
        })]
        actual = db_get_hotels_by_destination("Tokyo")
        self.assertEqual(actual, expected)

    
    def test_db_get_restaurants_by_destination(self):
        expected = [
            Restaurant.parse_obj({
                'id': 1, 
                'name': 'Starbelly', 
                'destination': 'Tokyo'
            }),
            Restaurant.parse_obj({
                'id': 2, 
                'name': 'abc', 
                'destination': 'Tokyo'
            })
        ]
        actual = db_get_restaurants_by_destination("Tokyo")
        self.assertEqual(actual, expected)

    
    def test_get_available_guide(self):
        expected = Guide.parse_obj({
            'id': 2, 
            'name': 'Jack', 
            'phone_number': '+1 123 1233 3213', 
            'email': 'fack@example.com'
        })
        actual = get_available_guide("Jason")
        self.assertEqual(actual, expected)


    def test_get_nearest_restaurant(self):
        expected = Restaurant.parse_obj({
            'id': 2, 
            'name': 'abc', 
            'destination': 'Tokyo'
        })
        actual = get_nearest_restaurant("Tokyo", "Starbelly")
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
