from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(1000), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form.get('url')
        if original_url:
            url = URL(original_url=original_url, short_url=generate_short_url())
            db.session.add(url)
            db.session.commit()
            flash('URL shortened successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Please enter a valid URL', 'error')
    urls = URL.query.all()
    return render_template('home.html', urls=urls)

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first()
    if url:
        return redirect(url.original_url)
    else:
        flash('Invalid short URL', 'error')
        return redirect(url_for('home'))

@app.route('/history')
def history():
    urls = URL.query.all()
    return render_template('history.html', urls=urls)

def generate_short_url():
    characters = string.ascii_lowercase + string.digits
    while True:
        short_url = ''.join(random.choice(characters) for _ in range(6))
        if not URL.query.filter_by(short_url=short_url).first():
            return short_url

if __name__ == '__main__':
    app.run()
