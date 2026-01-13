from todolist import app, db, login_manager
from flask import render_template, url_for, redirect, flash    
from todolist.models import List, User
from todolist.forms import AddListForm, DeleteListForm, RegisterForm, LoginForm, LogoutForm
from flask_login import login_user, logout_user, login_required, current_user




@app.route("/home")
@login_required
def homepage():
    flash_msg = flash("Welcome back")
    return render_template("home.html", flash_msg=flash_msg)

@app.route("/add", methods=['GET', 'POST'])
@login_required
def addlist():


    form = AddListForm()
    lastnum = db.session.query(db.func.max(List.num)).filter_by(user_id=current_user.id).scalar()
    nextnum = (lastnum or 0) + 1
    if form.validate_on_submit():
        new = List(todo=form.description.data, owner=current_user, num=nextnum )
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('showlist'))


    return render_template("add.html", form=form)


@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged-in to enter this page", "error")
    return redirect(url_for('login'))

@app.route("/show")
@login_required
def showlist():
    todolist = List.query.all()
    
    for item in todolist:
        form = DeleteListForm()
        form.todo_id.data = item.list_id
        item.form = form

     
    return render_template('show.html', todolist=todolist)

@app.route("/delete", methods=["POST"])
@login_required
def deletelist():
    form = DeleteListForm()

    if form.validate_on_submit():
        
        todo_id = int(form.todo_id.data)
        todo = List.query.filter_by(list_id=form.todo_id.data).first()
        owner_num = todo.num
        if todo:
             
            db.session.delete(todo)
            db.session.commit()
            for one_todo in List.query.all():
                print("inside for")
                if one_todo.owner == current_user:
                    print("inside if")
                    if one_todo.num > owner_num:
                        one_todo.num -= 1   
                        db.session.commit()
        else:
            print(f"Todo not found: ID {todo_id }")
    
    else:
        print("Form validation failed")
        print(f"{form.validate_on_submit()}")
        print(form.todo_id.data)


    return redirect(url_for('showlist'))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print("inside validate")
        user_to_create = User(username=form.username.data, password=form.password2.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        print("Validation failed")
        print(form.username.data)
        print(form.password1.data)
        print(form.password2.data)


    return render_template("register.html", form=form)


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print("inside validate")
        print(f"{user}")
        if user and user.check_password_hash(form.password.data):
            print("inside if")
            login_user(user)
            
            return redirect(url_for('showlist'))
        print("User not found")

    return render_template("login.html", form=form)


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    form = LogoutForm()
    print("Outside validate")
    if form.validate_on_submit():
        print("Inside validate")
        logout_user()
        return redirect(url_for('login'))
    return render_template('logout.html', form=form)