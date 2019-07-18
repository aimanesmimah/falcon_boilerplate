from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine= create_engine("sqlite:///test_db.db")
_SessionFactory= sessionmaker(bind=engine)


Base= declarative_base()


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()



class ModelBase:

    @classmethod
    def get(cls):
        session= session_factory()
        results= session.query(cls)
        session.close()
        return results.all()
    

    @staticmethod
    def serialize(items):
        def handler(item):
            pass
        return list(map(handler,items))

    
    @classmethod
    def add(cls,objects):
        session= session_factory()
        if isinstance(objects,list):
            for obj in objects:
                session.add(obj)
        else:
            session.add(obj)
        
        session.commit()
        session.close()
    
    @classmethod
    def delete(cls,obj):
        session= session_factory()
        session.delete(obj)
        session.commit()
        session.close()


