import sys
from sqlalchemy import Column, ForeignKey, Integer, String
# used for writing mapper code

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
# used to create foreign key relationships

from sqlalchemy import create_engine
# class used in config code at end of file

Base = declarative_base()
# lets sqlalchemy know that classes are special sqlalchemy classes
# that correspond to tables in our database
# 1 - 12 configuration code

class Team(Base):               # class definition
    __tablename__ = 'team'      # table information

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    # mapper code
    @property
    def serialize(self):
        return {
        'name': self.name,
        'id': self.id
        }

class Player(Base):             # class definition
    __tablename__ = 'player'    # table information

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    position = Column(String(30), nullable = False)
    bio = Column(String(1000))
    team_id = Column(Integer, ForeignKey('team.id'))
    # create foreign key relationship between team and player
    # look in team table and get team.id whenever team_id is called.
    team = relationship(Team)
    # mapper code
    @property
    def serialize(self):
        return {
        'name': self.name,
        'id': self.id,
        'position': self.position,
        'bio': self.team_id
        }

### insert at end of file ###
engine = create_engine('sqlite:///mydatabase.db')
# points to the database to be used. create engine can create file with mysql or postgres as well

Base.metadata.create_all(engine)
# goes into db and adds classes to be created as new tables in db.
