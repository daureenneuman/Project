from datetime import date, timedelta
from sqlalchemy import func

from model import (connect_to_db, db, Chore, Comment, 
                  User, UserChore, UserReward, 
                  UserBalance )
from random import choice


def populate_user_reward_log():
    userchores = UserChore.query.filter(UserChore.status == 
                            'done', UserChore.chore.has(is_mandatory = False)).all()
    for userchore in userchores:
        db.session.add(UserReward(user=userchore.user, 
                                    reward = userchore.chore.reward, date= userchore.date))
    db.session.commit()




# I need to use this precedure for my engine
def populate_user_balance():
    userrewards = db.session.query(UserReward.user_id, func.sum(UserReward.reward)).group_by(UserReward.user_id).all()
    for userreward in userrewards:
        user_id = userreward[0]
        balance = userreward[1]
        db.session.add(UserBalance(user_id=user_id, balance= balance, Last_update=date.today()))
    db.session.commit()
        


def intialize_engin():
    dict_engine = {}
    
    users = User.query.filter(User.group=='kids').all()
    dict_engine = {}
    for user in users:
        dict_user_chore = {}
        chores = Chore.query.filter(Chore.is_mandatory == False, Chore.min_age< user.age).all()
        for chore in chores:
            userrewards = db.session.query(UserChore.user_id, UserChore.chore_id, 
                func.count(UserChore.id)).filter(UserChore.chore == chore, 
                UserChore.user == user, UserChore.status=='done').group_by(UserChore.user_id, 
                UserChore.chore_id).order_by(UserChore.chore_id).all()
            for userreward in userrewards:
                dict_user_chore[chore.abr] = userreward[2]
                dict_engine[user.user_name] = dict_user_chore
    for user in users:
        if user.user_name in dict_engine:
            for chore in dict_engine[user.user_name]:
                value = dict_engine[user.user_name]
    return(dict_engine)
    
def find_history_chore(dict_engine):
    for child, chores in dict_engine.items():
        max_chore_number = 0
        min_chore_number = None
        
        for chore, number in chores.items():
        #Begiging of the child dictionary
            if min_chore_number == None:
                min_chore_number = number
                min_chore_desc = chore
            else:
                if min_chore_number > number:
                    min_chore_number = number
                    min_chore_desc = chore
                else:
                    pass
            if number > max_chore_number:
                max_chore_number = number
                max_chore_desc = chore
        
        return child, max_chore_desc, max_chore_number, min_chore_desc, min_chore_number


        













if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")

    db.create_all()
    # populate_user_reward_log()
    # populate_user_balance()
    dict_engine = intialize_engin()
    find_history_chore(dict_engine)
    


