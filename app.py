from admin import Admin
from unregisteredCustomer import UnregisteredCuctomer
from registeredCustomer import RegisteredCustomer
from employee import Employee
from pprint import pprint
from custom import respprint
import datetime


admin1 = Admin('admin', 'admin')
# print(admin1.add_order_employee())
# orders = admin1.get_order_info(category='status', selector=False)
# orders = admin1.get_order_info(category='city_name', selector='London')
# # orders = admin1.get_order_info(category='date_of_order', selector='2020-6-12')
# respprint(orders)
# print(orders)
# --------------------------------------------------------------------
# unregCust = UnregisteredCuctomer()
# unregCust.register_self('Karl', 'mop', 6, 'mop', 'mop')
# respprint(unregCust.get_product_info())

# --------------------------------------------------------------------
# regCust = RegisteredCustomer('mop', 'mop')
# info = regCust.get_self_info()
# orders = regCust.create_order([('Fish', 2), ('Pork', 3), ('Water', 5)])
# print(orders)
# pprint(info)
# respprint(info)
# respprint(product)
# --------------------------------------------------------------------
# employee = Employee('Kagor', 'kagor')
# employee = Employee('Tanos', 'tanos')
# employee = Employee('Dadar', 'dadar')
# employee = Employee('Garin', 'garin')
# status = employee.get_order()
# respprint(status)
# change = employee.change_order_status(14, True)
# status = employee.get_order()
# respprint(status)
# status = employee.change_order_status()
# respprint(status)

# pprint(status)
# --------------------------------------------------------------------
