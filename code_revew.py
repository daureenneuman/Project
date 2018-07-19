from datetime import date, timedelta
from sqlalchemy import func,  or_
import sys
import operator
from model import (connect_to_db, db, Chore, Comment, User, UserChore, UserReward, UserBalance )
from random import choice

    
def show_chores(day, mandatory, simultaneously ):
    weekday = day.weekday()
    print(weekday)
    if weekday == 2:
        chores_often = Chore.query.filter(_or(Chore.chore_often == 'by_weekly', 
            Chore.chore_often == 'daily',Chore.chore_often == 'homework')).all()
        print(chores_often)
    elif weekday == 5:
        chores_often = Chore.query.filter(_or(Chore.chore_often == 'by_weekly', 
            Chore.chore_often == 'weekly', Chore.chore_often =='daily')).all()
        print(chores_often)

    elif weekday  in [1,3,4]:
        chores_often = Chore.query.filter(_or(Chore.chore_often == 'homework', 
           Chore.chore_often == 'daily')).all()
        print(chores_often)
    else: 
        chores_often = Chore.query.filter(Chore.chore_often == 'daily').all()
    chores = []
    for chore in chores_often:
        if chore.is_simultaneously == simultaneously and chore.is_mandatory == mandatory:
            chores.append(chore)
    return chores

def craeting_chore_dictionary(chores):
    dict_chore = {} 
    for chore in chores:
        dict_child = {}
        users = User.query.filter(User.age>= chore.min_age, 
              User.group=='kids').order_by(User.age).all()
        for user in users:
            userrewards = db.session.query(UserChore.user_id, UserChore.chore_id, 
            func.count(UserChore.id)).filter(UserChore.chore == chore, 
               UserChore.user == user, UserChore.status=='done').group_by(UserChore.user_id, 
                        UserChore.chore_id).order_by(UserChore.chore_id).all()
            dict_child[user] = 0
            dict_chore[chore] = dict_child
            for userreward in userrewards:
                dict_child[user] = userreward[2]
                dict_chore[chore] = dict_child
    
    #sorting the dictionary by the number each child made a chore            
    chore_dictionary = {}
    for chore in dict_chore:
        sorted_dict = list(sorted(dict_chore[chore].items(), key=operator.itemgetter(1)))
        chore_dictionary[chore] = sorted_dict

    return chore_dictionary
    
def creating_child_dictionary(chores):
    child_dictionary = {}
    users = User.query.filter(User.group=='kids').all()
    
    for user in users:
        chore_dict= {}      

        chore_list = []
        for chore in chores:
            if chore.min_age <= user.age:
                chore_list.append(chore)

        chores = chore_list
        print(chores)

        for chore in chores:
            chore_dict[chore] = 0
            child_dictionary[user] = chore_dict
            
            userrewards = db.session.query(UserChore.user_id, UserChore.chore_id, 
                func.count(UserChore.id)).filter(UserChore.chore == chore, 
                    UserChore.user == user, UserChore.status=='done').group_by(UserChore.user_id, 
                        UserChore.chore_id).order_by(UserChore.chore_id).all()
            for userreward in userrewards:
                chore_dict[chore] = userreward[2]
                child_dictionary[user] = chore_dict
    

    child_dict = {}
    for child in child_dictionary:
        sorted_dict = list(sorted(child_dictionary[child].items(), key=operator.itemgetter(1)))
        child_dict[child] = sorted_dict
        
           
    return child_dict

#         continue    
if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database direc


    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB.")

    db.create_all()
    day =date.today()
    chores_man_sim = show_chores(day, mandatory=True, simultaneously=True)
    chores_man_turn = show_chores(day, mandatory=True, simultaneously=False)
    chores_vol_sim = show_chores(day, mandatory=False, simultaneously=True)
    chores_vol_turn = show_chores(day, mandatory=False, simultaneously=False)
    
    chore_dictionary = craeting_chore_dictionary(chores_man_sim)
    child_dictionary= creating_child_dictionary(chores_man_turn)
    