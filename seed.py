from datetime import date, timedelta
from sqlalchemy import func

from model import (connect_to_db, db, Chore, Comment, 
                  User, UserChore, UserReward, UserMessage)
from random import choice


# creating chore table id, description, chore_type, min_age, chore_day_type, 
def populate_chores_table():
    
    chores_seed = [("Set the table for dinner", "set-table", True, 4, 'daily', None, False),
            ("Diary time", "diary", True, 7, 'daily', None, True),
            ("Clear the table", "clear-table",True, 3, 'daily', None, False),
            ("Help prepare food", "cook", False, 4, 'daily',2,  False),
            ("Help with groceries", "groceries", False, 7, 'daily', 1, False),
            ("Take the dog for a walk", "dog-walk", False, 10, 'daily', 2, False),
            ("Feed the dog", "feed-dog", False, 3, 'daily',  1, False),
            ("Clean your room", "clean-room", True, 3, 'daily', None, True),
            ("Change your sheets", "sheets", False, 10, 'daily', 2, True),
            ("Fold laundry", "fold", False, 6, 'daily', 2, False),
            ("Unload the dishwasher", "unload", True, 6, 'daily', None, False),
            ("Empty Garbage", "trash", False, 7, 'daily', 1, False),
            ("Do your homework", "homework", True, 6, 'homework', None, True),
            ("Put clean laundry away", "clear-laundry", True, 5, 'daily', None, False),
            ("Organise your closet", "closet", False, 11, 'daily', 3,True),
            ("Read 20 minutes", "read", True, 6, 'daily',  None,True),
            ("Wash the car", "car", False, 5, 'weekly', 2, False),
            ("Get the mail", "mail", False , 4, 'daily', 1, False),
            ("prepare a salad", "salad", False , 9, 'daily', 1, False),
            ("Load the dishwasher", "load", False, 10, 'daily', 1, False)
           
        ]
    
    for chore in chores_seed:
        chore = Chore(description=chore[0], abr=chore[1], is_mandatory= chore[2], 
            min_age=chore[3], chore_often=chore[4], reward=chore[5], is_simultaneously=chore[6])
        db.session.add(chore)
        db.session.commit()


def populate_users_table():
    yoav = User(group='parents', password="123", user_name="Dad", is_admin=True)
    db.session.add(yoav)
    db.session.commit()
    alma = User(group='kids', password="123", age=11, user_name="Alma", 
        drive_file='1yOwC8DU0Z1dEC9FBWLvW8kF84J6K61v3PWvIXqF4NdQ', drive_name= 'alma.txt')
    db.session.add(alma)
    db.session.commit()
    goni = User(group='kids', password="123", age=8, user_name="Goni", 
        drive_file='18payf222xcK9pmgX03-71Og-RyTBaphiSF7wbHgNg7g', drive_name= 'goni.txt')
    db.session.add(goni)
    db.session.commit()
    ben = User(group='kids', password="123", age=10, user_name="Ben", 
        drive_file='1QDKjLki58PMSbirTf7UQWgA2W--LyikHfFDeYlPvhJQ', drive_name='ben.txt')
    db.session.add(ben)
    db.session.commit()
    nicole = User(group='kids', password="123", age=4, user_name="Nicole")
    db.session.add(nicole)
    db.session.commit()


           ###########################################     
if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")

    db.create_all()

    populate_chores_table()
    populate_users_table()