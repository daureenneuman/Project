from datetime import date, timedelta
from sqlalchemy import func

from model import (connect_to_db, db, Chore, Comment, 
                  User, UserChore, UserReward)
from random import choice, shuffle


def populate_chore_volentary():
       # going over all days in the last 30 days
    for i in range(1, 20):
        day = date.today() - timedelta(i)

        # quering all the volentary chores
        chores = Chore.query.filter(Chore.is_mandatory==False).order_by(Chore.min_age).all()
        for chore in chores:
            # quering all kids that are age appropriate for the chore
            users = User.query.filter(User.age>= chore.min_age, 
                            User.group=='kids').order_by(User.age).all()
            shuffle(users)
            # if the the chore can be simutensely 
            if chore.is_simultaneously==True:
                # chore is daily
                if chore.chore_often == 'daily':
                    for user in users:
                        user_pick = choice([True, True, False, False])
                        # is user for this date chose this chore add record and go to the next user in the same day
                        if user_pick:
                            db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status="done"))      
                        
                        # user did not pick the chore go with this chore and day to the next user
                
                # if the the chore is twice a week and is simuteniusly
                elif chore.chore_often == 'by_weekly':
                    # checking if is it tuesday ot friday
                    if day.weekday() in [2, 5]:
                        for user in users:
                            user_pick = choice([True, False, False, False])
                            # is user for this date chose this chore add record and go to the next user in the same day
                            if user_pick:
                                db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status="done"))
                            # user did not pick the chore go with this chore and day to the next user

                # chore is weekly and simuteniusly
                else:
                    if day.weekday() == 5:
                        for user in users:
                            user_pick = choice([True, False, True, False])
                            # is user for this date chose this chore add record and go to the next user in the same day
                            if user_pick:
                                db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status="done"))                        
                            # user did not pick the chore go with this chore and day to the next user


            # chore is in turns daily
            else:
                if chore.chore_often == 'daily':
                    for user in users:
                        user_pick = choice([False, True, True, False])
                        if user_pick:
                            db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status="done"))
                            # break for users and go to the next chore with the same day 
                            break
                    continue
                #chores in turn by twice a week
                elif chore.chore_often == 'by_weekly':
                    if day.weekday() in [2, 5]:
                        for user in users:
                            user_pick = choice([True, False, True, False])
                            if user_pick:
                                db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status="done"))
                            # break for users and go to the next chore with the same day 
                                break
                    continue
                #chores in turn by weekly
                else:
                    if day.weekday() == 5:
                        for user in users:
                            user_pick = choice([True, False, False, False])
                            if user_pick:
                                db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status="done"))
                            # break for users and go to the next chore with the same day 
                                break
                    continue

                
                        
                        
                    
        db.session.commit() 

def populate_chores_mandatory():
       # going over all days in the last 30 days
    for i in range(1, 20):
        day = date.today() - timedelta(i)

        # quering all the Mandatory chores
        chores = Chore.query.filter(Chore.is_mandatory==True).order_by(Chore.min_age).all()
        for chore in chores:
            # quering all kids that are age appropriate for the chore
            users = User.query.filter(User.age>= chore.min_age, 
                            User.group=='kids').order_by(User.age).all()
            shuffle(users)
            # if the the chore can be simutensely 
            if chore.is_simultaneously==True:
                # chore is daily
                if chore.chore_often == 'daily':
                    for user in users:
                        status = choice(["done", "done", "done", "assigned"])
                        # add record and go to the next user in the same day
                        db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status=status))      
                        
                                      
                # chore is twice a week and is simuteniusly
                elif chore.chore_often == 'by_weekly':
                    # checking if is it tuesday ot friday
                    if day.weekday() in [2, 5]:
                        for user in users:
                            status = choice(["done", "done", "done", "assigned"])
                            # add record and go to the next user in the same day
                            db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status=status))
                            
                # chore is homework and simuteniusly
                elif chore.chore_often == 'homework':
                    if day.weekday() in [1, 2, 3,  4,5]:
                        for user in users:
                            status = choice(["done", "done", "done", "assigned"])
                            # add record and go to the next user in the same day
                            db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status=status))
                            


                 # chore is weekly and simuteniusly
                else:
                    if day.weekday() == 5:
                        for user in users:
                            status = choice(["done", "done", "done", "assigned"])
                            # add record and go to the next user in the same day
                            db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status="done"))                        
                           


            # chore is in turns daily
            else:
                if chore.chore_often == 'daily':
                    
                    for user in users:

                        db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status="done"))

                        # break from users and go to the next chore with the same day 
                        break
                    continue
                #chores in turn by twice a week
                elif chore.chore_often == 'by_weekly':
                    if day.weekday() in [2, 5]:
                        for user in users:
                            db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status="done"))
                            # break from users and go to the next chore with the same day 
                            break
                    continue
                #chores in turn by weekly
                else:
                    if day.weekday() == 5:
                        for user in users:
                            db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status="done"))
                            # break for users and go to the next chore with the same day 
                            break
                    continue

                
                        
                        
                    
        db.session.commit() 


def populate_user_reward_log():
    userchores = UserChore.query.filter(UserChore.status == 
                            'done', UserChore.chore.has(is_mandatory = False)).all()
    for userchore in userchores:
        db.session.add(UserReward(user=userchore.user, 
                                    reward = userchore.chore.reward, date= userchore.date))
    db.session.commit()




# I need to use this precedure for my engine


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")
    db.create_all()
    populate_chore_volentary()
    populate_chores_mandatory()
    populate_user_reward_log()
    