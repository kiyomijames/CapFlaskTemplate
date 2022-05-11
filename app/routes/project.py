
from app import app, login 
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Project
from app.classes.forms import ProjectForm
from flask_login import login_required
import datetime as dt


@app.route('/project/new', methods=['GET', 'POST'])

@login_required

def projectNew():    # This gets the form object from the form.py classes that can be displayed on the template.
    form = ProjectForm()

    # This is a conditional that evaluates to 'True' if the user submitted the form successfully.
    # validate_on_submit() is a method of the form object. 
    if form.validate_on_submit():

        # This stores all the values that the user entered into the new post form. 
        # Post() is a mongoengine method for creating a new post. 'newPost' is the variable 
        # that stores the object that is the result of the Post() method.  
        newProject = Project(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.
            location = form.location.data,
            description = form.description.data,
            typem = form.typem.data,
            amountm = form.amountm.data,
            projectname = form.projectname.data,
            category = form.category.data,
            author = current_user.id,
            modifydate = dt.datetime.utcnow
        )
        # This is a method that saves the data to the mongoDB database.
        newProject.save()
        return redirect(url_for('project',projectID=newProject.id))
    return render_template('projectform.html',form=form)

@app.route('/project/edit/<projectID>', methods=['GET', 'POST'])
@login_required
def projectEdit(projectID):
    editProject = Project.objects.get(id=projectID)
    if current_user != editProject.author:
        flash("You can't edit a proeject you didn't write.")
        return redirect(url_for('post',postID=editProject.post.id))
    post = Project.objects.get(id=editProject.post.id)
    form = ProjectForm()
    if form.validate_on_submit():
        editProject.update(
            content = form.content.data,
            modifydate = dt.datetime.utcnow
        )
        return redirect(url_for('post',postID=editProject.post.id))

    form.content.data = editProject.content

    return render_template('projectform.html',form=form,post=post)   



@app.route('/project/<projectID>')
# This route will only run if the user is logged in.
@login_required
def project(projectID):
    # retrieve the post using the postID
    ThisProject = Project.objects.get(id=projectID)
    # If there are no comments the 'comments' object will have the value 'None'. Comments are 
    # related to posts meaning that every comment contains a reference to a post. In this case
    # there is a field on the comment collection called 'post' that is a reference the Post
    # document it is related to.  You can use the postID to get the post and then you can use
    # the post object (thisPost in this case) to get all the comments.
    #theseComments = Comment.objects(post=thisPost)
    # Send the post object and the comments object to the 'post.html' template.
    return render_template('project.html',project=ThisProject)

@app.route('/project/list')
# This means the user must be logged in to see this page
@login_required
def projectList():
    # This retrieves all of the 'posts' that are stored in MongoDB and places them in a
    # mongoengine object as a list of dictionaries name 'posts'.
    projects = Project.objects()
    # This renders (shows to the user) the posts.html template. it also sends the posts object 
    # to the template as a variable named posts.  The template uses a for loop to display
    # each post.
    return render_template('projects.html',projects=projects)

@app.route('/project/delete/<projectID>')
@login_required
def projectDelete(projectID): 
    deleteProject = Project.objects.get(id=projectID)
    deleteProject.delete()
    flash('The project was deleted.')
    return redirect(url_for('project',projectID=deleteProject.project.id)) 






