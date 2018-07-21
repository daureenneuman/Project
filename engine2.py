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
    len_users = 6
    print(len_chores)
    for chore in chore_dictionary:
        print(chore)
        print("down :here")
        
        for i in range(len(chore_dictionary[chore])):
            user_id = chore_dictionary[chore][i][0].id
            print("look here this is the user")
            print(user_id)
            
            if user_id not in user_counts or user_counts[user_id]<= int(len_chores / len_users):
                user_counts[user_id] = user_counts.get(user_id, 0) + 1
                print(i)
                print("entered if")
                print(user_counts)
                db.session.add(UserChore(user_id=user_id,  
                    chore=chore, date=day, status="suggested"))
                db.session.commit() 
                break

# every kid is going to get his daily mandatory assignment
def assign_man_sim(chore_dictionary):
#   
    for chore in chore_dictionary:
        print(chore)
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
# every kids is being suggested with his favorite and least favorite
def assign_vol_turn(child_dictionary):
    print("start function")
    print("start function")
    print("start function")
    print("start function")
    print("start function")
    print("start function")
    print("start function")
    print("start function")
    print("start function")
    print("start function")
    print(child_dictionary)
    list_chores = []
    len_users = len(child_dictionary)
    children = list(child_dictionary.keys())
    shuffle(children)
    for user in children:
        print("starting a new user : {}".format(user))
        print("starting a new user : {}".format(user))
        print("starting a new user : {}".format(user))
        print("starting a new user : {}".format(user))
        for i in range(len_users):
            
            least = None
            most = None
            len_chores = len(list(child_dictionary.values())[i])
            
            for j in range(len_chores):
                print("user is {} len chores for user is {} j is {}".format(user, len_chores, j))
                print("user is {} len chores for user is {} j is {}".format(user, len_chores, j))
                print("user is {} len chores for user is {} j is {}".format(user, len_chores, j))                                       
                if most == None:
                    print("first if ")
                    chore_most = child_dictionary[user][-j-1][0]
                    if chore_most not in list_chores:
                        print("adding most favorite chore to db")
                        db.session.add(UserChore(user=user,  
                        chore=chore_most, date=day, status="suggested"))
                        db.session.commit() 
                        list_chores.append(chore_most)
                        print(list_chores)
                        most = True
                        print("user is {} most is {} and least is {}".format(user, most, least))
                        print("user is {} most is {} and least is {}".format(user, most, least))
                        print("user is {} most is {} and least is {}".format(user, most, least))
                if least == None:
                    chore_least = child_dictionary[user][j][0]
                    if chore_least not in list_chores:
                        print("adding least favorite chore to db")
                        db.session.add(UserChore(user=user,  
                            chore=chore_least, date=day, status="suggested"))
                        db.session.commit() 
                        list_chores.append(chore_least)
                        print(list_chores)
                        least = True
                        print("user is {} most is {} and least is {}".format(user, most, least))
                        print("user is {} most is {} and least is {}".format(user, most, least))
                        print("user is {} most is {} and least is {}".format(user, most, least))
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
