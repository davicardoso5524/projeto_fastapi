from models.models import db
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=db)

def pegar_sessao():
    try:
        session = Session()
        yield session
    finally:
        session.close()