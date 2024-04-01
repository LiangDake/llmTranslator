
from localbin import app, db

from flask import redirect, url_for, render_template
from flask import request, session
from flask import flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from localbin.auth.forms import UserFormLogin, UserFormRegister
from localbin.auth.models import User
from flask import Blueprint

# Defining a blueprint
auth = Blueprint( 'auth', __name__, template_folder='../templates/auth', static_folder='../static/styles' )

# Register user
@auth.route("/register", methods=["GET", "POST"])
def register():
    """
    This view registers new user and handles validation.
    
    If form is validated and submited.
    First it checks if there is user with this name in db and if passwords match.
    
    Then for security the password is handled by
    :werkzeug.security.generate_password_hash()
    
    Then new user is created with the credentials specified
    We add it to the database.
    """
    
    form = UserFormRegister()
    
    if request.method == "POST":
        # Register user if form is submited and is valid
        if form.validate() and form.is_submitted:
            register_user = form.username.data
            user_password = form.password.data
            confirm_password = form.confirm_password.data
            
            # Check if user exists
            user = User.query.filter_by(username=register_user).first()
            if user:
                flash(f"User with name '{register_user}' already exists!", category='error')
                return redirect("auth.register")
                
            # Validate that passwords match
            if user_password != confirm_password:
                flash("Passwords dont match!")
                return redirect("auth.register")
            
            # Hash
            hash_password = generate_password_hash(user_password, method="scrypt", salt_length=16)
            
            # Init new User
            new_user = User(
                username=register_user,
                password =hash_password
            )
            
            # Add to db
            db.session.add(new_user)
            db.session.commit()
            
            flash("Registration succes! Proceed with loging in!")
            return redirect(url_for("login"))
        
        redirect(url_for("auth.register"))
    
    return render_template("register.html", form=form)

# Login user
@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login after form validation and submission
    """
    form = UserFormLogin()
    if request.method == "POST":
        if  form.validate() and form.is_submitted:
            
            login_username = form.username.data
            login_password = form.password.data
            
            user = User.query.filter_by(username=login_username).first()
            wrong_credentials_error = "Incorect username or password!"
            
            if not user:
                flash(wrong_credentials_error)
                return redirect(url_for("auth.login"))
            
            if not check_password_hash(user.password, login_password):
                flash(wrong_credentials_error)
                return redirect(url_for("/auth.login"))
                
            login_user(user)
            session["user"] = user.username
            
            flash("Login success!")
            return redirect(url_for('core.index')) 
          
    return render_template("login.html", form=form)

# Logout user
@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """
    Logout users and clear session
    """
    logout_user()
    session.clear()
    flash("Logged out!")
    return redirect("auth.login")