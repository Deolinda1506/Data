from flask import render_template, Blueprint

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('home.html')

@routes.route('/login')
def login():
    return render_template('login.html')

@routes.route('/register')
def register():
    return render_template('register.html')
