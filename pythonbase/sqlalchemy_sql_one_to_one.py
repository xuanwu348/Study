#encoding:utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///./one2one.db", echo=True)
Base = declarative_base()

class Addr(Base):
    __tablename__ = "addr"
    id = Column(Integer, primary_key=True)
    addr = Column(String(30))
    paddr = relationship("Person", uselist=False, backref="addr")

    def __repr__(self):
        return "<name %s>" % self.name

class Person(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    addr_id = Column(Integer, ForeignKey("addr.id"))

    def repr(self):
        return "<name %s>" % self.name

Base.metadata.create_all(engine)

if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()
    addr = Addr(addr="shenzhen nanshan road")
    session.add(addr)
    session.commit()
    addr_t= session.query(Addr).filter_by(addr="shenzhen nanshan road").first()
    person = Person(name="zhangsan", addr_id=addr_t.id)
    session.add(person)
    session.commit()
    result = session.query(Addr).filter_by(addr="shenzhen nanshan road").first()
    print(result.paddr.name)
    session.close()

