import ecommerce.products
product = ecommerce.products.Product("name1")

from ecommerce.products import Product
product = Product("name2")

from ecommerce import products
product = products.Product("name3")

from .database import Database