
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm
from models import db, User
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash("Email already registered")
            return redirect(url_for('register'))

      
        hashed_password = generate_password_hash(form.password.data)

       
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password
        )

        
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful")

        return redirect(url_for('register'))

    return render_template('register.html', form=form)



@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)