import psycopg2
from settings import *
from connection import Connection
from datetime import datetime


class RegisteredCustomer(Connection):

    def __init__(self,  email, password):
        self.login = email
        self.password = password
        self._first_name = ''
        self._last_name = ''
        self._city_id = ''
        self._id = ''

    def login_self(self):
        id = self._login_check(self.login, self.password, 'customer')
        if id:
            self._first_name = self._getData(
                ('customer',), ('first_name',), f"where reg_id = {id}")[0][0]
            self._last_name = self._getData(
                ('customer',), ('last_name',), f"where reg_id = {id}")[0][0]
            self._city_id = self._getData(
                ('customer',), ('city_id',), f"where reg_id = {id}")[0][0]
            self._id = self._getData(
                ('customer',), ('id',), f"where reg_id = {id}")[0][0]
            return True
        return False
    # виводимо інформацію про customer

    def get_self_info(self, selector=''):
        id = self._login_check(self.login, self.password, 'customer')
        print(id)
        if id:
            id_customer = self._getData(
                ('customer',), ('id',), f"where reg_id = {id}")[0][0]
            table = ('orders o',)
            fields = ("""o.id, concat(e.first_name,' ', e.last_name) as "employee", c.city_name,
                         o.date_of_order, concat(c2.first_name,' ', c2.last_name) as "customer", 
                         p.product_name, o.price, o.number , o.total, o.status """,)
            fieldNames = ["id", "employee", "city_name",
                          "date_of_order", "customer", "product_name", "price", "number", "total", "status"]
            selector = f""" left JOIN employee e on e.id = o.employee_id 
                            left JOIN city c on c.id = o.city_id 
                            left JOIN customer c2 on c2.id = o.customer_id 
                            left JOIN product p on p.id = o.product_id 
                            where c2.id= {id_customer}"""
            result = self._getData(table, fields, selector)
            if not result == []:
                changeRes = []
                for item in result:
                    cort = {}
                    for index, element in enumerate(item):
                        cort[fieldNames[index]] = element
                    changeRes.append(cort)
            else:
                changeRes = 'You have no orders'

        else:
            changeRes = 'Incorrect login or password'
        return changeRes
    # створюємо покупку зареєстрованим customer

    def create_order(self, products):
        if self.login_self():
            table = 'orders'
            data = []
            for item in products:
                order = {
                    "customer_id": self._id,
                    "city_id": self._city_id,
                    "date_of_order": datetime.today().strftime('%Y-%m-%d'),
                    "product_id": self._getData(('product',), ('id',), f"where product_name = '{item[0]}'")[0][0],
                    "price": self._getData(('product',), ('unit_price',), f"where product_name = '{item[0]}'")[0][0],
                    "number": item[1],
                    "total": self._getData(('product',), ('unit_price',), f"where product_name = '{item[0]}'")[0][0]*item[1],
                }
                data.append(order)
            result = self._postData(table, data)
            return result
        else:
            result = 'Incorrect login or password'
        return result
    # Удаляємо orders

    def delete_order(self, selector):
        if self.login_self():
            table = 'orders'
            selector = f"date_of_order = '{selector}'"
            result = self._deleteData(table,  selector)
        else:
            result = 'Incorrect login or password'
        return result
    # Виводимо інформацію про продукт

    def get_product_info(self, category='', selector='',):
        """
        category must be one of the item from the list:
        ['product_name','country_name', 'category_name']        
        """
        if self.login_self():
            categoryes = ['product_name', 'country_name', 'category_name']
            table = ('product p',)
            fields = (
                """p.id, p.product_name ,p.unit_price,c.country_name,pc.category_name """,)
            fieldNames = ["id", "product_name", "unit_price",
                          "country_name", "category_name"]
            if category and category in categoryes and selector:
                where = f"""where {category} = '{selector}'"""
            else:
                where = ''

            selector = f""" inner join country c on c.id =p.country_id                             
                                inner join product_category pc on pc.id =p.product_catagery_id {where}"""
            result = self._getData(table, fields, selector)
            changeRes = []
            for item in result:
                cort = {}
                for index, element in enumerate(item):
                    cort[fieldNames[index]] = element
                changeRes.append(cort)

        else:
            changeRes = 'Incorrect login or password'
        return changeRes
