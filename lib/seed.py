#!/usr/bin/env python3

from random import choice as rc
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

co_names = ['Facebook', 'Instagram', 'MySpace', 'Reddit', 'Neighborly', 'Walmart', 'Target', 'CostCo']
dev_names = ['Jake', 'Jerry', 'Jan', 'Mike', 'Bob', 'Chris', 'Jon', 'Sarah', 'Beth', 'Ben', 'Jill', 'Jake', 'Jennifer', 'Sam', 'Samantha', 'Eduardo', 'Amber', 'Melonie', 'Daryl', 'Chloe']
fb_names = ['Shirt', 'Pants', 'Scarf', 'Socks', 'Face Mask', 'Tie', 'Jacket', 'Earings', 'Ring', 'Watch', 'Backpack', 'Draw String Bag', 'Umbrella']

def create_records():
    companies = [Company(name=co_names[i], founding_year=random.randint(1800,2000)) for i in range(8)]
    devs = [Dev(name=rc(dev_names)) for i in range(500)]
    freebies = [Freebie(item_name=rc(fb_names), value=random.randint(0, 100)) for i in range(2000)]
    session.add_all(companies + devs + freebies)
    session.commit()
    return companies, devs, freebies

def delete_records():
    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.commit()

def relate_one_to_many(companies, devs, freebies):
    for freebie in freebies:
        freebie.company = rc(companies)
        freebie.dev = rc(devs)
    session.add_all(freebies)
    session.commit()
    return companies, devs, freebies

if __name__ == '__main__':
    delete_records()
    companies, devs, freebies = create_records()
    companies, devs, freebies = relate_one_to_many(companies, devs, freebies)
