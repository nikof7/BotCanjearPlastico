from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, ValidarTicket, GenerarTicket
from app.models import User, Post
from funciones import generar_ticket
import random, string

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	posts = Post.query.all()
	form = ValidarTicket()
	if form.validate_on_submit():
		for post in posts:
			if form.ticket.data == post.body:
				db.session.delete(post)
				db.session.commit()
				flash(f'Bien ahí, se verificó el ticket: {post}')
				return redirect(url_for('index'))
				break
		flash('Ticket inválido')
	return render_template('index.html', title='Home', posts=posts, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Felicitaciones, has registrado exitosamente la cuenta!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/generate', methods=['GET', 'POST'])
def generate():
	generate = GenerarTicket()
	if generate.validate_on_submit():
		password_characters = string.ascii_letters + string.digits + string.punctuation
		codigo_ticket = ''.join(random.choice(password_characters) for i in range(20))
		post = Post(body=codigo_ticket, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash(f"Se generó su ticket con el código de {codigo_ticket}")
		return redirect(url_for('generate'))
	return render_template('generate.html', title='Generador', generate=generate)
		