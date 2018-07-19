"""Chores Project."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from model import connect_to_db, db, Chore, Comment, User, UserChore, UserReward
from datetime import date, timedelta
from quickstart import service
from sqlalchemy import func

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined
day = date.today()

@app.route('/')
def index():
    """Homepage Login+Add-users."""
   
    return render_template("homepage.html")


@app.route("/logout")
def logout():
    session.clear() 
    flash("Logged Out!")
    
    return redirect("/")


# processing Login
@app.route("/process_login", methods=["POST"])
def login_process():
    session.clear() 
    name = request.form["name"]
    password = request.form["password"]
    user = User.query.filter(User.user_name == name, User.password==password).first()
    
    if user:
        session["user.id"] = user.id
        flash("You are looged in")
        if user.is_admin:
            session["admin"] = True
        return redirect('/user-chores')

    else:
        flash("Wrong name or password Please try again")
        return redirect("/")


@app.route('/user-chores')
def show_user_chores():
    
    if "user.id" not in session:
        return redirect('/')
    else:

        print("Hello you are in show user function")
        print(session["user.id"])
        day = date.today()
        user = User.query.filter(User.id == session["user.id"]).one()
        print(user)
        userchores = UserChore.query.filter(UserChore.user_id == user.id, UserChore.date==day).all()
        print(user, userchores)
        chores_vols = Chore.query.filter(Chore.is_mandatory == False).all()
        chores_mans = Chore.query.filter(Chore.is_mandatory == True, Chore.abr != "diary").all()
        chore_diary = Chore.query.filter(Chore.abr == "diary").one()
        print(chores_vols)
        userchores_man_list = []
        userchores_vol_list = []
        for userchore in userchores:
             if userchore.chore in chore_diary:
                userchore_diary = userchore
            print(userchore)
            elif userchore.chore in chores_mans:
                userchores_man_list.append(userchore)
            else:
                userchores_vol_list.append(userchore)

        
        return render_template("show_chores.html", userchores_vols=userchores_vol_list, 
                    userchores_mans=userchores_man_list, user=user, userchore_diary= userchore_diary)


@app.route('/process-chores', methods=["POST", "GET"])
def show_process_chores():
    
    print("process chores func")
    if "user.id" not in session:
        return redirect('/')
    else:
        chore_ids = request.form.getlist("chore_id")
        for chore_id in chore_ids:
            status=request.form["status-"+chore_id]
            print(status)
            if status == "done":
                print(chore_id, status)
                rec = UserChore.query.filter(UserChore.user_id == session["user.id"], 
                UserChore.date==day, UserChore.chore_id==chore_id).first()
                print(rec)
                rec.status = status
                db.session.commit()
        return redirect('/user-chores')


@app.route('/show-balance')
def calculate_user_balance():

    if "user.id" not in session:
        return redirect('/')
    else:
        user = session["user.id"]
        user_balance_rec = db.session.query(UserReward.user_id, func.sum(UserReward.reward)).filter(
            UserReward.user_id == user).group_by(UserReward.user_id).first()
        user_balance = user_balance_rec[1]
        print(user_balance)

        session["balance"] = user_balance
        return redirect('/user-chores')

@app.route('/clear-balance')
def hide_balance():
    if "user.id" not in session:
        return redirect('/')
    else:
        session.pop("balance", None)
    
    
    return redirect('/user-chores')


























# @app.route('/process_add_chore', methods=["POST"])    
# def process_add_chore():
#     description= request.form["description"]    
#     chore = Chore(description= description)
#     db.session.add(chore)
#     db.session.commit()
    

#     return redirect("/chores")



# @app.route('/rewards')
# def show_rewards():
   
#     rewards = Reward.query.all()
#     add_reward = request.args.get('add_reward')

#     return render_template("show_rewards.html", rewards=rewards, add_reward=add_reward)



# @app.route('/process_add_reward', methods=["POST"])    
# def process_add_reward():
#     description= request.form["description"] 
#     points= request.form["points"] 
#     reward = Reward(description= description, points=points)
#     db.session.add(reward)
#     db.session.commit()
    

#     return redirect("/rewards")


# @app.route('/reasons')
# def show_reasons():
   
#     reasons = Reason.query.all()
#     add_reason = request.args.get('add_reason')

#     return render_template("show_reasons.html", reasons=reasons, add_reason=add_reason)



# @app.route('/process_add_reason', methods=["POST"])    
# def process_add_reason():
#     description= request.form["description"] 
#     reason = Reason(description= description)
#     db.session.add(reason)
#     db.session.commit()
    

#     return redirect("/reasons")



# @app.route("/")
# def go_to_login():
#     return redirect("/login")

# @app.route("/login")
# def login_form():
#     return render_template("homepage.html")






















################################################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
