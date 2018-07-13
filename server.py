"""Chores Project."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Reward, Chore, Comment, Status, Group,User, UserChore, UserReward, UserBalance, Reason, ChoreType


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage Login+Add-users."""
   
    return render_template("homepage.html")


@app.route('/chores')
def show_chores():
   
    chores = Chore.query.all()
    add_chore = request.args.get('add_chore')
    return render_template("show_chores.html", chores=chores, add_chore=add_chore)



@app.route('/process_add_chore', methods=["POST"])    
def process_add_chore():
    description= request.form["description"]    
    chore = Chore(description= description)
    db.session.add(chore)
    db.session.commit()
    

    return redirect("/chores")



@app.route('/rewards')
def show_rewards():
   
    rewards = Reward.query.all()
    add_reward = request.args.get('add_reward')

    return render_template("show_rewards.html", rewards=rewards, add_reward=add_reward)



@app.route('/process_add_reward', methods=["POST"])    
def process_add_reward():
    description= request.form["description"] 
    points= request.form["points"] 
    reward = Reward(description= description, points=points)
    db.session.add(reward)
    db.session.commit()
    

    return redirect("/rewards")


@app.route('/reasons')
def show_reasons():
   
    reasons = Reason.query.all()
    add_reason = request.args.get('add_reason')

    return render_template("show_reasons.html", reasons=reasons, add_reason=add_reason)



@app.route('/process_add_reason', methods=["POST"])    
def process_add_reason():
    description= request.form["description"] 
    reason = Reason(description= description)
    db.session.add(reason)
    db.session.commit()
    

    return redirect("/reasons")



@app.route("/")
def go_to_login():
    return redirect("/login")

@app.route("/login")
def login_form():
    return render_template("homepage.html")


@app.route("/process_login", methods=["POST"])
def login_process():
    name = request.form["name"]
    password = request.form["password"]
    user = User.query.filter(User.user_name == name, User.password==password).first()
    
    if user:
        session["user_name"] = user.user_name
        flash("You are looged in")
        if user.is_admin:
            session["admin"] = True
        return redirect("/chores")

    else:
        flash("Wrong name or password Please try again")
        return redirect("/login")
      
    
@app.route("/logout")
def logout():
    if "user_name" in session:
        session.clear()
        flash("Logged Out!")
    
    return redirect("/")




















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
