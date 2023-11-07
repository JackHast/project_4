# importing dependencies

from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# declaring base

Base = declarative_base()

# creating class "corrections" to be used to create the table

class Correction(Base):
    __tablename__ = "corrections"
    sentence = Column("sentence",String,primary_key=True)
    correct_sentiment = Column("correct_sentiment",String)

    # used to instanciate the class
    def __init__(self,sentence,correct_sentiment):
        self.sentence = sentence
        self.correct_sentiment = correct_sentiment


# creating sqlite database and empty table "corrections"

engine = create_engine('sqlite:///Resources/correction.db',echo=True)
Base.metadata.create_all(bind=engine)

# creating session

Session = sessionmaker(bind=engine)
session = Session()

# closing session

session.close()

