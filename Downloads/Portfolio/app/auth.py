from flask import Blueprint,render_template,request,flash,redirect,url_for
from numpy import repeat
from .models import User
from . import db
from flask_login import login_user,login_required,logout_user,current_user

from werkzeug.security import generate_password_hash,check_password_hash
 
auth = Blueprint('auth',__name__)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if email == "":
            message = "Please enter your email address"
        elif password == "":
            message = "Please enter your password"
        else:
            if user:
                if check_password_hash(user.password,password):
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    message ='E-mail or password incorrect!'
            else:
                message = 'This user does not exist!'
                
        
    return render_template('login.html',message=message)

@auth.route('/logout')
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/login-info',methods=['GET', 'POST'])
@login_required
def login_info():
    user = User.query.get(current_user.id)
    message = None
    message_s = None
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        repeat_password = request.form.get('repeat_password')
        if len(email) < 4:
            message = "You sould enter an E-mail to update your info"
        elif new_password != repeat_password:
            message = "The new password does not match repeat password"
        else:
            user.email = email
            user.password = generate_password_hash(new_password, method='sha256')
            db.session.add(user)
            db.session.commit()
            message_s = "You change you login information successfully!"
            
    return render_template('login_info.html',message=message,user=user,message_s=message_s)
            