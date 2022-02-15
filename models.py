
from sqlalchemy.sql.expression import null
from database import Base
from sqlalchemy import ForeignKey, String,Integer,Column,DateTime
from sqlalchemy.orm import relationship
import datetime



class School(Base):
    __tablename__ = "school2"
    id= Column(Integer,primary_key=True)
    designation= Column(String(255),nullable=False)
    name= Column(String(255),nullable=False,unique=True)
    phone_number= Column(Integer,nullable=False)


class Classes(Base):
    __tablename__ = "classes2"
    id=Column(Integer,primary_key=True)
    techers_id=Column(Integer,ForeignKey(School.id))
    name_of_student=Column(String(255),ForeignKey(School.name))
    datetime=Column(DateTime,default=datetime.datetime.utcnow)

    sname = relationship("School", foreign_keys=[name_of_student])
    teacher = relationship("School", foreign_keys=[techers_id])


def __repr__(self):
    return f"<Classes name_of_student={self.name_of_student}>"



