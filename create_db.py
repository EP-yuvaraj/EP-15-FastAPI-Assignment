from database import Base,engine
from models import Classes,School

print("Creating DataBase ....")

Base.metadata.create_all(engine)

print("Created DataBase ....")

