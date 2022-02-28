import os
import random
from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required,current_user
from .models import User,Blog,Project
from . import db
from werkzeug.utils import secure_filename

 
views = Blueprint('views',__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            
@views.route('/')
def home():
    return render_template("home.html", user=current_user)
# projects
@views.route('/projects')
def projects():
    projects = Project.query.order_by(Project.id)
    return render_template("projects.html", user=current_user,projects=projects)

@views.route('/project/<int:id>')
def show_project(id):
    project = Project.query.get_or_404(id)
    return render_template("show_project.html", user=current_user,project=project)

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
            message ="The Project Title is Not long eoungh!"
        elif len(project_status) < 4:
            message ="please specify the current Project Status clearly!"
        elif len(project_description) < 4:
            message ="The Project Description is Not long eoungh!"
        elif len(project_content) < 4:
            message ='You need to write more details about the project!'
        elif len(project_github) < 4:
            message ='You need to link to the project on GitHub!'
        elif project_img.filename == '':
                message ='Sellect an image for the project!' 
        else:
            if project_img and allowed_file(project_img.filename):
                filename = secure_filename(project_img.filename)
                file_key = random.randint(5,100000000)
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
        
    return render_template("add_project.html", user=current_user, message=message)

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
            message ="The Project Title is Not long eoungh!"
        elif len(project_status) < 4:
            message ="please specify the current Project Status clearly!"
        elif len(project_description) < 4:
            message ="The Project Description is Not long eoungh!"
        elif len(project_content) < 4:
            message ='You need to write more details about the project!'
        elif len(project_github) < 4:
            message ='You need to link to the project on GitHub!'
        elif project_img.filename == '':
                message ='Sellect an image for the project!' 
        else:
            if project_img and allowed_file(project_img.filename):
                filename = secure_filename(project_img.filename)
                file_key = random.randint(5,100000000)
                filename = str(file_key)+"_"+filename
                os.remove(os.path.join('app/static/img/', str(project.project_img)))
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
    return render_template("edit_project.html", user=current_user,message=message,project=project)

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
    return render_template("blogs.html", user=current_user,blogs=blogs)

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
                file_key = random.randint(5,100000000)
                filename = str(file_key)+"_"+filename
                blog_cover.save(os.path.join('app/static/img/', filename))
            new_blog = Blog(blog_title=blog_title, blog_content=blog_content,blog_cover=filename)
            db.session.add(new_blog)
            db.session.commit()
            message = "The blog added successfully"
            return redirect(url_for('views.blogs'))
    return render_template("add_blog.html", user=current_user, message=message)

@views.route('/blog/<int:id>')
def show_blog(id):
    blog = Blog.query.get_or_404(id)
    return render_template("show_blog.html", user=current_user,blog=blog)

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
            message = "Select an image from You blog!"
        else:
            if blog_cover and allowed_file(blog_cover.filename):
                filename = secure_filename(blog_cover.filename)
                file_key = random.randint(5,100000000)
                filename = str(file_key)+"_"+filename
                os.remove(os.path.join('app/static/img', str(blog.blog_cover)))
                blog_cover.save(os.path.join('app/static/img/', filename))
            blog.blog_title = blog_title
            blog.blog_content = blog_content
            blog.blog_cover = filename
            db.session.add(blog)
            db.session.commit()
            return redirect(url_for('views.blogs'))
    return render_template("edit_blog.html", user=current_user,blog=blog,message=message)



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
    return render_template("about.html", user=current_user)


@views.route('/contact')
def contact():
    return render_template("contact.html", user=current_user)
