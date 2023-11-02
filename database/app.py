# importing dependencies

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# declaring base

Base = declarative_base()

# creating class "corrections" to be used to create table

class Correction(Base):
    __tablename__ = "corrections"
    sentence = Column("sentence",String,primary_key=True)
    output_sentiment = Column("output_sentiment",Integer)
    correct_sentiment = Column("correct_sentiment",Integer)

    # used to instanciate the class
    def __init__(self,sentence,output_sentiment,correct_sentiment):
        self.sentence = sentence
        self.output_sentiment = output_sentiment
        self.correct_sentiment = correct_sentiment


# creating sqlite database and empty table "corrections"

engine = create_engine('sqlite:///Resources/correction.db',echo=True)
Base.metadata.create_all(bind=engine)

# creating session

Session = sessionmaker(bind=engine)
session = Session()

# This is an example of creating an instance of the Correction class and adding to the database

correction = Correction('wallstreet explodes',1,0)
session.add(correction)
session.commit()

# closing session

session.close()

