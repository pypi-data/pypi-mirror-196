#######################################################
# 
# DataPackage.py
# Python implementation of the Class DataPackage
# Generated by Enterprise Architect
# Created on:      21-Sep-2020 10:28:02 PM
# Original author: natha
# 
#######################################################
from sqlalchemy import Column
from FreeTAKServer.model.SQLAlchemy.Root import Base, Root
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import VARCHAR
from sqlalchemy import CHAR
from sqlalchemy import DateTime
from datetime import datetime as dt

class DataPackage(Base, Root):
    """
    sqlalchemy object of table of datapackages and their information
    """

    # Name of the table
    __tablename__ = "DataPackages"

    #primary key
    PrimaryKey = Column(Integer, primary_key = True, autoincrement=True)

    # UID of Package Creator
    CreatorUid = Column(String(100))

    # 32-bit hash of datapackage
    Hash = Column(VARCHAR(100))

    # data package keywords
    Keywords = Column(VARCHAR(100), default='foobar')

    # File type
    MIMEType = Column(String(100), default="[application/x-zip-compressed]")

    # Name of datapackage
    Name = Column(String(100))

    # whether or not the data package is private 0 indicates false meaning it will be publicly broadcasted.
    Privacy = Column(Integer, default=0)

    # the size in bytes of the datapackage
    Size = Column(Integer)

    # the date time the datapackage was submitted
    SubmissionDateTime = Column(DateTime, default=dt.utcnow())

    # the call sign of the user who submitted the data package
    SubmissionUser = Column(String(100))
