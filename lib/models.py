from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine, desc
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship('Freebie', back_populates='company', cascade='all, delete-orphan')
    devs = association_proxy('freebies', 'dev', creator=lambda de: Freebie(dev=de))

    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(item_name=item_name, value=value, company=self, dev=dev)
        session.add(new_freebie)
        session.commit()
        return new_freebie
    
    @classmethod
    def oldest_company(cls):
        oldest_co = session.query(cls).order_by(cls.founding_year).first()
        return oldest_co

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship('Freebie', back_populates='dev', cascade='all, delete-orphan')
    companies = association_proxy('freebies', 'company', creator=lambda co: Freebie(company=co))

    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def received_one(self, item_name):
        for fb in [freebie.item_name for freebie in self.freebies]:
            if fb == item_name:
                return True
        return False
    
    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            session.query(Freebie).filter(Freebie.id == freebie.id).update({Freebie.dev_id: dev.id})
            print(f'{self.name} gave away their {freebie.item_name} to {dev.name}.')
        else:
            print(f'{self.name} does not have a {freebie.item_name}.')
            
    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    company = relationship('Company', back_populates='freebies')
    dev = relationship('Dev', back_populates='freebies')

    def __repr__(self):
        return f'<Freebie {self.item_name}>'
    
    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'
    

#import ipdb; ipdb.set_trace()
