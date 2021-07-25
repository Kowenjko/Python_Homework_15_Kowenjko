import psycopg2
from settings import *
from connection import Connection
from pprint import pprint


class Employee(Connection):

    def __init__(self, login, password):

        self.login = login
        self.password = password
    # редагуємо employee

    def edit_self_info(self, data, selector):
        if self._login_check(self.login, self.password, 'employee'):
            table = 'employee'
            result = self._updateData(table, data, selector)
        else:
            result = 'Incorrect login or password'
        return result
    # змінюємо стан заказу по id

    def change_order_status(self, id, status):

        if self._login_check(self.login, self.password, 'employee'):
            table = 'orders'
            data = {
                'status': status
            }
            result = self._updateData(table, data, f"id = {id}")
        else:
            result = 'Incorrect login or password'
        return result
    # Виводить інформацію про orders  зареєстрованого employee

    def get_order(self):

        id = self._login_check(self.login, self.password, 'employee')

        if id:
            id_employee = self._getData(
                ('employee',), ('id',), f"where reg_id = {id}")[0][0]

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
                            where e.id= {id_employee}"""
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
