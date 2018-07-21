def assign_man_vol_turn(new_dict):
    user_counts = {}
    len_chores = len(new_dict)
    len_users = 6
    print(len_chores)
    for chore in new_dict:
        if chore.chore_often =='by_weekly':
            if day.weekday() == 0 or day.weekday() == 5:
                print(chore)
                print("down :here")
                print(new_dict[chore])
                for i in range(len(new_dict[chore])):
                    user_id = new_dict[chore][i][0]
                    print("look here this is the user")
                    print(user_id)
            
                    if user_id not in user_counts or user_counts[user_id]<= int(len_chores / len_users):
                        user_counts[user_id] = user_counts.get(user_id, 0) + 1
                        print(i)
                        print("entered if")
                        print(user_counts)
                        print(user_counts[user_id])
                        db.session.add(UserChore(user_id=new_dict[chore][i][0],  
                            chore=chore, date=day, status="suggested"))
                        db.session.commit() 
                        break
                    else:
                        print("i'm in else")
                        print(i)
                        print(user_counts)
                        print(user_counts[user_id])
                        continue
        elif chore.chore_often =='weekly':
            if day.weekday() ==  5:
                print(chore)
                print("down :here")
                print(new_dict[chore])
                for i in range(len(new_dict[chore])):
                    user_id = new_dict[chore][i][0]
                    print("look here this is the user")
                    print(user_id)
            
                    if user_id not in user_counts or user_counts[user_id]<= int(len_chores / len_users):
                        user_counts[user_id] = user_counts.get(user_id, 0) + 1
                        print(i)
                        print("entered if")
                        print(user_counts)
                        print(user_counts[user_id])
                        db.session.add(UserChore(user_id=new_dict[chore][i][0],  
                            chore=chore, date=day, status="suggested"))
                        db.session.commit() 
                        break
                    else:
                        print("i'm in else")
                        print(i)
                        print(user_counts)
                        print(user_counts[user_id])
                        continue
        elif chore.chore_often =='daily':
            print(chore)
            print("down :here")
            print(new_dict[chore])
            for i in range(len(new_dict[chore])):
                user_id = new_dict[chore][i][0]
                print("look here this is the user")
                print(user_id)
            
                if user_id not in user_counts or user_counts[user_id]<= int(len_chores / len_users):
                    user_counts[user_id] = user_counts.get(user_id, 0) + 1
                    print(i)
                    print("entered if")
                    print(user_counts)
                    print(user_counts[user_id])
                    db.session.add(UserChore(user_id=new_dict[chore][i][0],  
                            chore=chore, date=day, status="suggested"))
                    db.session.commit() 
                    break
                else:
                    print("i'm in else")
                    print(i)
                    print(user_counts)
                    print(user_counts[user_id])
                    continue

def assign_man_sim():
    # mandatory simulteniusly
    chores = Chore.query.filter(Chore.is_mandatory==True, 
                Chore.is_simultaneously==True).order_by(Chore.min_age).all()
    for chore in chores:
        # quering all kids that are age appropriate for the chore
        users = User.query.filter(User.age>= chore.min_age, 
                            User.group=='kids').order_by(User.age).all()
        if chore.chore_often == 'daily':
            for user in users:
                db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status='assigned'))      
                db.session.commit()
                                      
                # chore is twice a week and simuteniusly and mandatory
        elif chore.chore_often == 'by_weekly':
                # checking if is it tuesday ot friday
            if day.weekday() in [2, 5]:
                for user in users:
                    # add record and go to the next user in the same day
                     db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status='assigned'))
                            
            # chore is homework  simuteniusly mandatory
            elif chore.chore_often == 'homework':
                if day.weekday() in [1, 2, 3,  4,5]:
                    for user in users:
                        # add record and go to the next user in the same day
                        db.session.add(UserChore(user=user), 
                                    chore=chore, date=day, status='assigned')
                            
            # chore is weekly and simuteniusly mandatory
            elif chore.chore_often == 'weekly':
                if day.weekday() == 5:
                    for user in users:
                        # add record and go to the next user in the same day
                        db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status='assigned'))                        
                           

    db.session.commit()

def assign_vol_sim():
    chores = Chore.query.filter(Chore.is_mandatory==False, 
                Chore.is_simultaneously==True).order_by(Chore.min_age).all()
    for chore in chores:
        # quering all kids that are age appropriate for the chore
        users = User.query.filter(User.age>= chore.min_age, 
                            User.group=='kids').order_by(User.age).all()
        if chore.chore_often == 'daily':
            for user in users:
                db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status='suggested'))      
                                              
        elif chore.chore_often == 'by_weekly':
                # checking if is it tuesday ot friday
            if day.weekday() in [2, 5]:
                for user in users:
                    # add record and go to the next user in the same day
                    db.session.add(UserChore(user=user, 
                                    chore=chore, date=day, status='suggested'))
             
        
        elif chore.chore_often == 'weekly':
            if day.weekday() == 5:
                for user in users:
                        # add record and go to the next user in the same day
                    db.session.add(UserChore(user=user, 
                            chore=chore, date=day, status='suggested'))                        
                           

    db.session.commit()   


