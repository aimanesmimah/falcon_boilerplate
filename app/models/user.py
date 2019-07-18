import requests, json
from sqlalchemy import String, Integer,Column

class User:
    def __init__(self,name,age,email=''):
        self.name= name
        self.age= age
        if email:
            self.email= email



class UserFactory:
    def __init__(self,limit=50):
        self.items=[]
        self.defaultLimit= limit
        self.service_url= 'https://randomuser.me/api/?results={}'.format(self.defaultLimit)
    

    def getUsers(self,limit=None):
        with requests.get(self.service_url) as response:
            #print(response.text)
            try:
                 responseDict= json.loads(response.text)
                 self.items= responseDict['results'] if responseDict['results'] and len(responseDict['results']) else []
                 if limit and isinstance(limit,int) and  0 < limit < 50:
                     return self.items[0:limit]
                 return self.items
            except ValueError as error:
                raise ValueError('could not load the json response')