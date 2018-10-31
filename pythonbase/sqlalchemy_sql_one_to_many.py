#encoding:utf-8
from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///./test.db", echo=True)

Base = declarative_base()

class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key = True)
    name = Column(String(65))
    children = relationship("Child", backref="parent")

    def __repr__(self):
        return "<id %s>" % self.id

class Child(Base):
    __tablename__ = "child"
    id = Column(Integer, primary_key=True)
    name = Column(String(65))
    parent_id = Column(Integer, ForeignKey("parent.id"))

    def __repr__(self):
        return "<name %s>" % self.name

Base.metadata.create_all(engine)

if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()
    parent1 = Parent(name="shao6")
    session.add(parent1)
    session.commit()
    parent_id = session.query(Parent).filter_by(name="shao6").first()
    child1 = Child(name="shao7", parent_id=parent_id.id)
    child2 = Child(name="shao8",parent_id=parent_id.id)
    session.add_all([child1, child2])
    session.commit()
    result = session.query(Parent).filter_by(name="shao6").first()
    print(result.children)
    session.close()

