from .base import ResourceBase
from app.models import Product


class ProductResource(ResourceBase):
    def on_get(self,req,res):
        prods= Product.get()
        print(prods)
        l= list(map(lambda x: x.serialize() ,prods))
        self.on_success(res,{
            'count': len(l),
            'products': l
        })
    
    def on_post(self,req,res):
        pass