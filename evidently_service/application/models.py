import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)


class Predictions(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    PULocationID = Column(Integer)
    DOLocationID = Column(Integer)
    trip_distance = Column(Float)
    passenger_count = Column(Float)
    fare_amount = Column(Float)
    total_amount = Column(Float)
    prediction = Column(Float)


class Reports(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    prediction_drift = Column(Float)
    num_drifted_columns = Column(Integer)
    share_missing_values = Column(Float)


print('now creating the table via models.py')
Base.metadata.create_all(bind=engine)