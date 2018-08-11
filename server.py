"""Chores Project."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update, desc, func
from model import connect_to_db, db, Chore, Comment, User, UserChore, UserReward, DiaryLog, UserMessage
from datetime import date, timedelta
from quickstart import service
from email.mime.text import MIMEText
from sqlalchemy import func
from apiclient import errors
from apiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload
from quickstart import service
import requests
import json
import io
from engine import show_chores, craeting_chore_dictionary, creating_child_dictionary
from datetime import datetime
from engine import show_chores
from quickstartgemail  import service_gemail
import base64
from seed0 import send_message, create_message
from random import choice, shuffle, random



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined
day = date.today()

@app.route('/')
def index():
    """Homepage Login+Add-users."""
    session.clear() 
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
    
    if user.is_admin:
        session["user.name"] = user.user_name
        session["admin"] = True
        return redirect("/admin")

    elif user.group=='kids':
        session["user.id"] = user.id
        session["user.name"] = user.user_name
        return redirect('/user-chores') 
        
    else:
        flash("Wrong name or password Please try again")
        return redirect("/")

@app.route("/admin")
def show_admin_page():
    messages = UserMessage.query.filter(UserMessage.status == 'open').all()
    from_date = date.today() 
    to_date = date.today() 

    return render_template('admin.html', messages=messages,
                    from_date=from_date, to_date=to_date)




@app.route('/user-chores')
def show_user_chores():
    if "user.id" not in session:
        return redirect('/')
    else:

        day = date.today()
        user = User.query.filter(User.id == session["user.id"]).one()
        userchores = UserChore.query.filter(UserChore.user_id == user.id, 
                    UserChore.date==day, UserChore.status != "done").all()
        chores_vols = Chore.query.filter(Chore.is_mandatory == False).all()
        chores_mans = Chore.query.filter(Chore.is_mandatory == True, Chore.id != 2).all()
        chore_diary = Chore.query.filter(Chore.id == 2).one()
        
        userchores_man_list = []
        userchores_vol_list = []
        userchore_diary =""
        for userchore in userchores:
            if userchore.chore == chore_diary:
                userchore_diary = userchore
            elif userchore.chore in chores_mans:
                userchores_man_list.append(userchore)
            else:
                userchores_vol_list.append(userchore)


        user_balance_rec = db.session.query(UserReward.user_id, func.sum(UserReward.reward)).filter(
            UserReward.user_id == user.id).group_by(UserReward.user_id).first()
        user_balance = user_balance_rec[1]

        session["balance"] = user_balance
        
        return render_template("show_chores.html", userchores_vols=userchores_vol_list, 
                    userchores_mans=userchores_man_list, user=user, userchore_diary= userchore_diary)


@app.route('/process-chores', methods=["POST", "GET"])
def show_process_chores():
    
    if "user.id" not in session:
        return redirect('/')
    else:
        chore_id = request.form.get("choreid")
        user_id = session["user.id"] 
        day = date.today()
        rec = UserChore.query.filter(UserChore.user_id == user_id, 
                UserChore.date==day, UserChore.chore_id==chore_id).first()
        rec.status = 'done'
        if rec.chore.reward:
                db.session.add(UserReward(user=rec.user, 
                                    reward = rec.chore.reward, date= day))
        db.session.commit()
        recs_man = UserChore.query.filter(UserChore.user_id == user_id, UserChore.chore.has(is_mandatory=True), 
                UserChore.date==day, UserChore.status != 'done',UserChore.chore_id !=2).all()
        recs_vol = UserChore.query.filter(UserChore.user_id == user_id, UserChore.chore.has(is_mandatory =False), 
                UserChore.date==day, UserChore.status != 'done').all()
        num_rec_man= len(recs_man)
        num_rec_vol= len(recs_vol)
        if num_rec_man==0:
            lastman ="yes"
        else:
            lastman ="no"

        if num_rec_vol==0:
            lastvol ="yes"
        else:
            lastvol ="no"
        return jsonify({'status': 'ok', 'chore': chore_id, 'lastman': lastman, 'lastvol': lastvol})


@app.route('/show-balance')
def calculate_user_balance():

    if "user.id" not in session:
        return redirect('/')
    else:
        user = session["user.id"]
        user_balance_rec = db.session.query(UserReward.user_id, func.sum(UserReward.reward)).filter(
            UserReward.user_id == user).group_by(UserReward.user_id).first()
        user_balance = user_balance_rec[1]
        session["balance"] = user_balance
        return redirect('/user-chores')


@app.route('/update-session-balance', methods=["POST"])
def update_user_balance():
    if "balance" in session:
        reward = request.form.get("reward")
        reward= int(reward)
        session["balance"] += reward
        return jsonify({'status': 'ok', 'balance': session["balance"]})
    else:
         return jsonify({'status': 'nosession'})



@app.route('/clear-balance')
def hide_balance():
    if "user.id" not in session:
        return redirect('/')
    else:
        session.pop("balance", None)
    
    
    return redirect('/user-chores')


@app.route("/user/diary")
def show_diary_form():
    session["diary"] = True
    
    return render_template("diary.html")


@app.route('/save-diary', methods=["POST"])
def save_diary():
    content = request.form["content"]
    user = User.query.filter(User.id == session["user.id"]).one()
    day = date.today()

    #status  update in users_chores
    db.session.add(DiaryLog(user = user, date = day, content = content))
    db.session.commit()
    rec = UserChore.query.filter(UserChore.user == user, 
                UserChore.date==day, UserChore.chore_id==2).first()
    rec.status = "done"
    db.session.commit()
    #quering all user logs
    text = ""
    day = None
    logs = DiaryLog.query.filter(DiaryLog.user == user).order_by(DiaryLog.id).all()
    for log in logs:
        day = log.date
        text = text + "\n\n" + str(day) + "\n" +log.content 
        
    drive_file_id =  user.drive_file
    drive_file_name = user.drive_name
    fh  = io.BytesIO(text.encode())
    media = MediaIoBaseUpload(fh, mimetype='text/plain')
    file_meta_data = {
    'name': drive_file_name, 
    'mimeType' : 'application/vnd.google-apps.document'
    }
    updated_file = service.files().update(
        body=file_meta_data,
        #uploadType = 'media',
        fileId=drive_file_id,
        #fields = fileID,
        media_body=media).execute()

    session.pop('diary', None)
    return redirect('/user-chores')



@app.route('/add/chores')
def show_chores():
    if "admin" in session:
        mans = Chore.query.filter(Chore.is_mandatory ==True).all()
        vols = Chore.query.filter(Chore.is_mandatory ==False).all()
       
        return render_template("all_chores.html", mans=mans, vols=vols)
    else:
        flash("You are not authorized to access admin pages")
        return redirect('/')
   
@app.route('/admin-new-chore', methods=["POST"])
def update_chore():
    description = request.form.get("desc")
    min_age = request.form.get("age")
    is_man = ('true' == request.form.get("must"))
    is_sim = ('true' == request.form.get("sim"))
    often = request.form.get("often")
    chore =  Chore.query.filter(Chore.description == description).first()
    if chore:
   
        chores = Chore.query.all()
        return render_template("all_chores.html", chores=chores)
    else:
        chore = Chore(description=description, is_mandatory= is_man, 
        min_age=min_age, chore_often=often, reward=0, is_simultaneously=is_sim)
        db.session.add(chore)
        db.session.commit() 
        desc=chore.description
        return jsonify({'status': 'ok', "desc": desc})

@app.route('/send')
def send_mail():
    message_text = "pay {} {}$".format(session["user.name"], session["balance"])
    subject = "{} balance".format(session["user.name"])
    message = create_message(sender= 'daureenn@gmail.com', to = 'daureenn@gmail.com', 
    subject=subject,  message_text=message_text)
    send_message(service_gemail,'me', message)
    user_message = UserMessage.query.filter(UserMessage.from_user_id == session["user.id"], UserMessage.status=='open').first()
    # If there is no open request add to DB 
    if not user_message:
        db.session.add(UserMessage(from_user_id =session["user.id"],
            message=message_text,  date= date.today(), status='open'))
        db.session.commit()

    return jsonify({'status': 'ok'})

@app.route('/process-payment', methods=["POST"])
def reedem_balance():
    # add record in negative to user_log update status in message to close
    mesid = request.form.get("mesid")
    user_mes = UserMessage.query.filter(UserMessage.id ==mesid).one()
    user_id = user_mes.from_user_id
    bal_rec = db.session.query(UserReward.user_id, func.sum(UserReward.reward)).filter(
            UserReward.user_id == user_id).group_by(UserReward.user_id).first()
    neg_balance = -bal_rec[1]
    db.session.add(UserReward(user_id =user_id, reward=neg_balance,  date= date.today()))
    db.session.commit()
    user_message_rec = UserMessage.query.filter(UserMessage.from_user_id == user_id, 
                    UserMessage.status=='open').one()
    user_message_rec.status='close'
    db.session.commit()

    return jsonify({'status': 'ok', 'mesid': mesid})

@app.route('/admin-today')
def show_today_chorse():
    sim_mans = UserChore.query.filter(UserChore.chore.has(is_mandatory=True, is_simultaneously=True),UserChore.date==date.today()).all()
    turn_vols = UserChore.query.filter(UserChore.chore.has(is_mandatory =False, is_simultaneously=False), UserChore.date==date.today()).all()
    turn_mans =  UserChore.query.filter(UserChore.chore.has(is_mandatory=True, is_simultaneously=False),UserChore.date==date.today()).all()
    sim_vols =  UserChore.query.filter(UserChore.chore.has(is_mandatory=False, is_simultaneously=True),UserChore.date==date.today()).all()
    
    users = User.query.filter(User.group=='kids').order_by(User.age).all()

    return render_template("todays_chores.html", sim_mans=sim_mans, turn_vols=turn_vols, turn_mans=turn_mans, sim_vols=sim_vols,users=users)


@app.route('/admin-report', methods=["POST", "GET"])
def expiriment():
    colors = ["#8FD8D8", "#37FDFC", "#39B7CD", "#0D4F8B", "#191970", "#6959CD", "#9370DB", "#40e0d0"]
    color_list = []
    from_date =request.form["start"]
    print(from_date)
    to_date = request.form["finish"]
    print(to_date)
    users = User.query.filter(User.group=='kids').all()
    dict_user = {}
    i=0
    for user in users:
        rec_done = db.session.query(func.count(UserChore.id)).filter(UserChore.date>= from_date, 
           UserChore.date<= to_date,  UserChore.user == user, UserChore.status == 'done', UserChore.chore_id!=2).one()
        count_done= rec_done[0]
        rec_undone = db.session.query(func.count(UserChore.id)).filter(UserChore.date>= from_date, 
           UserChore.date<= to_date, UserChore.user == user, UserChore.status != 'done', UserChore.chore_id!=2).one()
        count_undone= rec_undone[0]
        color = colors[i]
        i = +1
        color_list.append(color)
        
        if count_undone+count_done>0:
            per_done = 100*(float(count_done)/(count_done+count_undone))
            per_done = int(per_done)
            dict_user[user.user_name] = per_done
        else:
            dict_user[user] = 0
    labels = dict_user.keys()
    values = dict_user.values()  
    return render_template("report.html", values=values, labels=labels, colors=colors)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
