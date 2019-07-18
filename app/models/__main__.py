from datetime import date
from product import Product
from base import session_factory


# this module exists just for the sake testing orm tables mapping

def create_products():
    session= session_factory()
    session.add(Product('xxx123',date(2019, 10, 20)))
    session.add(Product('xxx1234',date(2020,11,6))) 
    session.commit()
    session.close()


def get_products():
    session= session_factory()
    print(dir(session))
    products_query= session.query(Product)
    session.close()
    return products_query.all()



if __name__ == '__main__':
    products = get_products()
    if len(products) == 0:
        create_products()
    products = get_products()

    for p in products:
        print(p.id)
        print(p)
        print(f'product with serial: {p.serial} has expiration date: {str(p.expiration)}')