from employee import Employee
from pprint import pprint
import psycopg2
from settings import *
from connection import Connection
import datetime
import random


class Admin(Connection):

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def register_self(self):
        self._register(self.login, self.password, 'admin')

    def login_self(self):
        return self._login_check(self.login, self.password, 'admin')
    # Добавляємо продукти

    def add_product(self, data):
        if self.login_self():
            table = 'product'
            result = self._postData(table, data)
        else:
            result = 'Incorrect login or password'
        return result
    # Добавляємо категорії продуктів

    def add_pr_category(self, data):
        if self.login_self():
            table = 'product_category'
            result = self._postData(table, data)
        else:
            result = 'Incorrect login or password'
        return result
    # Добавляємо emloyee в employee та login

    def add_employee(self, first_name, last_name, date_of_birds, city_id, chief_id, login, password):
        if self.login_self():
            self._register(login, password, 'employee')
            data = [{
                'first_name': first_name,
                'last_name': last_name,
                'date_of_birds': date_of_birds,
                'city_id': city_id,
                'chief_id': chief_id
            }]
            table = 'employee'
            result = self._postData(table, data)
        else:
            result = 'Incorrect login or password'
        return result
    #  удаляємо продукти

    def delete_product(self, selector):
        if self.login_self():
            table = 'product'
            selector = f"product_name = '{selector}'"
            result = self._deleteData(table,  selector)
        else:
            result = 'Incorrect login or password'
        return result
    # удаляємо категоріїї продуктів

    def delete_pr_category(self, selector):
        if self.login_self():
            table = 'product_category'
            selector = f"category_name = '{selector}'"
            result = self._deleteData(table,  selector)
        else:
            result = 'Incorrect login or password'
        return result
    # удаляємо employee

    def delete_employee(self, selector):
        if self.login_self():
            table = 'employee'
            selector = f"first_name = '{selector}'"
            result = self._deleteData(table,  selector)
        else:
            result = 'Incorrect login or password'
        return result
    # удаляємо customer

    def delete_customer(self, selector):
        if self.login_self():
            table = 'customer'
            selector = f"first_name = '{selector}'"
            result = self._deleteData(table,  selector)
        else:
            result = 'Incorrect login or password'
        return result
    # редагуємо продукти

    def edit_product(self, data, selector):
        if self.login_self():
            table = 'product'
            result = self._updateData(table, data, selector)
        else:
            result = 'Incorrect login or password'
        return result
    # редагуємо категорії продукти

    def edit_pr_category(self, data, selector):
        if self.login_self():
            table = 'product_category'
            result = self._updateData(table, data, selector)
        else:
            result = 'Incorrect login or password'
        return result
    # редагуємо employee

    def edit_employee(self, data, selector):
        if self.login_self():
            table = 'employee'
            result = self._updateData(table, data, selector)
        else:
            result = 'Incorrect login or password'
        return result
    # Добавляємо  employee, якщо він не призначений в orders  залежно від міста та стану заказу

    def add_order_employee(self):
        if self.login_self():
            order = self.get_order_info(category='status', selector=False)
            # print('order=', order)
            # формую двовимірний масив з id та назвою міста де не пизначений employee
            none_employee = [[item['id'], item['city_name']]
                             for item in order if item['employee'] == ' ']

            for item in none_employee:
                city = self._getData(('city',), ('id',),
                                     f"where city_name = '{item[1]}'")
                # print('city=', city)
                employee = self._getData(
                    ('employee',), ('id',), f"where city_id = {city[0][0]}")
                # print('employee=', employee)
                if not employee == []:
                    data = {'employee_id': random.choices(employee)[0][0]
                            }
                    changeRes = self._updateData(
                        'orders', data, f"id = {item[0]}")
                else:
                    changeRes = 'Is not Employee'
        else:
            changeRes = 'Incorrect login or password'
        return changeRes
    # Виводимо інформацію про  заказ

    def get_order_info(self, category='', selector='',):
        """
        category must be one of the item from the list:
        ['city_name','date_of_order', 'product_name','number', 'total', 'status']
        date format for selector: 2020-6-12
        """
        if self.login_self():
            categoryes = ['city_name', 'date_of_order',
                          'product_name', 'number', 'total', 'status']
            table = ('orders o',)

            fields = ("""o.id, concat(e.first_name,' ', e.last_name) as "employee", c.city_name,
                         o.date_of_order, concat(c2.first_name,' ', c2.last_name) as "customer", 
                         p.product_name, o.price, o.number , o.total, o.status """,)
            fieldNames = ["id", "employee", "city_name",
                          "date_of_order", "customer", "product_name", "price", "number", "total", "status"]
            if category and category in categoryes and selector != '':
                if isinstance(selector, bool):
                    where = f"""where {category} = {selector}"""
                else:
                    where = f"""where {category} = '{selector}'"""
            else:
                where = ''
            # print(where)
            selector = f""" left JOIN employee e on e.id = o.employee_id 
                            left JOIN city c on c.id = o.city_id 
                            left JOIN customer c2 on c2.id = o.customer_id 
                            left JOIN product p on p.id = o.product_id 
                            {where}"""
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
