import falcon, multiprocessing, json
from gunicorn.app.base import BaseApplication
from gunicorn.six import iteritems
import gunicorn.reloader

class Application(BaseApplication):
    def __init__(self,root,port='8080'):
        try:
            self.application= falcon.API(middleware= self.subscribe_middlewares())
            #self.application.add_error_handler(Exception,self.unexpected_error_handler)
            self.options=  {
                                    'bind': '%s:%s' % ('127.0.0.1', port ),
                                    'workers': self.number_of_workers(),
                                }
            
            super(Application,self).__init__()
        except ValueError as error:
            print(error)
        
        #self.subscribe_route(ThingsResource()('/things'))
       
    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options) if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)
    
    
    def load(self):
        return self.application
    
    @staticmethod
    def number_of_workers():
        return (multiprocessing.cpu_count() * 4) + 1

    def subscribe_middlewares(self):
        from app.middlewares import middlewares
        results= filter(lambda middleware: callable(middleware), middlewares)
        results= list(map( lambda middleware: middleware(), results ))
        results= filter(lambda instance: hasattr(instance,'process_request') or hasattr(instance,'process_response'), results)
        return list(results)

    def subscribe_middlewares_deprecated(self):
        middlewareAttributes= filter(lambda item: isinstance(item,str) and (item[0:2] != '__' or item[-2:] != '__'), dir(mwares or object()))
        appMiddlewares=[]
        for attr in middlewareAttributes:
            middleware= getattr(mwares,attr)
            #assert callable(middleware)
            if callable(middleware):
                instance= middleware()
                if hasattr(instance,'process_response') or hasattr(instance,'process_request'):
                    appMiddlewares.append(instance)
        
        return appMiddlewares


    def subscribe_route_deprecated(self,resource):
        if self.application and hasattr(self.application,'add_route'):
            self.application.add_route(resource.endpoint,resource)
    
    @staticmethod
    def error_handler(ex, req, resp, params):
        resp.body= json.dumps({
            'success': False,
           'message': 'an error has occured, try again'
        })


    def configure_env(self):
        import sys
        args= sys.argv
        self.env= 'production' if len(args) > 1 and args[1] == 'production' else 'development'