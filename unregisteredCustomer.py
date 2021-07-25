import psycopg2
from settings import *
from connection import Connection


class UnregisteredCuctomer(Connection):
    # Реєструємо customer
    def register_self(self, first_name, last_name, city, login, password):
        if self._register(login, password, 'customer'):
            table = 'customer'
            data = [{
                'city_id': city,
                'first_name': first_name,
                'last_name': last_name,
                'reg_id': self._getNextId('login')-1,
            }]
            result = self._postData(table, data)
        else:
            result = 'Login is exist!'
        return result
    # Виводимо інформацію про продукт

    def get_product_info(self, category='', selector='',):
        """
        category must be one of the item from the list:
        ['product_name','country_name', 'category_name']        
        """

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

        return changeRes
