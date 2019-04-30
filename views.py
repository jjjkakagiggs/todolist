from flask import Flask,render_template,redirect,url_for,request,flash
from flask_login import login_required,login_user,logout_user,current_user


from todolist import app
from todolist.forms import TodoListForm,LoginForm
from todolist.models import Todolist,User
from todolist import db,login_manager


@app.route('/',methods=['GET','POST'])
@login_required
def show_todo_list():
    form = TodoListForm()
    if request.method == 'GET':
        todolists = Todolist.query.all()
        return render_template('index.html',todolists=todolists,form=form)
    else:
        if form.validate_on_submit():
            todolist = Todolist(user_id=current_user.id,title = form.title.data,status = form.status.data)
            db.session.add(todolist)
            db.session.commit()
            flash('You have add a new todo list')
        else:
            flash(form.errors)
        return redirect(url_for('show_todo_list'))



@app.route('/delete/<int:id>')
@login_required
def delete_todo_list(id):
    todolist = Todolist.query.filter_by(id = id).first_or_404()
    db.session.delete(todolist)
    db.session.commit()
    flash('You have delete a todo list')
    return redirect(url_for('show_todo_list'))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username = request.form['username']).first()
        if user:
            if user.verify_password(request.form['password']):
                login_user(user)
                flash('you have logged in!')
                return redirect(url_for('show_todo_list'))
            else:
                flash('Invalid username or password')
        else:
            flash('Invalid username or password')
    form = LoginForm(username='abc',password='111')
    return render_template('login.html',form = form)


@app.route('/change/<int:id>',methods=['GET','POST'])
@login_required
def change_todo_list(id):
    if request.method == 'GET':
        todolist = Todolist.query.filter_by(id = id).first_or_404()
        form = TodoListForm()
        form.title.data = todolist.title
        form.status.data = str(todolist.status)
        return render_template('modify.html',form=form)
    else:
        form = TodoListForm()
        if form.validate_on_submit():
            todolist = Todolist.query.filter_by(id=id).first_or_404()
            todolist.title = form.title.data
            todolist.status = form.status.data
            db.session.commit()
            flash('You have modify a todolist')
        else:
            flash(form.errors)
        return redirect(url_for('show_todo_list'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have logout!')
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = int(user_id)).first()
