from . import db
from flask_login import UserMixin
from sqlalchemy import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(300), unique=True)
    password = db.Column(db.String(400))


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(900))
    blog_cover = db.Column(db.String(900))
    blog_content = db.Column(db.String(1000000000000000000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_title = db.Column(db.String(900))
    project_status = db.Column(db.String(900))
    project_img = db.Column(db.String(900))
    project_github = db.Column(db.String(2000))
    project_description = db.Column(db.String(1000))
    project_content = db.Column(db.String(10000000000000))


class Freelancejobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(900))
    job_status = db.Column(db.String(900))
    job_img = db.Column(db.String(900))
    amount_made = db.Column(db.String(2000))
    job_description = db.Column(db.String(1000))
    quoted_review = db.Column(db.String(1000))
    client_name = db.Column(db.String(1000))


class Testimonials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    testimonial_content = db.Column(db.String(20000))
    client_name = db.Column(db.String(900))
    show_home = db.Column(db.String(900))


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(2000))
    email = db.Column(db.String(900))
    message_content = db.Column(db.String(50000))
    message_purpose = db.Column(db.String(900))
    message_status = db.Column(db.String(900))
    archive = db.Column(db.String(900))
