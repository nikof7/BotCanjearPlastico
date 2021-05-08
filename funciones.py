from flask import flash
import random
from app import app, db
from flask_login import current_user
from app.models import Post

def generar_ticket():
	codigo_ticket = random.random()
	post = Post(body=codigo_ticket, author=current_user)
	db.session.add(post)
	db.session.commit()
	flash(f"Se generó su ticket con el código de {codigo_ticket}")
	return