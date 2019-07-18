from app import Application
from app.resources import apply_routes
import os,sys

if __name__ == '__main__':
    root= sys.path[0]
    application= Application(root,port=5050)
    apply_routes(application.load())
    application.run()