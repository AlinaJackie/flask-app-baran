from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from . import students
from .models import Group, Student, User
from .forms import StudentForm, RegistrationForm, LoginForm
from extensions import db

# Список студентів
@students.route('/', methods=['GET'])
@login_required
def list_students():
    search_query = request.args.get('search', '')

    if search_query:
        students_list = Student.query.filter(
            (Student.name.ilike(f'%{search_query}%')) |
            (Student.email.ilike(f'%{search_query}%'))
        ).all()
    else:
        students_list = Student.query.all()

    return render_template('students/list_students.html', students=students_list, search_query=search_query)

# Створення нового студента
@students.route('/new', methods=['GET', 'POST'])
@login_required
def new_student():
    form = StudentForm()
    form.group.choices = [(group.id, group.name) for group in Group.query.all()]

    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            group_id=form.group.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Студента успішно додано!', 'success')
        return redirect(url_for('students.list_students'))

    return render_template('students/new_student.html', form=form)

# Редагування даних студента
@students.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    form.group.choices = [(group.id, group.name) for group in Group.query.all()]

    if form.validate_on_submit():
        student.name = form.name.data
        student.email = form.email.data
        student.age = form.age.data
        student.group_id = form.group.data
        db.session.commit()
        flash('Дані студента оновлено!', 'info')
        return redirect(url_for('students.list_students'))

    return render_template('students/edit_student.html', form=form, student=student)

# Видалення студента
@students.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)

    try:
        db.session.delete(student)
        db.session.commit()
        flash(f'Студента {student.name} успішно видалено!', 'danger')
    except Exception as e:
        flash('Помилка при видаленні студента!', 'danger')

    return redirect(url_for('students.list_students'))

# Деталі студента
@students.route('/student/<int:id>')
def student_details(id):
    student = Student.query.get_or_404(id)
    return render_template('students/student_details.html', student=student)

# Реєстрація нового користувача
@students.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('students.list_students'))  # Якщо користувач вже авторизований, перенаправляємо

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Логін користувача після реєстрації
        login_user(user)

        flash('You have been registered and logged in!', 'success')

        # Перенаправлення на головну сторінку
        return redirect(url_for('students.list_students'))

    return render_template('students/register.html', form=form)


# Логін користувача
@students.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('students.profile'))  # Замість profile, можете поставити іншу сторінку
        else:
            flash('Invalid username or password', 'danger')

    return render_template('students/login.html', form=form)

# Вихід користувача
@students.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('students.login'))
