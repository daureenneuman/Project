"""Models and database functions for Chores project."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from collections import defaultdict

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

#vlue for chore_often
class Chore(db.Model):
    """Chores """

    __tablename__ = "chores"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.String(300), nullable=False)
    abr = db.Column(db.String(15), nullable=False)
    is_mandatory = db.Column(db.Boolean, nullable=False)
    min_age = db.Column(db.Integer, nullable=True)
    chore_often = db.Column(Enum('daily', 'homework', 'weekly', 'by_weekly', 'voluntary as needed', name='chore_often'), default='voluntary as needed')
    reward = db.Column(db.Integer, nullable=True)
    is_simultaneously = db.Column(db.Boolean, default =False)
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"< Description: {self.description}, {self.chore_often}, {self.min_age}, {self.is_mandatory}>"


class User(db.Model):
    """Users"""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group = db.Column((Enum('kids', 'parents', name='group')), default='kids')
    password = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    user_name = db.Column(db.String(15), nullable=False)
    google_account = db.Column(db.String(40), nullable=True)
    google_acccount_password = db.Column(db.String(30), nullable=True)
    is_admin = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User name: {self.user_name} Age: {self.age} Id: {self.id}>"


class UserChore(db.Model):
    """Chores Types"""

    __tablename__ = "users_chores"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    chore_id =  db.Column(db.Integer, db.ForeignKey('chores.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    date = db.Column(db.DateTime, nullable=False)
    status =  db.Column(Enum('suggested', 'in_process', 'done', 'assigned', name='status'))
    reason = db.Column(db.String(100), nullable=True)

    chore = db.relationship("Chore",
                           backref=db.backref("users_chores", order_by=id) , uselist=False)

    user = db.relationship("User",
                           backref=db.backref("users_chores", order_by=id))

    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"< User: {self.user_id} Chores: {self.chore_id} Date: {self.date}>"


class UserReward(db.Model):
    """Chores Types"""

    __tablename__ = "user_rewards"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    reward = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User",
                           backref=db.backref("user_rewards", order_by=id))

    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"< User: {self.user_id} Reward id: {self.reward_id} Date: {self.date}>"



class UserBalance(db.Model):
    """Chores Types"""

    __tablename__ = "user_balances"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    balance =  db.Column(db.Integer, nullable=True)
    Last_update = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User",
                           backref=db.backref("user_balances", order_by=id))

    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"< User: {self.user_id} Balancr: {self.balance} Date: {self.Last_update}>"



class Comment(db.Model):
    """Comments"""
    __tablename__ = "comments"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment = db.Column(db.String(300), nullable=False)
    
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"< Comment: {self.comment} Id: {self.id}>"
   
    

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///chores'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")

    db.create_all()