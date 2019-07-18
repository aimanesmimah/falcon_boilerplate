from .base import ResourceBase
import falcon

class ThingsResource(ResourceBase):
    def on_get(self,req,res):
        #raise falcon.HTTPUnauthorized('Auth token required','description',['Token type="Fernet"'], href='http://docs.example.com/auth')
        payload= {
            'name': 'ayman',
            'age': 23
        }

        self.on_success(res,payload)




class SmallThingsResource(ResourceBase):
    def on_get(self,req,res,name):
        payload= {
            'message': f'hello from class {self.__class__.__name__} with param: name={name}'
        }

        #res.location= '/things'

        self.on_success(res,payload)

