from app import *
from app.models import User, Project,Comment, db
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash

import os
from app import Config


# default user

@log_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))



@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index_1.html', title='Antony Injila | Home', projects=projects)

@app.route('/404', methods=['POST', 'GET'])
def feedback():
    return render_template('feedback.html', title='Antony Injila | 404')



# user authentication
@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password1']
        c_password = request.form['password2']
        # check user exists
        # user = User.query.filter_by(email=request.form['email']).first()

        # if user:
        #     flash('User already exists here')
        #     return render_template('signup.html')
        # else:
        if password == c_password:
            user = User(username=name, email=email,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash('User created successfuly')
            return redirect(url_for('login'))
        flash('Password did not match')
        return redirect(url_for('signup'))

    return render_template('signup.html', title="Antony Injila | Signup")


@app.route('/login', methods=['POST','GET'])
def login():
    # collect form data
    if request.method == 'POST':
        # check if empty
        if request.form['email'] == None or request.form['password'] == None:
            return redirect(url_for('login'))
        else:
            user = User.query.filter_by(email= request.form['email']).first()
            # check if password match
            if user is None or not user.check_password(request.form['password']):
                flash('Invalid username or password', 'alert alert-danger')
                return redirect(url_for('login'))
            login_user(user)
            flash('Login successful', 'alert alert-success')
            return redirect(url_for('index'))
    return render_template('login.html', title="Antony Injila | Login")

@app.route("/logout")
def logout():
    logout_user()
    flash('Logout successful', 'alert alert-success')
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    projects = Project.query.all()[:3]
    projects_num = len(projects)
    if request.form and request.files:
        name = request.form.get('name')
        email = request.form.get('email')
        about = request.form.get('about')

        f = request.files['image-file']
        filename = secure_filename(f.filename)
        # location for storing images: Portfolio/static/images/name_of_image
        image_file = "{}/{}/{}".format("static", "images/uploads", filename)
        # image upload
        f.save(os.path.join(app.config["UPLOAD_FOLDER"] + "/uploads", filename))

        user = User(name=name,email=email,about=about,image_file=image_file)
        db.session.add(user)
        db.session.commit()
        user = User.query.get(1)
        return render_template('dashboard.html',title="Antony Injila | Dashboard",user=user )
    user = User.query.get(1)
    count = len(projects)
    return render_template('dashboard.html', title="Antony Injila | Dashboard", user=user,count=count, projects=projects,projects_num = projects_num)


@app.route('/dashboard/update', methods=['GET','POST'])
def dashboard_update():
    projects = Project.query.all()
    user = User.query.get(1)
    projects_num = len(projects)
    if request.method == "POST" or request.files:
        name = request.form.get('name')
        email = request.form.get('email')
        about = request.form.get('about')
        technical_experience = request.form.get('technical_experience')
        recent_activities = request.form.get('recent_activities')
        current_job = request.form.get('current_job')
        educational_background = request.form.get('educational_background')
        profession = request.form.get('profession')
        python = request.form.get('python')
        javascript = request.form.get('javascript')
        java = request.form.get('java')
        django = request.form.get('django')
        flask = request.form.get('flask')
        nodejs = request.form.get('nodejs')
        android = request.form.get('android')
        image_file_old = request.form.get('image-file-old')
        cv_file_old = request.form.get('cv-file-old')

        f_image = request.files['image-file']
        f_cv = request.files['cv-file']

        filename_image = secure_filename(f_image.filename)
        filename_cv = secure_filename(f_cv.filename)

        if filename_image:
            image_file = "{}/{}/{}".format("static", "images/uploads/avaters", filename_image)
            f_image.save(Config.UPLOAD_FOLDER + "/avaters/" + filename_image)
            user.image_file = image_file
            db.session.commit()
        elif filename_cv:
            # location for storing images: Portfolio/static/images/name_of_image
            cv_file = "{}/{}/{}".format("static", "images/uploads/resume", filename_cv)
            # image upload
            f_cv.save(Config.UPLOAD_FOLDER +"/resume/" +filename_cv)
            user.cv_file = cv_file
            db.session.commit()

        else:
            user.name = name
            user.email = email
            user.about = about
            user.technical_experience = technical_experience
            user.recent_activities = recent_activities
            user.current_job = current_job
            user.educational_background = educational_background
            user.profession = profession
            user.python = python
            user.javascript = javascript
            user.java = java
            user.django = django
            user.flask = flask
            user.nodejs = nodejs
            user.android = android
            user.image_file = image_file_old
            user.cv_file = cv_file_old
        # save the new changes
            db.session.commit()
        # return redirect('/project/update/{}/'.format(project_id))
            return redirect(url_for('dashboard'))

    return render_template('dashboard.html', title="Antony Injila | Dashboard update", user=user, projects=projects)





@app.route('/about')
def about():
    user = User.query.get(1)
    return render_template('about.html', title='Antony Injila | About page', user=user)


@app.route('/resume')
def resume():
    user = User.query.get(1)
    resume = user.cv_file
    return render_template('resume.html', title='Antony Injila | Resume page', resume=resume)

# Projects urls and views
@app.route('/projects/add', methods=['GET', 'POST'])
def projects_add():
    projects = Project.query.all()
    if request.method == 'POST':
        name  = request.form['name']
        technologies  = request.form['technologies']
        description  = request.form['description']
        github  = request.form['github']
        youtube  = request.form['youtube']

        # grab imge file
        f = request.files['image-file']
        filename = secure_filename(f.filename)
        image_file=''

        if filename =='':
            image_file = "{}/{}/{}".format("static", "images/uploads/projects", 'default.jpeg')
            # f.save(Config.UPLOAD_FOLDER + "/projects/" + 'default.jpeg')
        # location for storing images: Portfolio/static/images/name_of_image
        else:
            image_file = "{}/{}/{}".format("static", "images/uploads/projects", filename)
            # image upload
            f.save(Config.UPLOAD_FOLDER + "/projects/" + filename)

        new_project = Project(
            name=name,
            technologies=technologies,
            description =description,
            github = github,
            youtube = youtube,
            image_file = image_file
        )
        db.session.add(new_project)
        db.session.commit()
        flash('{} added successfuly'.format(name), 'alert alert-success')
        return redirect(url_for('projects'))
    return render_template('projects.html', title='Antony Injila | Projects Add', projects=projects)


@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', title = 'Antony Injila | Projects', projects=projects)


@app.route('/projects/detail/<int:project_id>')
def projects_detail(project_id):
    project = Project.query.get(project_id)
    comments = Comment.query.filter_by(project_id=project_id).all()
    count_comments = len(comments)
    technologies = ''
    if project.technologies:
        technologies = project.technologies.split()
    else:
        pass

    return render_template('projects_detail.html', project=project,technologies=technologies, comments=comments,count_comments=count_comments, title="Antony Injila |{} page".format(project.name))


@app.route('/projects/update/<int:project_id>', methods=['POST'])
def projects_update(project_id):
    project = Project.query.get(project_id)

    if request.method == "POST" or request.files:
        project = Project.query.get(project_id)
        name = request.form['name']
        technologies = request.form['technologies']
        youtube = request.form['youtube']
        github = request.form['github']
        description = request.form['description']

        if request.files['project-image']:
            f = request.files['project-image']
            filename = secure_filename(f.filename)
            image_file = "{}/{}/{}".format("static", "images/uploads/projects", filename)
            f.save(Config.UPLOAD_FOLDER + "/projects/" + filename)

            project.image_file = image_file
            project.name=name
            project.youtube=youtube
            project.github=github
            project.technologies = technologies
            project.description = description
            db.session.commit()
            return redirect(url_for('projects_detail', project_id=project.id))
        else:
            project.name=name
            project.youtube=youtube
            project.github=github
            project.technologies = technologies
            project.description = description
            project.image_file = request.form['old-project-image']
            db.session.commit()
            return redirect(url_for('projects_detail', project_id=project.id))

    return redirect(url_for('projects_detail', project_id=project.id))

    # return render_template('projects_update.html')


@app.route('/projects/delete/<int:project_id>')
def projects_delete(project_id):
    return render_template('projects.html')

@app.route('/comment', methods=['GET','POST'])
def comment():

    project_id = request.form['project_id']
    comment = request.form['comment']
    comment = Comment(project_id=project_id,comment=comment)
    db.session.add(comment)
    db.session.commit()
    flash("Comment added successfuly")
    return redirect(url_for('projects_detail', project_id=project_id))


@app.route('/comment/delete/<int:comment_id>/<int:project_id>', methods=['GET','POST'])
def comment_delete(comment_id,project_id):
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('projects_detail', project_id=project_id))


# Sennding an Email
@app.route('/send-email', methods=['POST','GET'])
def email():
    if request.form['email']:
        msg = Message(request.form['subject'],sender=request.form['email'], recipients=['antonyshikubu@gmail.com'])

        msg.body = "Sent by :\n{}\n{}".format(request.form['email'],request.form['body'])
        mail.send(msg)
        flash('Email received', 'alert alert-danger alert-dismissible fade show')
        return redirect(url_for('index'))
    else:
        flash("please enter your email Address")
        return redirect(url_for('index'))


@app.route('/courses')
def courses():
    return render_template('courses.html',  title='Antony Injila | Courses')


@app.errorhandler(404)
def not_found(error):
    return render_template('feedback.html', error=error, title='Antony Injila | 404'),404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('feedback.html', error=error), 500