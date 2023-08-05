import time

from sharetop.core.oil.oil_detail import get_oil_reserves, get_oil_products, get_oil_consumption,\
    get_oil_refinerythroughput, get_oil_refinerycapacity, get_oil_crudeoilpricehistory

token = "f109298d079b5f60"

# d1 = get_oil_reserves(token, "1")
# print(d1)
#
# d2 = get_oil_products(token, "1")
# print(d2)

d3 = get_oil_crudeoilpricehistory(token)
print(d3)

# for i in range(10):
#     # time.sleep(3)
#     d1 = get_oil_consumption(token, "1")
#     print(d1)

