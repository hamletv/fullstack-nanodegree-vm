# provide function and variables for run-time environment
import sys

# string classes imported used for writing mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# use in configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# used to create foreign key relationships configuration
from sqlalchemy.orm import relationship

# use in configuration code at end of file
from sqlalchemy import create_engine

# instance of declarative base class imported
# lets sqlalchemy know that our classes are special sqlalchemy classes
# that correspond to tables in our database
Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

class MenuItem(Base):
    __tablename__ = 'menu_item'
    # create database with sqlalchemy: map python objects to columns in our db
    # sytax: columnName = Column(attributes)
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    # foregin key relationship between restaurant class and menuitems class
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

#######insert at end of file########
# points to database being used
engine = create_engine('sqlite:///restaurantmenu.db')

# adds classes we will create as new tables in database
Base.metadata.create_all(engine)
