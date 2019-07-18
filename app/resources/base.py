from abc import ABCMeta, abstractmethod
import falcon, json

class ResourceBase(metaclass=ABCMeta):
    RequestCounter= 0
    def __init__(self):
        self.endpoint= '/'

    @abstractmethod
    def on_get():
        pass

    def __call__(self,endpoint):
        if isinstance(endpoint,str):
            self.endpoint= endpoint
            return self
        raise TypeError('endpoint type is invalid')
    
    @staticmethod
    def on_success(response,payload):
        ResourceBase.RequestCounter += 1
        response.status= falcon.HTTP_200
        response.set_header('Powered-By', 'Falcon')
        response.body= json.dumps({
            'success': True, 
            **payload
        })
    
    @staticmethod
    def on_error(response,errorType,description=''):
        # to be more customized depending on error type
        ResourceBase.RequestCounter +=1
        errorPayload= {
            'error': True
        }

        if errorType == 'server_error':
            response.status= falcon.HTTP_500
            raise falcon.HTTPError(falcon.HTTP_500,errorType,description)
        elif errorType == 'data_error':
            response.status= falcon.HTTP_725
            response.body= json.dumps({
                **errorPayload,
                'message': 'data could not be loaded'
            })
        elif errorType == 'payload_error':
            response.status= falcon.HTTP_720
            response.body= json.dumps({
                **errorPayload,
                'message': 'incorrect request payload'
            })
        elif errorType == 'param_error':
            response.status= falcon.HTTP_741
            response.body= json.dumps({
                **errorPayload,
                'message': 'invalid request parameter'
            })
        elif errorType == 'bad_request':
            raise falcon.HTTPBadRequest(
                'Missing parameter',
                'A param must be submitted in the request body.')
        else:
            pass