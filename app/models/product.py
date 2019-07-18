from sqlalchemy import Column, Integer, String, Date
from .base import ModelBase,Base


class Product(ModelBase,Base):
    __tablename__= 'products'

    id= Column(Integer, primary_key= True )
    label= Column(String)
    serial= Column(String)
    expiration= Column(Date)

    def __init__(self,serial,expiration= '2020-01-01' ):
        self.serial= serial
        self.label= f'product-{self.serial}'
        self.expiration= expiration
    

    def serialize(self):
        return {
            'label': self.label,
            'serial': self.serial,
            'expiration': str(self.expiration)
        }
    

    def __repr__(self):
        return f'{self.__class__.__name__}(label={self.label}, serial={self.serial}, expiration={self.expiration})'