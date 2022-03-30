import os
import random
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Testimonials, User, Blog, Project, Freelancejobs, Contact
from . import db
from werkzeug.utils import secure_filename
from captcha.image import ImageCaptcha
import time


views = Blueprint('views', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def captcha():
    num = random.randint(1000, 9999)
    image = ImageCaptcha()
    tstr = time.strftime("%Y%m%d-%H%M%S")
    image.write(str(num), f'app/static/img/{tstr}.png')
    return num, tstr


def messages_count():
    messages = Contact.query.filter_by(message_status='unread').count()
    return messages


@views.route('/')
def home():
    testimonials = Testimonials.query.filter_by(
        show_home='yes')
    return render_template("home.html", user=current_user, messages=messages_count(), testimonials=testimonials)

# projects


@views.route('/projects')
def projects():
    projects = Project.query.order_by(Project.id)
    return render_template("projects.html", user=current_user, projects=projects, messages=messages_count())


@views.route('/project/<int:id>')
def show_project(id):
    project = Project.query.get_or_404(id)
    return render_template("show_project.html", user=current_user, project=project, messages=messages_count())


@views.route('/add-project', methods=['GET', 'POST'])
@login_required
def add_project():
    message = None
    if request.method == 'POST':
        project_title = request.form.get('project_title')
        project_status = request.form.get('project_status')
        project_description = request.form.get('project_description')
        project_content = request.form.get('project_content')
        project_github = request.form.get('project_github')
        project_img = request.files['project_img']

        if len(project_title) < 4:
            message = "The Project Title is Not long eoungh!"
        elif len(project_status) < 4:
            message = "please specify the current Project Status clearly!"
        elif len(project_description) < 4:
            message = "The Project Description is Not long eoungh!"
        elif len(project_content) < 4:
            message = 'You need to write more details about the project!'
        elif len(project_github) < 4:
            message = 'You need to link to the project on GitHub!'
        elif project_img.filename == '':
            message = 'Sellect an image for the project!'
        else:
            if project_img and allowed_file(project_img.filename):
                filename = secure_filename(project_img.filename)
                file_key = random.randint(5, 100000000)
                filename = str(file_key)+"_"+filename
                project_img.save(os.path.join('app/static/img/', filename))
            new_project = Project(project_title=project_title,
                                  project_status=project_status,
                                  project_description=project_description,
                                  project_content=project_content,
                                  project_github=project_github,
                                  project_img=filename
                                  )
            db.session.add(new_project)
            db.session.commit()
            flash("The Project was Added successfully", category='success')
            return redirect(url_for("views.projects"))

    return render_template("add_project.html", user=current_user, message=message, messages=messages_count())


@views.route('/project/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    message = None
    if request.method == 'POST':
        project_title = request.form.get('project_title')
        project_description = request.form.get('project_description')
        project_status = request.form.get('project_status')
        project_content = request.form.get('project_content')
        project_github = request.form.get('project_github')
        project_img = request.files['project_img']
        if len(project_title) < 4:
            message = "The Project Title is Not long eoungh!"
        elif len(project_status) < 4:
            message = "please specify the current Project Status clearly!"
        elif len(project_description) < 4:
            message = "The Project Description is Not long eoungh!"
        elif len(project_content) < 4:
            message = 'You need to write more details about the project!'
        elif len(project_github) < 4:
            message = 'You need to link to the project on GitHub!'
        elif project_img.filename == '':
            message = 'Sellect an image for the project!'
        else:
            if project_img and allowed_file(project_img.filename):
                filename = secure_filename(project_img.filename)
                file_key = random.randint(5, 100000000)
                filename = str(file_key)+"_"+filename
                os.remove(os.path.join('app/static/img/',
                          str(project.project_img)))
                project_img.save(os.path.join('app/static/img/', filename))
            project.project_title = project_title
            project.project_description = project_description
            project.project_status = project_status
            project.project_content = project_content
            project.project_github = project_github
            project.project_img = filename
            db.session.add(project)
            db.session.commit()
            return redirect(url_for('views.projects'))
    return render_template("edit_project.html", user=current_user, message=message, project=project, messages=messages_count())


@views.route('/project/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):
    project = Project.query.get(id)
    os.remove(os.path.join('app/static/img/', str(project.project_img)))
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("views.projects"))

# blogs


@views.route('/blog')
def blogs():
    blogs = Blog.query.order_by(Blog.id)
    return render_template("blogs.html", user=current_user, blogs=blogs, messages=messages_count())


@views.route('/add-blog', methods=['GET', 'POST'])
@login_required
def add_blog():
    message = None
    if request.method == 'POST':
        blog_title = request.form.get('blog_title')
        blog_content = request.form.get('blog_content')
        blog_cover = request.files['blog_cover']
        if len(blog_title) < 4:
            message = "The blog title is too short"
        elif len(blog_content) < 4:
            message = "The blog content is too short"
        elif blog_cover.filename == '':
            message = "Select an image from You blog!"
        else:
            if blog_cover and allowed_file(blog_cover.filename):
                filename = secure_filename(blog_cover.filename)
                file_key = random.randint(5, 100000000)
                filename = str(file_key)+"_"+filename
                blog_cover.save(os.path.join('app/static/img/', filename))
            new_blog = Blog(blog_title=blog_title,
                            blog_content=blog_content, blog_cover=filename)
            db.session.add(new_blog)
            db.session.commit()
            message = "The blog added successfully"
            return redirect(url_for('views.blogs'))
    return render_template("add_blog.html", user=current_user, message=message, messages=messages_count())


@views.route('/blog/<int:id>')
def show_blog(id):
    blog = Blog.query.get_or_404(id)
    return render_template("show_blog.html", user=current_user, blog=blog)


@views.route('/blog/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blog(id):
    blog = Blog.query.get_or_404(id)
    message = None
    if request.method == 'POST':
        blog_title = request.form.get('blog_title')
        blog_content = request.form.get('blog_content')
        blog_cover = request.files['blog_cover']
        if len(blog_title) < 4:
            message = "The blog title is too short"
        elif len(blog_content) < 4:
            message = "The blog content is too short"
        elif blog_cover.filename == '':
            message = "Select an image for Your blog!"
        else:
            if blog_cover and allowed_file(blog_cover.filename):
                filename = secure_filename(blog_cover.filename)
                file_key = random.randint(5, 100000000)
                filename = str(file_key)+"_"+filename
                os.remove(os.path.join('app/static/img', str(blog.blog_cover)))
                blog_cover.save(os.path.join('app/static/img/', filename))
            blog.blog_title = blog_title
            blog.blog_content = blog_content
            blog.blog_cover = filename
            db.session.add(blog)
            db.session.commit()
            return redirect(url_for('views.blogs'))
    return render_template("edit_blog.html", user=current_user, blog=blog, message=message, messages=messages_count())


@views.route('/blog/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_blog(id):
    blog = Blog.query.get(id)
    os.remove(os.path.join('app/static/img/', str(blog.blog_cover)))
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for("views.blogs"))


@views.route('/about')
def about():
    return render_template("about.html", user=current_user, messages=messages_count())


# freelance jobs

@views.route('/freelancejobs')
def freelancejobs():
    freelancejobs = Freelancejobs.query.order_by(Freelancejobs.id)
    return render_template("freelancejobs.html", user=current_user, freelancejobs=freelancejobs, messages=messages_count())


@views.route('/add-job', methods=['GET', 'POST'])
@login_required
def add_job():
    message = None
    if request.method == 'POST':
        job_title = request.form.get('job_title')
        job_status = request.form.get('job_status')
        job_img = request.files['job_img']
        amount_made = request.form.get('amount_made')
        job_description = request.form.get('job_description')
        quoted_review = request.form.get('quoted_review')
        client_name = request.form.get('client_name')
        if len(job_title) < 4:
            message = "The jon title is too short"
        elif len(amount_made) < 1:
            message = "Put who much you made on this job"
        elif len(job_status) < 1:
            message = "what is the job status?"
        elif len(job_description) < 4:
            message = "The job description is too short"
        elif len(quoted_review) < 4:
            message = "The Client review is too short"
        elif len(client_name) < 4:
            message = "The Client name is too short"
        elif job_img.filename == '':
            message = "Select an image for the job!"
        else:
            if job_img and allowed_file(job_img.filename):
                filename = secure_filename(job_img.filename)
                file_key = random.randint(5, 100000000)
                filename = str(file_key)+"_"+filename
                job_img.save(os.path.join('app/static/img/', filename))
            new_job = Freelancejobs(job_title=job_title, job_status=job_status,
                                    amount_made=amount_made, client_name=client_name, quoted_review=quoted_review, job_description=job_description, job_img=filename)
            db.session.add(new_job)
            db.session.commit()
            message = "The job added successfully"
            return redirect(url_for('views.freelancejobs'))
    return render_template("add_job.html", user=current_user, message=message, messages=messages_count())


@views.route('/freelancejobs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    freelancejob = Freelancejobs.query.get_or_404(id)
    message = None
    if request.method == 'POST':
        job_title = request.form.get('job_title')
        job_status = request.form.get('job_status')
        job_img = request.files['job_img']
        amount_made = request.form.get('amount_made')
        job_description = request.form.get('job_description')
        quoted_review = request.form.get('quoted_review')
        client_name = request.form.get('client_name')
        if len(job_title) < 4:
            message = "The jon title is too short"
        elif len(amount_made) < 1:
            message = "Put who much you made on this job"
        elif len(job_status) < 1:
            message = "what is the job status?"
        elif len(job_description) < 4:
            message = "The job description is too short"
        elif len(client_name) < 2:
            message = "The job client name is too short"
        elif job_img.filename == '':
            message = "Select an image for the job!"
        else:
            if job_img and allowed_file(job_img.filename):
                filename = secure_filename(job_img.filename)
                file_key = random.randint(5, 100000000)
                filename = str(file_key)+"_"+filename
                job_img.save(os.path.join('app/static/img/', filename))
            freelancejob.job_title = job_title
            freelancejob.job_status = job_status
            freelancejob.amount_made = amount_made
            freelancejob.job_description = job_description
            freelancejob.quoted_review = quoted_review
            freelancejob.client_name = client_name
            freelancejob.job_img = filename
            db.session.add(freelancejob)
            db.session.commit()
            return redirect(url_for('views.freelancejobs'))
    return render_template("edit_job.html", user=current_user, freelancejob=freelancejob, message=message, messages=messages_count())


@views.route('/freelancejobs/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_job(id):
    freelancejob = Freelancejobs.query.get(id)
    os.remove(os.path.join('app/static/img/', str(freelancejob.job_img)))
    db.session.delete(freelancejob)
    db.session.commit()
    return redirect(url_for("views.freelancejobs"))

# Testimonials


@views.route('/testimonials')
def testimonials():
    testimonials = Testimonials.query.order_by(Testimonials.id)
    return render_template("testimonials.html", user=current_user, testimonials=testimonials, messages=messages_count())


@views.route('/add-testimonial', methods=['GET', 'POST'])
@login_required
def add_testimonial():
    message = None
    if request.method == 'POST':
        testimonial_content = request.form.get('testimonial_content')
        client_name = request.form.get('client_name')
        show_home = request.form.get('show_home')
        if len(testimonial_content) < 4:
            message = "The testimonial is too short"
        elif len(client_name) < 4:
            message = "The name is too short"
        else:
            new_testimonial = Testimonials(testimonial_content=testimonial_content,
                                           client_name=client_name, show_home=show_home)
            db.session.add(new_testimonial)
            db.session.commit()
            message = "The testimonial added successfully"
            return redirect(url_for('views.testimonials'))
    return render_template("add_testimonial.html", user=current_user, message=message, messages=messages_count())


@views.route('/testimonials/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_testimonial(id):
    testimonial = Testimonials.query.get_or_404(id)
    message = None
    if request.method == 'POST':
        testimonial_content = request.form.get('testimonial_content')
        client_name = request.form.get('client_name')
        show_home = request.form.get('show_home')
        if len(testimonial_content) < 4:
            message = "The testimonial is too short"
        elif len(client_name) < 4:
            message = "The name is too short"
        else:
            testimonial.testimonial_content = testimonial_content
            testimonial.client_name = client_name
            testimonial.show_home = show_home
            db.session.add(testimonial)
            db.session.commit()
            return redirect(url_for('views.testimonials'))
    return render_template("edit_testimonial.html", user=current_user, testimonial=testimonial, message=message, messages=messages_count())


@views.route('/testimonials/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_testimonial(id):
    testimonial = Testimonials.query.get(id)
    db.session.delete(testimonial)
    db.session.commit()
    return redirect(url_for("views.testimonials"))

# message system


@views.route('/contact', methods=['GET', 'POST'])
def message():
    global num1
    global tstr
    message = None
    m_type = None
    if request.method == "GET":
        num1, tstr = captcha()
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        message_content = request.form.get('message_content')
        message_purpose = request.form.get('message_purpose')
        ip = request.form["ip"]
        message_status = "unread"
        archive = "no"
        if len(full_name) < 4:
            message = "Your Full Name please!"
            m_type = "is-danger"
        elif "@" not in email:
            message = "Enter a valid email address"
            m_type = "is-danger"
        elif len(ip) < 1:
            message = "The Captcha field is empty!"
            m_type = "is-danger"
        elif ip != str(num1):
            message = "The Captcha code is Wrong!"
            m_type = "is-danger"
        elif message_content == "":
            message = "The message conetnt is too short"
            m_type = "is-danger"
        else:
            new_message = Contact(full_name=full_name,
                                  email=email, message_purpose=message_purpose,
                                  message_status=message_status, archive=archive,
                                  message_content=message_content)
            db.session.add(new_message)
            db.session.commit()
            message = "The message was sent successfully, You will hear from me soon!"
            m_type = "is-success"
            num1, tstr = captcha()
    return render_template("contact.html", tstr=tstr, user=current_user, message=message, m_type=m_type, messages=messages_count())


@views.route('/inbox')
@login_required
def inbox():
    freelance_jobs = Contact.query.filter_by(
        message_purpose='freelance_job', archive="no")
    fulltime_job_offers = Contact.query.filter_by(
        message_purpose='fulltime_job_offer', archive="no")
    consultations = Contact.query.filter_by(
        message_purpose='consultation', archive="no")
    others = Contact.query.filter_by(
        message_purpose='other', archive="no")
    archives = Contact.query.filter_by(
        archive='yes')
    return render_template("inbox.html", user=current_user, freelance_jobs=freelance_jobs,
                           others=others, archives=archives, consultations=consultations, fulltime_job_offers=fulltime_job_offers, messages=messages_count())


@views.route('/message/<int:id>', methods=['GET', 'POST'])
@login_required
def read_message(id):
    message = Contact.query.get_or_404(id)
    if message.message_status == "unread":
        message.message_status = "read"
        db.session.add(message)
        db.session.commit()
    return render_template("read_message.html", user=current_user, message=message, messages=messages_count())


@views.route('/message/archive/<int:id>', methods=['GET', 'POST'])
@login_required
def archive_message(id):
    message = Contact.query.get_or_404(id)
    if message.archive == "no":
        message.archive = "yes"
        db.session.add(message)
        db.session.commit()
    return redirect(url_for("views.inbox"))


@views.route('/message/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_message(id):
    message = Contact.query.get(id)
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for("views.inbox"))
