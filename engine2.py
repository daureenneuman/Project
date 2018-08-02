from datetime import date, timedelta
from sqlalchemy import func,  or_
import sys
import operator
from model import (connect_to_db, db, Chore, Comment, User, UserChore, UserReward)
from random import choice, shuffle
from engine import show_chores, craeting_chore_dictionary, creating_child_dictionary


# in this input dictionary every chore has secondary chold kid with the number of time the child has done the chore
# this function is assigning chores based on the kid that has done ot the least number of time
def assign_man_turn(chore_dictionary):
    user_counts = {}
    len_chores = len(chore_dictionary)
    users = User.query.filter(User.group=='kids').order_by(User.age).all()
    len_users = len(users)
    
    for chore in chore_dictionary:
        for i in range(len(chore_dictionary[chore])):
            user_id = chore_dictionary[chore][i][0].id
                        
            if user_id not in user_counts or user_counts[user_id]<= int(len_chores / len_users):
                user_counts[user_id] = user_counts.get(user_id, 0) + 1
                db.session.add(UserChore(user_id=user_id,  
                    chore=chore, date=day, status="suggested"))
                db.session.commit() 
                break

# every kid is going to get his daily mandatory assignment
def assign_man_sim(chore_dictionary):
#   
    for chore in chore_dictionary:
        
        users = User.query.filter(User.age>= chore.min_age, 
                            User.group=='kids').order_by(User.age).all()
        for user in users: 
            db.session.add(UserChore(user=user, chore=chore, 
                                            date=day, status='assigned'))      
    db.session.commit()
           


def assign_vol_sim(chore_dictionary):
   for chore in chore_dictionary:
        print(chore)
        users = User.query.filter(User.age>= chore.min_age, 
                            User.group=='kids').order_by(User.age).all()
        chores_count = 0
        while chores_count <=2:
            for user in users: 
                db.session.add(UserChore(user=user, chore=chore, 
                                            date=day, status='suggested')) 
                db.session.commit()
                chores_count+=1   
         
        continue
#   :
# every kids is suggested ro earn reward by completing his least favorite chore and most favorite chore
def assign_vol_turn(child_dictionary):
    list_chores = []
    len_users = len(child_dictionary)
    children = list(child_dictionary.keys())
    shuffle(children)
    for user in children:
        for i in range(len_users):
            
            least = None
            most = None
            len_chores = len(list(child_dictionary.values())[i])
            
            for j in range(len_chores):
                if most == None:
                    chore_most = child_dictionary[user][-j-1][0]
                    if chore_most not in list_chores:
                        db.session.add(UserChore(user=user,  
                        chore=chore_most, date=day, status="suggested"))
                        db.session.commit() 
                        list_chores.append(chore_most)
                        print(list_chores)
                        most = True

                if least == None:
                    chore_least = child_dictionary[user][j][0]
                    if chore_least not in list_chores:
                        db.session.add(UserChore(user=user,  
                            chore=chore_least, date=day, status="suggested"))
                        db.session.commit() 
                        list_chores.append(chore_least)
                        least = True

                if most == True and least == True:
                    break
            break            




if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database direc


    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB.")

    db.create_all()
    day = date.today() 
    chores_man_sim = show_chores(day, True, True)
    chores_man_turn = show_chores(day, True, False)
    chores_vol_sim = show_chores(day, False, True)
    chores_vol_turn = show_chores(day, False, False)
    
    #creating assignment for man turn chores
    man_turn_chore_dictionary = craeting_chore_dictionary(chores_man_turn)
    assign_man_turn(man_turn_chore_dictionary)

    # #creating assignment for man sim chores
    man_sim_dictionary = craeting_chore_dictionary(chores_man_sim)
    assign_man_sim(man_sim_dictionary)

    # # creating assignment for vol sim chores there is none and the data base currently
    vol_sim_dictionary = craeting_chore_dictionary(chores_vol_sim)
    assign_vol_sim(vol_sim_dictionary)

   #creating assignment for vol turn chores there is none and the data base currently
      
    child_dict = creating_child_dictionary(chores_vol_turn)
    assign_vol_turn(child_dict)
