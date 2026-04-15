import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///shopping.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    purchased = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    items = Item.query.order_by(Item.id.desc()).all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    if name:
        db.session.add(Item(name=name))
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:id>')
def toggle(id):
    item = Item.query.get_or_404(id)
    item.purchased = not item.purchased
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)