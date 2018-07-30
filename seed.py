from datetime import date, timedelta
from sqlalchemy import func

from model import (connect_to_db, db, Chore, Comment, 
                  User, UserChore, UserReward, UserMessage)
from random import choice


# creating chore table id, description, chore_type, min_age, chore_day_type, 
def populate_chores_table():
    
    chores_seed = [("Set the table for dinner", "set-table", True, 4, 'daily', None, False),
            ("It is time to write in your diary", "diary", True, 7, 'daily', None, True),
            ("Clear the table", "clear-table",True, 3, 'daily', None, False),
            ("Help prepare food", "cook", False, 4, 'daily',2,  False),
            ("Help carry the groceries", "groceries", True, 7, 'daily', None, False),
            ("Take the dog for a walk", "dog-walk", True, 10, 'daily', None, False),
            ("Feed the dog", "feed-dog", True, 3, 'daily',  None, False),
            ("Hang up towels in the bathroom", "towels", True, 4 ,'daily', None, True),
            ("Clean your room", "clean-room", True, 3, 'daily', None, True),
            ("Mop the living room", "mop", False,  8, 'weekly', 1, False),
            ("Change your sheets", "sheets", True, 7, 'weekly', None, False),
            ("Fold laundry", "fold", False, 6, 'daily', 2, False),
            ("Put away dishes from the dishwasher", "unload", True, 6, 'daily', None, False),
            ("Empty Garbage", "trash", False, 7, 'daily', 1, False),
            ("Do your homework", "homework", True, 6, 'homework', None, True),
            ("Sweep the livingroom", "sweep", False, 6, 'by_weekly', 1, False),
            ("Put clean laundry away", "clear-laundry", True, 5, 'daily', None, False),
            ("Wipe bathroom sink", "sink", False, 6, 'daily', 1, False),
            ("orgenize your closet", "closet", True, 6, 'weekly', None,True),
            ("Clean Bathroom Toilet", "Toilet", False, 7, 'by_weekly', 3, False),
            ("Clean Kitchen: Microwave", "Microwave",  False, 10, 'weekly', 1, False),
            ("Clean fridge", "fridge", False , 12, 'weekly', 3, False),
            ("Read for 20 minutes", "read", True, 6, 'daily',  None,True),
            ("Clean the inside of the car", "car", False, 5, 'weekly', 2, False),
            ("Get the mail", "mail", False , 4, 'daily', 1, False),
            ("prepare a salad", "salad", False , 9, 'daily', 1, False),
           
            ("Load the dishwasher", "load", False, 10, 'daily', 1, False),
            ("Vacum the carpet", "Vacum", False, 8, 'by_weekly', 2, False),
            ("Clean the ouside", "outside", True, 4, 'daily', None, False),
            ("Remove all toys/games", "toys", True, 3, 'daily', None, True)
        ]
    
    for chore in chores_seed:
        chore = Chore(description=chore[0], abr=chore[1], is_mandatory= chore[2], 
            min_age=chore[3], chore_often=chore[4], reward=chore[5], is_simultaneously=chore[6])
        db.session.add(chore)
        db.session.commit()


def populate_users_table():
    yoav = User(group='parents', password="123", user_name="Dad", is_admin=True)
    db.session.add(yoav)
    alma = User(group='kids', password="123", age=11, user_name="Alma", 
        drive_file='1yOwC8DU0Z1dEC9FBWLvW8kF84J6K61v3PWvIXqF4NdQ', drive_name= 'alma.txt')
    db.session.add(alma)
    goni = User(group='kids', password="123", age=8, user_name="Goni", 
        drive_file='18payf222xcK9pmgX03-71Og-RyTBaphiSF7wbHgNg7g', drive_name= 'goni.txt')
    db.session.add(goni)
    eric = User(group='kids', password="123", age=5, user_name="Eric")
    db.session.add(eric)
    elison = User(group='kids', password="123", age=17, user_name="Elison", 
        drive_file='12jEha6W-BPVopjKStsnQmMa1o064Z-o3_jgttD934CA', drive_name='elison.txt')
    db.session.add(elison)
    ben = User(group='kids', password="123", age=10, user_name="Ben", 
        drive_file='1QDKjLki58PMSbirTf7UQWgA2W--LyikHfFDeYlPvhJQ', drive_name='ben.txt')
    db.session.add(ben)
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