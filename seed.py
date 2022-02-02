from faker import Faker
from Internship_Project import db, UserModel, PostModel
from werkzeug.security import generate_password_hash
from random import random, randint

fake = Faker()


db.create_all()

for i in range(1,5):
    user = UserModel(username=fake.name(), email=fake.email(), password=generate_password_hash(fake.password()))
    db.session.add(user)
    db.session.commit()

for i in range(1,5):
    post = PostModel(account_name=fake.sentence(nb_words=2), amount=randint(600, 16758), profit=randint(10, 600))
    db.session.add(post)
    db.session.commit()
### in the terminal : / python <filename> (seed.py) /
